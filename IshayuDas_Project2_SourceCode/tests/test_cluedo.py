# tests/test_cluedo.py

import unittest
from unittest.mock import patch, MagicMock
from cluedo_game.game import Game
from cluedo_game.board import Board
from cluedo_game import constants

class TestGameSetup(unittest.TestCase):
    
    @patch('random.choice')
    def test_solution_creation_and_card_dealing(self, mock_random_choice):
        # Define a fixed sequence of choices for random.choice
        mock_random_choice.side_effect = [
            constants.Character.MISS_SCARLETT,  # Solution character
            constants.Weapon.DAGGER,            # Solution weapon
            constants.Room.LIBRARY              # Solution room
        ]

        # Initialize the game with 3 players
        game = Game(num_players=3)

        # Test Solution
        self.assertIsNotNone(game.solution)
        self.assertEqual(game.solution['character'], constants.Character.MISS_SCARLETT)
        self.assertEqual(game.solution['weapon'], constants.Weapon.DAGGER)
        self.assertEqual(game.solution['room'], constants.Room.LIBRARY)

        # Test Player Creation
        self.assertEqual(len(game.players), 3)
        self.assertEqual(game.players[0].character, constants.Character.MISS_SCARLETT)
        self.assertEqual(game.players[1].character, constants.Character.COLONEL_MUSTARD)

        # Test Card Distribution
        total_cards = len(constants.Character) + len(constants.Weapon) + len(constants.Room)
        num_dealt_cards = sum(len(p.hand) for p in game.players)
        
        self.assertEqual(total_cards - 3, num_dealt_cards)
        
        # In a 3 player game, 18 cards are dealt (6 each)
        self.assertEqual(len(game.players[0].hand), 6)
        self.assertEqual(len(game.players[1].hand), 6)
        self.assertEqual(len(game.players[2].hand), 6)

        # Ensure no player has a solution card
        solution_cards = set(game.solution.values())
        for player in game.players:
            player_hand_set = set(player.hand)
            self.assertTrue(player_hand_set.isdisjoint(solution_cards))

class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.board.initialize_positions()

    def test_initial_positions(self):
        # Check if all characters have a starting position
        self.assertEqual(len(self.board.character_positions), len(constants.Character))
        self.assertEqual(self.board.get_location(constants.Character.PROFESSOR_PLUM), constants.Room.STUDY)

        # Check if all weapons are on the board
        self.assertEqual(len(self.board.weapon_positions), len(constants.Weapon))
        self.assertIn(self.board.get_location(constants.Weapon.CANDLESTICK), list(constants.Room))

    def test_token_movement(self):
        # Move a character
        self.board.move_token(constants.Character.MISS_SCARLETT, constants.Room.LIBRARY)
        self.assertEqual(self.board.get_location(constants.Character.MISS_SCARLETT), constants.Room.LIBRARY)

        # Move a weapon
        self.board.move_token(constants.Weapon.ROPE, constants.Room.BALLROOM)
        self.assertEqual(self.board.get_location(constants.Weapon.ROPE), constants.Room.BALLROOM)

if __name__ == '__main__':
    unittest.main()