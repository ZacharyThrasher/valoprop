class Match:
    def __init__(self):
        self.team1 = ""
        self.team2 = ""
        self.team1_first_pick = ""
        self.team2_first_pick = ""
        self.team1_first_ban = ""
        self.team2_first_ban = ""
        self.team1_second_ban = ""
        self.team2_second_ban = ""
        self.remaining_map = ""

def parse_match_string(match_string):
    match_data = match_string.split(";")
    
    match = Match()
    match.team1_first_ban = match_data[0]
    match.team1 = match.team1_first_ban.split(" ")[0]
    match.team1_first_ban = match.team1_first_ban.split(" ")[2]
    match.team2_first_ban = match_data[1]
    match.team2 = match.team2_first_ban.split(" ")[0]
    match.team2_first_ban = match.team2_first_ban.split(" ")[3]
    match.team1_first_pick = match_data[2]
    match.team1_first_pick = match.team1_first_pick.split(" ")[3]
    match.team2_first_pick = match_data[3]
    match.team2_first_pick = match.team2_first_pick.split(" ")[3]
    match.team1_second_ban = match_data[4]
    match.team1_second_ban = match.team1_second_ban.split(" ")[3]
    match.team2_second_ban = match_data[5]
    match.team2_second_ban = match.team2_second_ban.split(" ")[3]
    match.remaining_map = match_data[6]
    match.remaining_map = match.remaining_map.split(" ")[1]
    return match

def print_matches(match):
    print("TEAM 1 " + match.team1)
    print("TEAM 2 " + match.team2)
    print("BAN 1 " + match.team1_first_ban)
    print("BAN 2 " + match.team2_first_ban)
    print("PICK 1 " + match.team1_first_pick)
    print("PICK 2 " + match.team2_first_pick)
    print("BAN 3 " + match.team1_second_ban)
    print("BAN 4 " + match.team2_second_ban)
    print("REMAINING MAP " + match.remaining_map)


# PUT MATCH STRING HERE
match_string = "BLD ban Ascent; RRQ ban Sunset; BLD pick Lotus; RRQ pick Icebox; BLD ban Split; RRQ ban Bind; Breeze remains TLN ban Breeze; BLD ban Ascent; TLN pick Lotus; BLD pick Bind; TLN ban Split; BLD ban Sunset; Icebox remains GE ban Lotus; BLD ban Ascent; GE pick Sunset; BLD pick Icebox; GE ban Breeze; BLD ban Bind; Split remains BLD ban Ascent; T1 ban Icebox; BLD pick Breeze; T1 pick Lotus; BLD ban Sunset; T1 ban Bind; Split remains DFM ban Bind; BLD ban Split; DFM ban Lotus; BLD ban Sunset; DFM ban Breeze; BLD ban Ascent; Haven remains"

# PUT TEAM NAME HERE
TEAM_NAME = "BLD"

#parse the match string into individual matches
match_parsed_string = match_string.split("remains ")

match1 = parse_match_string(match_parsed_string[0])

match2 = parse_match_string(match_parsed_string[1])

match3 = parse_match_string(match_parsed_string[2])

match4 = parse_match_string(match_parsed_string[3])

match5 = parse_match_string(match_parsed_string[4])

#store all of the matches in an array
matches = [match1, match2, match3, match4, match5]

#create array to store all of team name's first picks and print them
team_first_picks = []
for match in matches:
    if match.team1 == TEAM_NAME:
        team_first_picks.append(match.team1_first_pick)
    else:
        team_first_picks.append(match.team2_first_pick)
print("")
print("First picks: ") 
print(team_first_picks)


#find the most common first pick and print it
tmp = max(set(team_first_picks), key = team_first_picks.count)
print("")
print("Most common " + TEAM_NAME + " first pick: " + tmp)
print("Number of times " + tmp + " was picked first: " + str(team_first_picks.count(tmp)))

#do the same for the first bans
team_first_bans = []
for match in matches:
    if match.team1 == TEAM_NAME:
        team_first_bans.append(match.team1_first_ban)
    else:
        team_first_bans.append(match.team2_first_ban)
print("")
print("First Bans: ")
print(team_first_bans)

tmp = max(set(team_first_bans), key = team_first_bans.count)
print("")
print("Most common " + TEAM_NAME + " first ban: " + tmp)
print("Number of times " + tmp + " was banned first: " + str(team_first_bans.count(tmp)))

#do the same for the second bans
team_second_bans = []
for match in matches:
    if match.team1 == TEAM_NAME:
        team_second_bans.append(match.team1_second_ban)
    else:
        team_second_bans.append(match.team2_second_ban)

print("")
print("Second bans: ")
print(team_second_bans)

tmp = max(set(team_second_bans), key = team_second_bans.count)
print("")
print("Most common " + TEAM_NAME + " second ban: " + tmp)
print("Number of times " + tmp + " was banned second: " + str(team_second_bans.count(tmp)))

#do the same for the remaining maps
remaining_maps = []
for match in matches:
    remaining_maps.append(match.remaining_map)

tmp = max(set(remaining_maps), key = remaining_maps.count)

print("")
print("Remaining maps: ")
print(remaining_maps)

#find the most common remaining map and print it
print("")
print("Most common remaining map: " + tmp)
print("Number of times " + tmp + " was left remaining: " + str(remaining_maps.count(tmp)))


