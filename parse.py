"""
DBFZ_TSE tournament results parser file
"""
import pdb
import os
import time

CHAR_ROSTER = ['Adult Gohan', 'Android #16', 'Android #18', 'Android #21',
        'Bardock', 'Beerus', 'Broly', 'Captain Ginyu', 'Cell', 'Frieza',
        'Teen Gohan', 'Blue Goku', 'Goku', 'Goku Black', 'Gotenks', 'Hit',
        'Kid Buu', 'Krillin', 'Majin Buu', 'Nappa', 'Piccolo', 'Tien',
        'Trunks', 'Blue Vegeta', 'Vegeta', 'Vegito', 'Yamcha', 'Zamasu']

def eh_data_parser(file_path):
    """Parses tournament results from eventhubs saved onto txt files
    into usable format for engine.
    :output: list of lists of tourney names, a dictionary of character names,
        serving as the keys for a list of # of games won, played, appearances,
        a list of placings for each character for each tournament, and a list
        of partners used for each character.
    """
    start_time = time.time()
    result = []
    file_name_list = os.listdir(file_path)
    for file_name in file_name_list:
        # {character name: games won, games played,
        #               appearances, [all placings], [partners]}
        character_dict = {}
        # enumerating dict entries for each character
        for char in CHAR_ROSTER:
            character_dict[char] = [0, 0, 0, [], []]
        # opening and formatting raw data
        text_file = open(file_path+file_name, "r")
        raw_lines = text_file.readlines()
        lines = list(map(lambda x: x[:-1], raw_lines))  # removing '/n'
        lines = list(filter(None, lines))  # removing empty str elements
        lines[-1] = raw_lines[-1] # bugfix since last line doesn't have '\n'
        standings = lines[0:8]
        battle_log = lines[9:]

        for placing in standings:
            place = placing[0]
            # isolating team string
            splice_point = placing.index('(') + 1
            team_string = placing[splice_point:len(placing)-1]
            # formatting into a list
            team = team_string.split(',')
            # removing extra spaces
            length = len(team)
            for i in range(1, length):
                team[i] = team[i][1:]
            for char in team:
                # incrementing appearance counter
                character_dict[char][2] += 1
                # adding placing to list of placings
                character_dict[char][3].append(place)
                # adding partners to list of partners
                for other_char in team:
                    if char != other_char:
                        character_dict[char][4].append(other_char)
        
        for battle in battle_log:
            first_team_score = int(battle[-4])
            second_team_score = int(battle[-2])
            games_played = first_team_score + second_team_score
            right_parens_indices = []
            left_parens_indices = []
            r_index = 0
            l_index = 0
            # locating both player's teams in string
            while (r_index and l_index) < len(battle) :
                r_index = battle.find('(', r_index)
                l_index = battle.find(')', l_index)
                if r_index == -1 and l_index == -1:
                    break
                right_parens_indices.append(r_index+1)
                left_parens_indices.append(l_index)
                r_index += 1
                l_index += 1
            # splicing teams out of string
            first_team_string =\
                    battle[right_parens_indices[0]:left_parens_indices[0]]
            second_team_string =\
                    battle[right_parens_indices[1]:left_parens_indices[1]]
            # converting into lists
            first_team = first_team_string.split(',')
            second_team = second_team_string.split(',')
            # removing extra spaces
            first_length = len(first_team)
            second_length = len(second_team)
            for j in range(1, first_length):
                first_team[j] = first_team[j][1:]
            for k in range(1, second_length):
                second_team[k] = second_team[k][1:]
            for l in range (3):
                # adding games won to sum of games won
                character_dict[first_team[l]][0] += first_team_score
                character_dict[second_team[l]][0] += second_team_score
                # adding games played to sum of games played
                character_dict[first_team[l]][1] += games_played
                character_dict[second_team[l]][1] += games_played

        result.append([file_name, character_dict])
    print(str(time.time() - start_time) + ' seconds long')
    
    return result

def main():
    file_path = "eventhubs_data/"
    eh_data_parser(file_path)


if __name__ == "__main__":
    main()
