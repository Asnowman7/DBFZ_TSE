
"""
DBFZ_TSE engine file
"""
import pdb
from collections import Counter

# points rewarded to score for each placing (subject to change)
placing_points_dict = {'1' : 8, '2' : 7, '3' : 6, '4' : 5, '5' : 4, '7' : 3}

class Character:

    def __init__(self, name):
        self.name = name
        self.placing_score = 0
        self.games_stats = {}  # {"tourney name" : games won, games played}
        self.total_games_won = 0
        self.total_games_played = 0
        self.appearances = {}  # {"tourney name" : number of teams using char}
        self.partners = []  # names of partners added for each appearance

    def record_games(self, tourney_name, games_won, games_played):
        """Adds new entry into games_stats dictionary, where
        the key is the tournament name, and the value is a tuple of games
        won and games played. Also adds input games won and played to
        previous sum of games won and played.
        """
        self.games_stats[tourney_name] = (games_won, games_played)
        self.total_games_won += games_won
        self.total_games_played += games_played

    def update_appearances(self, tourney_name, num_appearances):
        """Adds new entry into appearances dict, where the key is the
        tournament name and the value is the number of times a character
        was included in a team at tournament in question.
        """
        self.appearances[tourney_name] = num_appearances

    def update_score(self, placings):
        """Adds appropriate placing points to placing score according to
        input placing and placing points dictionary.
        """
        for p in placings:
            placing_score = placing_points_dict[p]
            self.placing_score += placing_score

    def add_partners(self, new_partners):
        """Adds new partners to list of known partners.
        """
        self.partners = self.partners + new_partners

    def calc_win_percentage(self):
        """Calculates win percentage of character and returns percentage
        as a float.
        """
        return self.total_games_won / self.total_games_played

    def most_common_partners(self):
        """Tallies up number of occurences of partners in partner list,
        sorts list, and returns the 2 most common partners for character.
        """
        partner_list = []
        ordered_partners = Counter(self.partners)
        for key, value in ordered_partners.items():
            partner_list.append((key, value))
        partner_list.sort(key=lambda x: x[1], reverse=True)
        return partner_list[0][0], partner_list[1][0]


    def __repr__(self):
        return "Name: " + self.name + '\n' +\
                "Placing Score: " + str(self.placing_score) + '\n' +\
                "Win Percentage: " + str(self.calc_win_percentage()) + "%\n" +\
                "Two Most Common Partners: " + \
                    self.most_common_partners()[0] + " and " +\
                    self.most_common_partners()[1]

def main():
    print("Hiya I'm the main function running now...")

if __name__ == "__main__":
    main()
