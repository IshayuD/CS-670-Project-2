# cluedo_game/game.py

import random
import time
from . import constants
from .board import Board
from .player import Player
from .ai_player import AIPlayer

class Game:
    """Orchestrates the entire Cluedo game with human and AI players."""
    def __init__(self, total_players, num_ai):
        self.num_players = total_players
        self.num_ai = num_ai
        self.players = []
        self.board = Board()
        self.solution = None
        self.current_turn_index = 0
        self._setup_game()

    def _setup_game(self):
        """Initializes the game state, creates players, solution, and deals cards."""
        # 1. Create Solution
        self.solution = {
            "character": random.choice(list(constants.Character)),
            "weapon": random.choice(list(constants.Weapon)),
            "room": random.choice(list(constants.Room))
        }

        # 2. Create Deck
        deck = list(constants.Character) + list(constants.Weapon) + list(constants.Room)
        deck.remove(self.solution["character"])
        deck.remove(self.solution["weapon"])
        deck.remove(self.solution["room"])
        random.shuffle(deck)

        # 3. Create Players (Human and AI)
        player_characters = constants.TURN_ORDER[:self.num_players]
        ai_indices = random.sample(range(self.num_players), self.num_ai)
        
        for i, char_enum in enumerate(player_characters):
            if i in ai_indices:
                player = AIPlayer(f"AI Player ({char_enum.value})", char_enum)
            else:
                player = Player(f"Player {i+1} ({char_enum.value})", char_enum)
            self.players.append(player)

        # 4. Deal Cards
        card_index = 0
        while card_index < len(deck):
            for player in self.players:
                if card_index < len(deck):
                    player.add_card_to_hand(deck[card_index])
                    card_index += 1
        
        # 5. Initialize AI players with their clue sheets
        for player in self.players:
            if isinstance(player, AIPlayer):
                player.initialize_ai()
        
        # 6. Initialize Board
        self.board.initialize_positions()

    def run(self):
        """Starts and runs the main game loop."""
        print("\n--- Game Setup Complete ---")
        # In Part 2, the solution is hidden from the players.
        # print(f"DEBUG: The solution is {self.solution['character'].value}, {self.solution['weapon'].value}, {self.solution['room'].value}.")
        for player in self.players:
            if not isinstance(player, AIPlayer):
                player.display_hand()
            
        game_over = False
        winner = None
        while not game_over:
            winner, game_over = self.take_turn()
            if all(p.has_lost for p in self.players):
                print("\nAll players have made an incorrect accusation! The house wins.")
                game_over = True

        print("\n" + "="*40)
        print("--- GAME OVER ---")
        if winner:
            print(f"🎉 {winner.name} wins the game! 🎉")
        print(f"The correct solution was: {self.solution['character'].value}, with the {self.solution['weapon'].value}, in the {self.solution['room'].value}.")
        print("="*40)

    def take_turn(self):
        """Manages a single player's turn, returning winner and game_over status."""
        current_player = self.players[self.current_turn_index]
        
        print("\n" + "="*40)
        print(f"--- {current_player.name}'s Turn ---")

        if current_player.has_lost:
            print("You have made an incorrect accusation and cannot take any more actions.")
            self.current_turn_index = (self.current_turn_index + 1) % self.num_players
            return None, False

        # Accusation or Move
        if isinstance(current_player, AIPlayer):
            time.sleep(1) # Simulate thinking
            accusation = current_player.clue_sheet.can_accuse()
            if accusation:
                print("AI is making an accusation!")
                return self.handle_accusation(current_player, accusation)
        else:
            action = input("Do you want to (m)ove or make an (a)ccusation? ").lower()
            if action == 'a':
                return self.handle_accusation(current_player)

        # Movement
        current_location = self.board.get_location(current_player.character)
        print(f"You are currently in the {current_location.value}.")
        self.handle_movement(current_player, current_location)
        
        # Suggestion
        new_location = self.board.get_location(current_player.character)
        if new_location in constants.BOARD_CONNECTIONS:
            self.handle_suggestion(current_player, new_location)
        
        self.current_turn_index = (self.current_turn_index + 1) % self.num_players
        return None, False

    def handle_movement(self, player, location):
        """Handles the movement part of a turn."""
        destination = None
        if isinstance(player, AIPlayer):
            time.sleep(1)
            destination = player.decide_move(location)
        else:
            input("\nPress Enter to roll the die...")
            roll = random.randint(1, 6)
            print(f"You rolled a {roll}!")
            
            possible_moves = list(constants.BOARD_CONNECTIONS.get(location, []))
            if location in constants.SECRET_PASSAGES:
                passage_dest = constants.SECRET_PASSAGES[location]
                choice = input(f"You can use a secret passage to the {passage_dest.value}. Use it? (y/n): ").lower()
                if choice == 'y':
                    destination = passage_dest
            
            if not destination:
                print("You can move to the following rooms:")
                for i, move in enumerate(possible_moves):
                    print(f"  {i+1}: {move.value}")
                
                if not possible_moves:
                    print("No available moves from here.")
                    return
                
                while True:
                    try:
                        move_choice = int(input("Enter the number of your destination: "))
                        if 1 <= move_choice <= len(possible_moves):
                            destination = possible_moves[move_choice - 1]
                            break
                    except (ValueError, IndexError):
                        print("Invalid choice.")
        
        if destination:
            self.board.move_token(player.character, destination)

    def handle_suggestion(self, suggester, room):
        """Manages the full suggestion and refutation process."""
        suggestion = {}
        if isinstance(suggester, AIPlayer):
            print("AI is making a suggestion...")
            time.sleep(1)
            suggestion = suggester.clue_sheet.get_suggestion(room)
        else:
            print(f"\nYou are in the {room.value}. Make a suggestion.")
            # Get Character Suggestion
            chars = list(constants.Character)
            for i, char in enumerate(chars): print(f"  {i+1}: {char.value}")
            while 'character' not in suggestion:
                try: suggestion['character'] = chars[int(input("Suspect: ")) - 1]
                except (ValueError, IndexError): print("Invalid.")
            # Get Weapon Suggestion
            weapons = list(constants.Weapon)
            for i, w in enumerate(weapons): print(f"  {i+1}: {w.value}")
            while 'weapon' not in suggestion:
                try: suggestion['weapon'] = weapons[int(input("Weapon: ")) - 1]
                except (ValueError, IndexError): print("Invalid.")
            suggestion['room'] = room
        
        suggestion['suggester'] = suggester
        print(f"\n--- Suggestion: {suggester.name} suggests it was {suggestion['character'].value} with the {suggestion['weapon'].value} in the {suggestion['room'].value}. ---")

        self.board.move_token(suggestion['character'], room)
        self.board.move_token(suggestion['weapon'], room)

        # Refutation Process
        refuting_player, shown_card = self.process_refutations(suggestion)

        # Update all players' knowledge
        for p in self.players:
            p.update_knowledge(suggestion, refuting_player, shown_card if p == suggester else None)

    def process_refutations(self, suggestion):
        """Cycles through players to find one who can refute."""
        suggester_idx = self.players.index(suggestion['suggester'])
        suggested_cards = {suggestion['character'], suggestion['weapon'], suggestion['room']}

        for i in range(1, self.num_players):
            player_to_check_idx = (suggester_idx + i) % self.num_players
            player_to_check = self.players[player_to_check_idx]

            if player_to_check.has_lost: continue # Skip lost players

            matching_cards = [card for card in player_to_check.hand if card in suggested_cards]
            if matching_cards:
                print(f"\n{player_to_check.name} can refute the suggestion.")
                shown_card = None
                if isinstance(player_to_check, AIPlayer):
                    time.sleep(1)
                    shown_card = player_to_check.choose_card_to_show(suggested_cards)
                    print(f"AI ({player_to_check.name}) has privately shown a card to {suggestion['suggester'].name}.")
                else:
                    if len(matching_cards) == 1:
                        shown_card = matching_cards[0]
                        print(f"You only have one matching card ({shown_card.value}), so you show it.")
                    else:
                        print("Which card do you want to show?")
                        for j, card in enumerate(matching_cards): print(f"  {j+1}: {card.value}")
                        while not shown_card:
                            try: shown_card = matching_cards[int(input("Card to show: ")) - 1]
                            except (ValueError, IndexError): print("Invalid.")
                return player_to_check, shown_card
        
        return None, None # No one could refute

    def handle_accusation(self, accuser, ai_accusation=None):
        """Manages a player's final accusation."""
        accusation = {}
        if ai_accusation:
            accusation = ai_accusation
        else:
            print("\nYou are making a final accusation! If you are wrong, you lose.")
            # Get Character Accusation
            chars = list(constants.Character)
            for i, char in enumerate(chars): print(f"  {i+1}: {char.value}")
            while 'character' not in accusation:
                try: accusation['character'] = chars[int(input("Accused Character: ")) - 1]
                except (ValueError, IndexError): print("Invalid.")
            # Get Weapon Accusation
            weapons = list(constants.Weapon)
            for i, w in enumerate(weapons): print(f"  {i+1}: {w.value}")
            while 'weapon' not in accusation:
                try: accusation['weapon'] = weapons[int(input("Accused Weapon: ")) - 1]
                except (ValueError, IndexError): print("Invalid.")
            # Get Room Accusation
            rooms = list(constants.Room)
            for i, r in enumerate(rooms): print(f"  {i+1}: {r.value}")
            while 'room' not in accusation:
                try: accusation['room'] = rooms[int(input("Accused Room: ")) - 1]
                except (ValueError, IndexError): print("Invalid.")

        print(f"\n--- ACCUSATION: {accuser.name} accuses {accusation['character'].value}, with the {accusation['weapon'].value}, in the {accusation['room'].value}! ---")
        
        is_correct = (accusation['character'] == self.solution['character'] and
                      accusation['weapon'] == self.solution['weapon'] and
                      accusation['room'] == self.solution['room'])

        if is_correct:
            return accuser, True # Winner, game_over
        else:
            print("\nThat is incorrect! You can no longer make moves, but you must still refute suggestions.")
            accuser.has_lost = True
            return None, False # No winner, game not over
