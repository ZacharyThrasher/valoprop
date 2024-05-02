from bs4 import BeautifulSoup
import pandas as pd
from sklearn.linear_model import LinearRegression
import sys
import matplotlib.pyplot as plt
import urllib.request
import requests
import csv

session1 = requests.Session()
session2 = requests.Session()

# create a dictionary to assign a number to each agent
agent_map = {
    'astra': 1,
    'breach': 2,
    'brimstone': 3,
    'chamber': 4,
    'clove': 5,
    'cypher': 6,
    'deadlock': 7,
    'fade': 8,
    'gekko': 9,
    'harbor': 10,
    'iso': 11,
    'jett': 12,
    'kayo': 13,
    'killjoy': 14,
    'neon': 15,
    'omen': 16,
    'phoenix': 17,
    'raze': 18,
    'reyna': 19,
    'sage': 20,
    'skye': 21,
    'sova': 22,
    'viper': 23,
    'yoru': 24
}

# I need an object to store every player object I create while scraping the data, so that I can access the player objects later--there also needs to be no duplicates in this object and I need to be able to access the player objects by their name
all_players = {}


#make a map in python

#player_map = {}

def calculate_team_b_odds(odds_team_b):
    # Convert overround to a decimal
    overround_decimal = 0.08653846153846153846153846153846
    # Calculate the implied probability for team B
    implied_prob_team_b = 1 / odds_team_b
    
    # Calculate the adjusted implied probability for team A
    implied_prob_team_a = 1 / (1 + overround_decimal - implied_prob_team_b)
    
    
    return implied_prob_team_a



class Stats:
    def __init__(self, rounds, kast, kpr, fkpr, fdpr):
        self.rounds = int(rounds)
        self.kast = float(kast)
        self.kpr = float(kpr)
        self.fkpr = float(fkpr)
        self.fdpr = float(fdpr)
    def get_weighted_stats(self):
        self.weighted_kpr = (self.kpr * self.rounds)
        self.weighted_kast = (self.kast * self.rounds)
        self.weighted_fkpr = (self.fkpr * self.rounds)
        self.weighted_fdpr = (self.fdpr * self.rounds)
        return Stats(self.rounds, self.weighted_kast, self.weighted_kpr, self.weighted_fkpr, self.weighted_fdpr)
    #define addition for the Stats class
    def __add__(self, other):
        return Stats(self.rounds + other.rounds, self.kast + other.kast, self.kpr + other.kpr, self.fkpr + other.fkpr, self.fdpr + other.fdpr)
    #define subtraction for the Stats class
    def __sub__(self, other):
        return Stats(self.rounds - other.rounds, self.kast - other.kast, self.kpr - other.kpr, self.fkpr - other.fkpr, self.fdpr - other.fdpr)
    #define division for the Stats class
    def __truediv__(self, number):
        return Stats(self.rounds, self.kast / number, self.kpr / number, self.fkpr / number, self.fdpr / number)
    def weighted_average(self, other):
        agent1_stats = self.get_weighted_stats()
        agent2_stats = other.get_weighted_stats()
        weighted_average = agent1_stats + agent2_stats
        weighted_average =  weighted_average /  weighted_average.rounds
        return weighted_average
    def __array__(self):
        return [self.rounds, self.kast, self.kpr, self.fkpr, self.fdpr]
    def __str__(self):
        return f"Rounds: {self.rounds}, KAST: {self.kast}, KPR: {self.kpr}, FKPR: {self.fkpr}, FDPR: {self.fdpr}"


