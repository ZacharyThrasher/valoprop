from bs4 import BeautifulSoup
import pandas as pd
from sklearn.linear_model import LinearRegression
import sys
import matplotlib.pyplot as plt
import urllib.request
import requests
import csv


def round_predictor(team_a_odds, team_b_odds):
    # Read the CSV file
    data = pd.read_csv('odds.csv')

    # Calculate the absolute difference between the first column and the second column in the csv file
    matrix1 = data[data.columns[0]]
    matrix2 = data[data.columns[1]]
    data['rounds_per_game'] = data[data.columns[2]]
    data['abs_diff'] = abs(matrix1 - matrix2)


    # Perform linear regression using the absolute difference and column 3
    X = data[['abs_diff']]
    y = data['rounds_per_game']
    regressor = LinearRegression()
    regressor.fit(X, y)

    #print the correlation coefficient
    correlation = regressor.coef_[0]

    # find the absolute value of team_a_odds - team_b_odds
    abs_diff_odds = abs(team_a_odds - team_b_odds)

    predicted_value = regressor.predict([[abs_diff_odds]])
    print(f"Projections are based on {predicted_value} rounds per game on average. The correlation coefficient is {correlation}.")

    return predicted_value


# define a player object where we can store the player name and the player's kpr on each map
class Player:
    def __init__(self, name, kpr, rounds):
        self.name = name
        self.kpr = kpr
        self.rounds = rounds
        self.total_rounds = 0
        self.weighted_kpr = 0
        self.prop = 0
        self.projection = 0
        self.difference = 0
        self.direction = ""
        self.actualKills = 0

def algo(url):
    # URL to scrape
    theurl = url
    # Open the URL
    thepage = urllib.request.urlopen(theurl)

    # Parse the HTML
    soup = BeautifulSoup(thepage, 'html.parser')

    match_odds = soup.find_all('span', class_='match-bet-item-odds mod- mod-1')
    #if the odds are not found on the page, the user is prompted to enter the odds manually
    if not match_odds:
        print("Odds not found on the page, please enter the odds manually")
        team_a_odds = float(input("Enter the odds for team A: "))
    else:
        team_a_odds = float(match_odds[0].text)



    match_odds = soup.find_all('span', class_='match-bet-item-odds mod- mod-2')
    if not match_odds:
        team_b_odds = float(input("Enter the odds for team B: "))
    else:
        team_b_odds = float(match_odds[0].text)

    predicted_rounds = round_predictor(team_a_odds, team_b_odds)

    predicted_rounds = 2 * predicted_rounds

    # Find all the links in the HTML
    project_href = [i['href'] for i in soup.find_all('a', href=True)]

    # Find the links with /player/ in them (these are the player links) and store them in a list, removing the /player/ part
    players = [i for i in project_href if '/player/' in i]
    players = [i.replace('/player/', '') for i in players]

    #remove duplicates from the list
    players = list(dict.fromkeys(players))

    #create an empty list to store the player objects
    all_players = []

    # Loop through the player links and create a player object for each player
    for i in range(len(players)):
        # Open the player link
        thepage = urllib.request.urlopen("https://www.vlr.gg/player/" + players[i])
        soup = BeautifulSoup(thepage, 'html.parser')

        # Find the player's name
        name = soup.find('h1', class_='wf-title').text

        # remove all the spaces from the name
        name = name.replace(" ", "")

        # Load the player's stats table
        # The stats table is separated into rows and columns using the <tr> and <td> tags respectively
        # Each Row represents a different agent and the columns represent the stats for that agent
        # The 9th column in each row represents the KPR for that agent
        # each agent's kpr should be added to the player object

        table = soup.find('table', class_='wf-table')
        rows = table.find_all('tr')
        rounds = []
        kpr = []
        cols = []

        # Loop through the rows and columns to find the KPR for each agent, but throw out the first row
        for row in rows[1:]:
            cols.append(row.find_all('td'))

        for col in cols:
            #cols[2] is the rounds column
            #cols[8] is the KPR column
            # print the rounds and kpr for each agent on the same line
            kpr.append(col[8].text)
            rounds.append(col[2].text)
        
        # Create a player object and add it to the team_a list
        player = Player(name, kpr, rounds)
        all_players.append(player)

    # Calculate the weighted average kpr for each player using their rounds played as the weights

    for player in all_players:
        total_kpr = 0
        for i in range(len(player.rounds)):
            player.total_rounds += int(player.rounds[i])
            total_kpr += float(player.kpr[i]) * int(player.rounds[i])

        player.weighted_kpr = total_kpr / player.total_rounds
        player.projection = player.weighted_kpr * predicted_rounds
        player.prop = float(input("Enter " + player.name + "'s prop: " ))
        player.difference = player.projection - player.prop
        if player.difference > 0:
            player.direction = "over"
        else:
            player.direction = "under"
        

    #print a few new lines to separate the output
    print("\n\n")

    # Print the weighted average kpr for each player
    for player in all_players:
        print(player.name + " is projected to get " + str(player.projection) + " kills if they average a " + str(player.weighted_kpr) + " weighted KPR, which means you should take the " + player.direction + " on " + str(player.prop) + " kills because they would cover by " + str(player.difference) + ". This was based on " + str(player.total_rounds) + " rounds of data.")

