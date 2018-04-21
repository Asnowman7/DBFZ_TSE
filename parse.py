"""
DBFZ_TSE tournament results parser file
"""
import pdb
import os
import pandas as pd

def eh_data_parser(file_path):
    """Parses tournament results from eventhubs saved onto txt files
    into usable format for engine.
    :output: list of lists of tourney names, a dictionary of character names,
        serving as the keys for a list of # of games won, played, appearances,
        and list of placings for each character for each tournament.
    """
    result = []
    file_name_list = os.listdir(file_path)
    for file_name in file_name_list:
        # {character name: games won, games played,
        #               appearances, [all placings]}
        character_dict = {
                'Adult Gohan' : [0, 0, 0, []], 'Android #16' : [0, 0, 0, []],
                'Android #18' : [0, 0, 0, []], 'Android #21' : [0, 0, 0, []],
                'Bardock' : [0, 0, 0, []], 'Beerus' : [0, 0, 0, []],
                'Broly' : [0, 0, 0, []], 'Captain Ginyu' : [0, 0, 0, []],
                'Cell' : [0, 0, 0, []], 'Frieza' : [0, 0, 0, []],
                'Teen Gohan' : [0, 0, 0, []], 'Blue Goku' : [0, 0, 0, []],
                'Goku' : [0, 0, 0, []], 'Goku Black' : [0, 0, 0, []],
                'Gotenks' : [0, 0, 0, []], 'Hit' : [0, 0, 0, []],
                'Kid Buu' : [0, 0, 0, []], 'Krillin' : [0, 0, 0, []],
                'Majin Buu' : [0, 0, 0, []], 'Nappa' : [0, 0, 0, []],
                'Piccolo' : [0, 0, 0, []], 'Tien' : [0, 0, 0, []],
                'Trunks' : [0, 0, 0, []], 'Blue Vegeta' : [0, 0, 0, []],
                'Vegeta' : [0, 0, 0, []], 'Yamcha' : [0, 0, 0, []]}
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
            team[1] = team[1][1:]
            team[2] = team[2][1:]
            for char in team:
                # incrementing appearance counter
                character_dict[char][2] += 1
                # adding placing to list of placings
                character_dict[char][3].append(place)
        
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
            first_team[1] = first_team[1][1:]
            first_team[2] = first_team[2][1:]
            second_team[1] = second_team[1][1:]
            second_team[2] = second_team[2][1:]
            for i in range (3):
                # adding games won to sum of games won
                character_dict[first_team[i]][0] += first_team_score
                character_dict[second_team[i]][0] += second_team_score
                # adding games played to sum of games played
                character_dict[first_team[i]][1] += games_played
                character_dict[second_team[i]][1] += games_played

        result.append([file_name, character_dict])
    return result

def main():
    file_path = "eventhubs_data/"
    eh_data_parser(file_path)


if __name__ == "__main__":
    main()