class Player:
    def __init__(self, name):
        self.name = name.strip()
        self.total_rounds = 0
        self.gameKills = []
        self.actualKills = 0

        # take each row of the stats table and create a stats object for each agent they've played in the past 60 days, storing them in a list that is indexed by the agent name
        self.agent_stats = {}
        self.agent_names = []

        self.all_agents_average = None

        # match_agent_average is a Stats object that stores the average stats for the agents the player played in the match, using self.agent_stats
        self.match_agent_average = None

        # difference in betting odds between the two teams
        self.oddsDifference = 0

        # queue with the kpr the player has had in the last 5 games
        self.recent_performance = []

        self.average_opposing_player = None
   
    def load_stats_table(self, table):

        # clear the agent stats dictionary
        self.agent_stats = {}

        # clear the agent names list
        self.agent_names = []

        cols = []
        
        rows = table.find_all('tr')

        # Loop through the rows and columns to find the KPR for each agent, but throw out the first row
        for row in rows[1:]:
            if(row.find_all('td') == []):
                print("Found no rows")
                continue
            cols.append(row.find_all('td'))

        for col in cols:
            #cols[0] is the agent name column
            #cols[2] is the rounds column
            #cols[3] is the rating column
            #cols[4] is the ACS column
            #cols[5] is the KD column
            #cols[6] is the ADR column
            #cols[7] is the KAST column
            #cols[8] is the KPR column
            #cols[9] is the APR column
            #cols[10] is the FKPR column
            #cols[11] is the FDPR column
            # print the rounds and kpr for each agent on the same line
            #print(name, "'s NEW AGENT: ")
            # iterate through col and if any of the columns are empty, go to the next agent
            if col[0].find('img')['alt'] == '' or col[2].text.strip() == '' or col[3].text.strip() == '' or col[4].text.strip() == '' or col[5].text.strip() == '' or col[6].text.strip() == '' or col[7].text.strip() == '' or col[8].text.strip() == '' or col[9].text.strip() == '' or col[10].text.strip() == '' or col[11].text.strip() == '':
                print("Stats were empty")
                continue
            rounds = col[2].text.strip()
            kast = col[7].text.strip().strip('%')
            kpr = col[8].text.strip()
            fkpr = col[10].text.strip()
            fdpr = col[11].text.strip()
            self.agent_stats[col[0].find('img')['alt']] = Stats(rounds, kast, kpr, fkpr, fdpr)
            self.agent_names.append(col[0].find('img')['alt'])

    def average_match_agents(self, agent1_name, agent2_name):
        #store the stats for agent1 and agent 2 in temporary variables
        agent1_stats = self.agent_stats[agent1_name]
        agent2_stats = self.agent_stats[agent2_name]
        self.match_agent_average = agent1_stats.weighted_average(agent2_stats)
        self.total_rounds = self.match_agent_average.rounds

    def average_all_agents(self):
        # Calculate the average stats for all agents the player has played in the past 60 days
        total_stats = Stats(0, 0, 0, 0, 0)
        for agent in self.agent_stats:
            total_stats += self.agent_stats[agent].get_weighted_stats()
        if total_stats.rounds == 0:
            return -1
        self.all_agents_average = total_stats / total_stats.rounds
        return 0
    
    def average_opposing_team(self, players):
        #takes a list of player objects and calculates the average stats for the opposing team
        total_stats = Stats(0, 0, 0, 0, 0)
        for player in players:
            if(player.average_all_agents() == -1):
                return -1
            total_stats += player.all_agents_average
        self.average_opposing_player = total_stats / len(players)
        return 0
    def average_recent_performance(self):
        # Calculate the average kpr for the player over the last 5 games
        total_kpr = 0
        for kpr in self.recent_performance:
            total_kpr += kpr
        return total_kpr / len(self.recent_performance)

       

# create headers for the csv file
fieldnames = (['Name','Agent1','Agent2','Total Rounds','Weighted KPR','Weighted KAST','Weighted FKPR','Weighted FDPR','Odds Difference','Average Opposing KPR','Average Opposing KAST','Average Opposing FKPR','Average Opposing FDPR','Recent Kill Average','Actual Kills'])


def add_player_csv(player, agent1, agent2, opponents, csv_file):
    # find the average stats for the agents the player played in the match
    #if agent1 or agent 2 are not in the player's agent_stats dictionary, go to the next player
    if agent1 not in player.agent_stats or agent2 not in player.agent_stats:
        return
    #if the opposing team is empty, go to the next player
    if len(opponents) == 0:
        return
    if len(player.recent_performance) == 0:
        return
    player.average_match_agents(agent1, agent2)
    # find the average stats for the opposing team
    if (player.average_opposing_team(opponents) == -1):
        return
    # find the average recent performance for the player
    recent_kpr = player.average_recent_performance()
    # open the csv file in append mode
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        #convert the player's agent names to numbers
        agent1 = agent_map[agent1]
        agent2 = agent_map[agent2]
        writer.writerow([player.name, agent1, agent2, player.match_agent_average.rounds, player.match_agent_average.kpr, player.match_agent_average.kast, player.match_agent_average.fkpr, player.match_agent_average.fdpr, player.oddsDifference, player.average_opposing_player.kpr, player.average_opposing_player.kast, player.average_opposing_player.fkpr, player.average_opposing_player.fdpr, recent_kpr, player.actualKills])

    