def calculate_team_b_odds(odds_team_b):
    # Convert overround to a decimal
    overround_decimal = 0.08653846153846153846153846153846
    # Calculate the implied probability for team B
    implied_prob_team_b = 1 / odds_team_b
    
    # Calculate the adjusted implied probability for team A
    implied_prob_team_a = 1 / (1 + overround_decimal - implied_prob_team_b)
    
    
    return implied_prob_team_a

# manual input
# algo(input("Enter the URL of the match: "))

# do the same thing except wih historical data
def historical_algo():
    session1 = requests.Session()
    session2 = requests.Session()
    for page_num in range(0, 1):
        # Send a GET request to the VLR website
        base_url = 'https://vlr.orlandomm.net/api/v1/results?page='
        response = session1.get(base_url + str(page_num))

        # Parse the json response
        data = response.json()
        matches = data['data']
        match_id_array = []
        for match in matches:
            match_id_array.append(match['id'])

        # Extract the rating difference and number of rounds for each match result
        for itr in match_id_array:

            # make a new get request to get the match data
            match_url = 'https://vlr.gg/' + itr
            response = session2.get(match_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            games = BeautifulSoup(response.content, 'html.parser')

            match_odds = soup.find_all('span', class_='match-bet-item-odds')
            #if the odds are not found on the page, set the odds to 1
            if not match_odds:
                team_a_odds = 1
                team_b_odds = 1
            else:
                team_a_odds = float(float(match_odds[1].text[1:]) / 100)
                team_b_odds = float(calculate_team_b_odds(team_a_odds))

            predicted_rounds = round_predictor(team_a_odds, team_b_odds)

            predicted_rounds = 2 * predicted_rounds

            



            #find the team ratings
            # Find all the links in the HTML
            project_href = [i['href'] for i in soup.find_all('a', href=True)]

            # Find the links with /player/ in them (these are the player links) and store them in a list, removing the /player/ part
            players_url = [i for i in project_href if '/player/' in i]
            players = [i.replace('/player/', '') for i in players_url]

            #remove duplicates from the list
            players = list(dict.fromkeys(players))

            #create an empty list to store the player objects
            all_players = []

            # Loop through the player links and create a player object for each player
            for i in range(len(players)):
                # Open the player link
                thepage = urllib.request.urlopen("https://www.vlr.gg/player/" + players[i])
                soup = BeautifulSoup(thepage, 'html.parser')

                # Find the player's name
                name = soup.find('h1', class_='wf-title').text

                # remove all the spaces from the name
                name = name.replace(" ", "")

                # Load the player's stats table
                # The stats table is separated into rows and columns using the <tr> and <td> tags respectively
                # Each Row represents a different agent and the columns represent the stats for that agent
                # The 9th column in each row represents the KPR for that agent
                # each agent's kpr should be added to the player object

                table = soup.find('table', class_='wf-table')
                rows = table.find_all('tr')
                rounds = []
                kpr = []
                cols = []

                # Loop through the rows and columns to find the KPR for each agent, but throw out the first row
                for row in rows[1:]:
                    cols.append(row.find_all('td'))

                for col in cols:
                    #cols[2] is the rounds column
                    #cols[8] is the KPR column
                    # print the rounds and kpr for each agent on the same line
                    kpr.append(col[8].text)
                    rounds.append(col[2].text)
                
                # Create a player object and add it to the team_a list
                player = Player(name, kpr, rounds)
                all_players.append(player)

            # Calculate the weighted average kpr for each player using their rounds played as the weights
            for player in all_players:
                total_kpr = 0
                for i in range(len(player.rounds)):
                    player.total_rounds += int(player.rounds[i])
                    total_kpr += float(player.kpr[i]) * int(player.rounds[i])

                player.weighted_kpr = total_kpr / player.total_rounds
                player.projection = player.weighted_kpr * predicted_rounds
                player.difference = player.projection - player.prop
                if player.difference > 0:
                    player.direction = "over"
                else:
                    player.direction = "under"
                game_stats = games.find_all('div', class_='vm-stats-game ')
                for game in game_stats:
                    tmp = game.find('table','wf-table-inset mod-overview')
                    if tmp is None:
                        continue
                    rows = tmp.find_all('tr')
                    for row in rows[1:]:
                        cols = row.find_all('td')
                        player.actualKills += int(cols[4].text)
                        print(player.name + " has " + str(player.actualKills) + " kills.")
       



algo(input("Enter the URL of the match: "))


