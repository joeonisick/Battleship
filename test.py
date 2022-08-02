import unittest
from unittest import TestCase
from unittest.mock import patch
from unittest import TestCase
from game_functions import build_board, play_again, test_input, ship_hider

"""
def get_input(text):
    return input(text)

def answer():
    ans = get_input('enter yes or no: ')
    if ans == 'yes':
        return 'you entered yes'
    if ans == 'no':
        return 'you entered no'

class Input_tests(TestCase):
    #Tests initial user selections for play and radar
    from game_functions import play_again
    @patch('play_again.get_input', return_value='yes')
    def test_answer_yes(self, input):
        self.assertEqual(answer(), 'you entered yes')
    @patch('play_again.get_input', return_value='no')
    def test_answer_yes(self, input):
        self.assertEqual(answer(), 'you entered no')    
"""

class Battleship_functional_testing(unittest.TestCase):
    """
    #tests the module for verifying user input
    def test_input_validation():
        print()
    """

    #Tests the module for the vaild range of columns and rows 1-10 (index 0-9)
    def test_board_build(self):
        game_options = {"row_height" : int()}
        game_options["column_width"] = int()
        board = []
        test = True
        count = 0
        
        #test column build
        for x in range(2,11):
            game_options["row_height"] = x
            for y in range(2,11):
                if count == 10:
                    count = 0
                game_options["column_width"] = y
                board = build_board(game_options)
                self.assertEqual(board[x-1][y-1], " O ", f"List Item String Failed")
                self.assertEqual(len(board), x, f"Row Creation Test Failed")
                self.assertEqual(len(board[count]), y, f"Column Creation Test Failed")

    def test_random_ship_placement(self):
        game_options = {}
        game_options["define_ships"] = {"carrier":[1,5],"battleship":[2,4],\
            "cruiser":[3,3],"submarine":[4,3],"destroyer":[5,2]}
        game_options["row_height"] = int(10)
        game_options["column_width"] = int(10)
        game_boards = {}
        game_boards["p1_ship_coords"] = {}
        
        for key in game_options["define_ships"]:
            game_boards["p1_ship_coords"][key] = []
            ship_hider(game_boards, game_options, "p1_ship_coords", key)
        self.assertEqual(len(game_boards["p1_ship_coords"]), 5,\
                f"Failed to create 5 ships")
        for key in game_boards["p1_ship_coords"]:
            self.assertEqual(len(game_boards["p1_ship_coords"][key]),\
                 game_options["define_ships"][key][1], \
                    f"Failed to properly size ships")

if __name__ == '__main__':
    unittest.main()