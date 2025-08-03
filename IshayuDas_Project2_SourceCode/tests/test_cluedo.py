import unittest
from unittest.mock import patch, MagicMock
from cluedo_game.game import Game
from cluedo_game.board import Board
from cluedo_game.ai_player import AIPlayer, ClueSheet
from cluedo_game import constants

class TestGameMechanics(unittest.TestCase):

    def setUp(self):
        """Set up a predictable game state for testing."""
        # Patch random to control outcomes
        patcher = patch('random.choice')
        self.addCleanup(patcher.stop)
        self.mock_random_choice = patcher.start()

        # Define a fixed sequence of choices for a predictable solution
        self.mock_random_choice.side_effect = [
            constants.Character.MISS_SCARLETT,  # Solution character
            constants.Weapon.DAGGER,            # Solution weapon
            constants.Room.LIBRARY              # Solution room
        ]
        
        # Initialize a game with 1 human and 1 AI player
        self.game = Game(total_players=2, num_ai=1)
        self.human_player = self.game.players[0]
        self.ai_player = self.game.players[1]
        
        # Ensure the AI player is correctly identified
        if not isinstance(self.ai_player, AIPlayer):
            self.human_player, self.ai_player = self.ai_player, self.human_player

    def test_accusation_correct(self):
        """Test if a correct accusation wins the game."""
        correct_accusation = {
            "character": constants.Character.MISS_SCARLETT,
            "weapon": constants.Weapon.DAGGER,
            "room": constants.Room.LIBRARY
        }
        winner, game_over = self.game.handle_accusation(self.human_player, correct_accusation)
        self.assertTrue(game_over)
        self.assertEqual(winner, self.human_player)

    def test_accusation_incorrect(self):
        """Test if an incorrect accusation makes a player lose."""
        incorrect_accusation = {
            "character": constants.Character.PROFESSOR_PLUM,
            "weapon": constants.Weapon.WRENCH,
            "room": constants.Room.STUDY
        }
        winner, game_over = self.game.handle_accusation(self.human_player, incorrect_accusation)
        self.assertFalse(game_over)
        self.assertIsNone(winner)
        self.assertTrue(self.human_player.has_lost)

    def test_refutation_cycle(self):
        """Test that the correct player refutes a suggestion."""
        # Let's give the AI a specific card to test refutation
        card_to_find = constants.Character.COLONEL_MUSTARD
        self.ai_player.hand = [card_to_find]

        suggestion = {
            "suggester": self.human_player,
            "character": card_to_find,
            "weapon": constants.Weapon.ROPE,
            "room": constants.Room.HALL
        }

        refuting_player, shown_card = self.game.process_refutations(suggestion)

        self.assertIsNotNone(refuting_player, "A refutation should have occurred.")
        self.assertEqual(refuting_player, self.ai_player)
        self.assertEqual(shown_card, card_to_find)


class TestAIPlayerLogic(unittest.TestCase):

    def setUp(self):
        """Set up an AI player with a known hand."""
        self.ai_hand = [
            constants.Character.MRS_WHITE,
            constants.Weapon.CANDLESTICK,
            constants.Room.BALLROOM
        ]
        self.ai_player = AIPlayer("Test AI", constants.Character.PROFESSOR_PLUM)
        for card in self.ai_hand:
            self.ai_player.add_card_to_hand(card)
        self.ai_player.initialize_ai()
        self.clue_sheet = self.ai_player.clue_sheet

    def test_ai_can_accuse(self):
        """Test the AI's ability to know when it has solved the murder."""
        # Initially, the AI should not be able to accuse.
        self.assertIsNone(self.clue_sheet.can_accuse())

        # Manually eliminate all but one possibility for each category.
        solution_char = list(self.clue_sheet.possible_characters)[0]
        solution_weapon = list(self.clue_sheet.possible_weapons)[0]
        solution_room = list(self.clue_sheet.possible_rooms)[0]

        for char in list(constants.Character):
            if char not in self.ai_hand and char != solution_char:
                self.clue_sheet.eliminate(char, owner=MagicMock())
        
        for weapon in list(constants.Weapon):
            if weapon not in self.ai_hand and weapon != solution_weapon:
                self.clue_sheet.eliminate(weapon, owner=MagicMock())

        for room in list(constants.Room):
            if room not in self.ai_hand and room != solution_room:
                self.clue_sheet.eliminate(room, owner=MagicMock())
        
        # Now the AI should be able to make a correct accusation.
        accusation = self.clue_sheet.can_accuse()
        self.assertIsNotNone(accusation)
        self.assertEqual(accusation['character'], solution_char)
        self.assertEqual(accusation['weapon'], solution_weapon)
        self.assertEqual(accusation['room'], solution_room)

if __name__ == '__main__':
    unittest.main()