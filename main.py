
"""
DBFZ_TSE main file:
    -reads and parses eventhubs data
    -creates Character class objects for each character and inputs data
    -saves data to a database of some sort?
    -produces scattergraphs of select statistics
    -format data to train and test unsupervised models
"""
import pdb
import parse
import engine
import predict

def init_data(eh_data):
    """Culminates data for each character within its own unique Character
    Class object.
    """
    char_class_obj_list = []
    for char in parse.CHAR_ROSTER:
        # init new character class object
        new_char_obj = engine.Character(char)
        # adding data points to class object
        for tourney in eh_data:
            tourney_name = tourney[0]
            char_dict = tourney[1]
            games_won = char_dict[char][0]
            games_played = char_dict[char][1]
            num_appear = char_dict[char][2]
            placings = char_dict[char][3]
            partners = char_dict[char][4]
            # recording games won & played
            new_char_obj.record_games(tourney_name, games_won, games_played)
            # updating appearance tally
            new_char_obj.update_appearances(tourney_name, num_appear)
            # updating placing score
            new_char_obj.update_score(placings)
            # adding partners
            new_char_obj.add_partners(partners)
        
        char_class_obj_list.append(new_char_obj)

    return char_class_obj_list

def main():
    file_path = "eventhubs_data/"
    data = parse.eh_data_parser(file_path)
    char_obj_list = init_data(data)

if __name__ == "__main__":
    main()
