import requests
from bs4 import BeautifulSoup
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import csv

def calculate_team_a_odds(odds_team_b):
    # Convert overround to a decimal
    overround_decimal = 0.08653846153846153846153846153846
    # Calculate the implied probability for team B
    implied_prob_team_b = 1 / odds_team_b
    
    # Calculate the adjusted implied probability for team A
    implied_prob_team_a = 1 / (1 + overround_decimal - implied_prob_team_b)
    
    
    return implied_prob_team_a

# Example usage:
# odds_team_b = 2.0  # Example odds for team B
# overround = 5  # Example overround (5%)
# odds_team_a = calculate_team_a_odds(odds_team_b)
# print("Adjusted odds for team A winning:", round(odds_team_a, 2))


session1 = requests.Session()
session2 = requests.Session()

# Initialize lists to store the rating difference and number of rounds
odds_diffs = []
rounds_played = []
with open(r'odds.csv', 'a', newline='') as csvfile:
    fieldnames = ['Odds Team A','Odds Team B','Rounds Played Per Game']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    

    for page_num in range(101, 151):
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

            #find the team ratings
            match_odds = soup.find_all('span', class_='match-bet-item-odds')

            #remove all of the extra characters from the ratings
            if len(match_odds) == 0:
                continue

            decimal_odds = int(match_odds[1].text[1:]) / 100

            if decimal_odds == 0:
                continue


            other_team_odds = calculate_team_a_odds(decimal_odds)
  

            round_scores = soup.find_all('div', class_='score')

            if len(round_scores) == 0:
                continue

            rounds = 0
            for numRounds in round_scores:
                rounds += int(numRounds.text)
            rounds_per_game = rounds / (len(round_scores) / 2)

            writer.writerow({'Odds Team A':decimal_odds, 'Odds Team B':other_team_odds, 'Rounds Played Per Game':rounds_per_game})