def get_player_total_kills(player, game_stats): 
    tmp = player 
    tmp.gameKills = []
    for game in game_stats:
        stats_container = game.find_all('div','vm-stats-game')
        #print(stats_container)
        for stats in stats_container:
            rows = stats.find_all('tr')
            for row in rows[1:]:
                player_kills = row.find('td', class_='mod-stat mod-vlr-kills')
                if player_kills is None:
                    continue
                kill_stats = player_kills.find('span', class_='side mod-side mod-both')
                if kill_stats.text.strip() == '' or kill_stats.text.strip() == '\xa0':
                    print("Kills stats were empty")
                    continue 
                #if kills stats was a non breaking space, go to the next row
                #print(kill_stats)
                #find the player link in the row
                player_link = row.find('a', href=True)
                if player_link is None:
                    print("Player link not found")
                    continue
                scraped_name = player_link.find('div', class_='text-of')
                #print(scraped_name)
                #remove padding used in the scraped name
                scraped_name = scraped_name.text.strip()
                if tmp.name.lower() in scraped_name.lower():
                    tmp.gameKills.append(int(kill_stats.text.strip()))
    #remove the second element from gameKills
    if len(tmp.gameKills) < 3:
        return -1
    tmp.gameKills.pop(1)
    if len(tmp.gameKills) == 3:
        tmp.gameKills.pop(2)
    tmp.actualKills = 0
    #sum the kills in the gameKills list
    for kills in tmp.gameKills:
        tmp.actualKills += kills

    if(len(tmp.recent_performance) < 3):
        tmp.recent_performance.append(tmp.actualKills)
    else: 
        tmp.recent_performance.pop(0)
        tmp.recent_performance.append(tmp.actualKills)

    return tmp


# make a new get request to get the match data
# 27 pages seems to be past 2 months
for page_num in range(0, 27):
        print("Page number: ", page_num)
        # Send a GET request to the VLR website
        base_url = 'https://vlr.orlandomm.net/api/v1/results?page='
        response = session1.get(base_url + str(page_num))

        # Parse the json response
        data = response.json()
        matches = data['data']
        match_id_array = []
        for match in matches:
            #exclude the non Champions Tour tournament matches, and only include tournaments that have Americas, EMEA, China, Pacific in the title
            if 'Champions Tour' not in match['tournament'] and not ('Americas' in match['tournament'] or 'EMEA' in match['tournament'] or 'Pacific' in match['tournament']):
                continue
            match_id_array.append(match['id'])

        # go through each match
        for itr in match_id_array:
            print("Match ID: ", itr)
            # make a new get request to get the match data
            match_url = 'https://vlr.gg/' + str(itr)
            response = session2.get(match_url)
            match_page = BeautifulSoup(response.content, 'html.parser')

            match_odds = match_page.find_all('span', class_='match-bet-item-odds')
            #if the odds are not found on the page, go next
            if match_odds == []:
                #print("Odds not found")
                continue
            else:
                if(float(match_odds[1].text[1:])/100 == 0):
                    #print("Odds are 0")
                    continue
                team_a_odds = float(float(match_odds[1].text[1:]) / 100)
                team_b_odds = float(calculate_team_b_odds(team_a_odds))

                
            # get the links on the site
            project_href = [i['href'] for i in match_page.find_all('a', href=True)]

            # Find the links with /player/ in them (these are the player links) and store them in a list, removing the /player/ part
            players_url = [i for i in project_href if '/player/' in i]

            # remove duplicates in players_url
            players_url = list(dict.fromkeys(players_url))

            # make sure there are 10 players in the list
            if len(players_url) != 10:
                #print("Wrong number of players")
                continue
            # the first 5 players_url are the players on team a, the next 5 are the players on team b
            team_a_players = players_url[:5]
            team_b_players = players_url[5:]

            team_a_players_links = [i.replace('/player/', '') for i in team_a_players]
            team_b_players_links = [i.replace('/player/', '') for i in team_b_players]

            team_a_players_names = [i.split('/')[1] for i in team_a_players_links]
            team_b_players_names = [i.split('/')[1] for i in team_b_players_links]

            team_a_player_map = dict(zip(team_a_players_names, team_a_players_links))
            team_b_player_map = dict(zip(team_b_players_names, team_b_players_links))
  
            game_stats = match_page.find_all('div', class_='vm-stats-container')

            team_a_players = []
            team_b_players = []

            #go through team a, find which ones are in all_players, if they are not, add them to all_players
            for player in team_a_player_map:
                if player in all_players:
                    #print("Player already in all_players")
                    # add the player to the team a players list
                    all_players[player] = get_player_total_kills(all_players[player], game_stats)
                    all_players[player].oddsDifference = abs(team_a_odds - team_b_odds)
                    team_a_players.append(all_players[player])
                else: 
                    player_link = team_a_player_map[player]
                    #print("Player link: ", player_link)
                    # Open the player link
                    thepage = urllib.request.urlopen("https://www.vlr.gg/player/" + player_link)
                    player_page = BeautifulSoup(thepage, 'html.parser')
                    # Find the player's name
                    # Load the player's stats table
                    table = player_page.find('table', class_='wf-table')
                    if table is None:
                        print("Table was empty")
                        continue
                    # Create a player object and add it to player list
                    tmp_player = Player(player)
                    tmp_player.load_stats_table(table)
                    all_players[player] = get_player_total_kills(tmp_player, game_stats)
                    all_players[player].oddsDifference = abs(team_a_odds - team_b_odds)
                    #add the player to the team a players list
                    team_a_players.append(tmp_player)
            
            #go through team b, find which ones are in all_players, if they are not, add them to all_players
            for player in team_b_player_map:
                if player in all_players:
                    # add the player to the team b players list
                    all_players[player] = get_player_total_kills(all_players[player], game_stats)
                    all_players[player].oddsDifference = abs(team_a_odds - team_b_odds)
                    team_b_players.append(all_players[player])
                    if len(all_players.get(player).recent_performance) < 3:
                        print("Not enough games in the recent performance queue to add " + all_players[player].name + " to the csv file. Their recent performance queue has " + str(len(all_players[player].recent_performance)) + " games")
                        continue
                    #if the player's agent_names list is empty, go to the next player
                    if len(all_players.get(player).agent_names) == 0:
                        continue
                    if len(all_players.get(player).agent_names) == 1:
                        agent1 = all_players.get(player).agent_names[0]
                        agent2 = all_players.get(player).agent_names[0]
                    else:
                        agent1 = all_players.get(player).agent_names[0]
                        agent2 = all_players.get(player).agent_names[1]
                    add_player_csv(all_players[player], agent1, agent2, team_b_players, 'testStats.csv')
                else: 
                    player_link = team_b_player_map[player]
                    # Open the player link
                    thepage = urllib.request.urlopen("https://www.vlr.gg/player/" + player_link)
                    player_page = BeautifulSoup(thepage, 'html.parser')
                    # Find the player's name
                    # Load the player's stats table
                    table = player_page.find('table', class_='wf-table')
                    if table is None:
                        print("Table was empty")
                        continue
                    # Create a player object and add it to player list
                    tmp_player = Player(player)
                    tmp_player.load_stats_table(table)
                    #get the total kills for the player
                    #adding the player to the all_players dictionary
                    print("Adding " + tmp_player.name + " to all_players")
                    all_players[player] = get_player_total_kills(tmp_player, game_stats)
                    all_players[player].oddsDifference = abs(team_a_odds - team_b_odds)
                    #add the player to the team b players list
                    team_b_players.append(tmp_player)
                    #print("First time seeing " + tmp_player.name + " in data")
            
            # now add the team a players to the csv file
            for player in team_a_player_map:
                if player in all_players:
                    if len( all_players[player].recent_performance) < 3:
                        print("Not enough games in the recent performance queue to add " + all_players[player].name + " to the csv file. Their recent performance queue has " + str(len(all_players[player].recent_performance)) + " games")
                        continue
                    print("Adding " + all_players[player].name + " to the csv file")
                    #if the player's agent_names list is empty, go to the next player
                    if len(all_players.get(player).agent_names) == 0:
                        continue
                    if len(all_players.get(player).agent_names) == 1:
                        agent1 = all_players.get(player).agent_names[0]
                        agent2 = all_players.get(player).agent_names[0]
                    else:
                        agent1 = all_players.get(player).agent_names[0]
                        agent2 = all_players.get(player).agent_names[1]
                    add_player_csv(all_players[player], agent1, agent2, team_b_players, 'testStats.csv')
                else:
                    #print("Player not in all_players")
                    continue

                
