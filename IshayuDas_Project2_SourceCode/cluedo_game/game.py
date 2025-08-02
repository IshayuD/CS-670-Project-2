# cluedo_game/game.py

import random
from . import constants
from .board import Board
from .player import Player

class Game:
    """Orchestrates the entire Cluedo game."""
    def __init__(self, num_players):
        self.num_players = num_players
        self.players = []
        self.board = Board()
        self.solution = None
        self.current_turn_index = 0
        self._setup_game()

    def _setup_game(self):
        """Initializes the game state, creates the solution, and deals cards."""
        # 1. Create Solution
        all_chars = list(constants.Character)
        all_weapons = list(constants.Weapon)
        all_rooms = list(constants.Room)
        
        self.solution = {
            "character": random.choice(all_chars),
            "weapon": random.choice(all_weapons),
            "room": random.choice(all_rooms)
        }

        # 2. Create Deck
        deck = all_chars + all_weapons + all_rooms
        deck.remove(self.solution["character"])
        deck.remove(self.solution["weapon"])
        deck.remove(self.solution["room"])
        random.shuffle(deck)

        # 3. Create Players
        player_characters = constants.TURN_ORDER[:self.num_players]
        for i, char_enum in enumerate(player_characters):
            player = Player(f"Player {i+1}", char_enum)
            self.players.append(player)

        # 4. Deal Cards
        card_index = 0
        while card_index < len(deck):
            for player in self.players:
                if card_index < len(deck):
                    player.add_card_to_hand(deck[card_index])
                    card_index += 1
        
        # 5. Initialize Board
        self.board.initialize_positions()

    def run(self):
        """Starts and runs the main game loop."""
        print("\n--- Game Setup Complete ---")
        # For Part 1, we can show the solution for easier testing.
        print(f"DEBUG: The solution is {self.solution['character'].value}, {self.solution['weapon'].value}, {self.solution['room'].value}.")
        for player in self.players:
            player.display_hand()
            
        game_over = False
        while not game_over:
            self.take_turn()
            # For Part 1, the game loop runs indefinitely until stopped manually.
            # A full implementation would check for a correct accusation to set game_over = True.

    def take_turn(self):
        """Manages a single player's turn."""
        current_player = self.players[self.current_turn_index]
        current_location = self.board.get_location(current_player.character)
        
        print("\n" + "="*40)
        print(f"--- {current_player.name}'s Turn ({current_player.character.value}) ---")
        print(f"You are currently in the {current_location.value}.")
        
        self.handle_movement(current_player, current_location)
        
        new_location = self.board.get_location(current_player.character)
        if new_location in constants.BOARD_CONNECTIONS: # Check if in a room (not a hallway start)
            self.handle_suggestion(current_player, new_location)
        
        self.current_turn_index = (self.current_turn_index + 1) % self.num_players

    def handle_movement(self, player, location):
        """Handles the dice roll and movement part of a turn."""
        input("\nPress Enter to roll the die...")
        roll = random.randint(1, 6)
        print(f"You rolled a {roll}!")

        possible_moves = list(constants.BOARD_CONNECTIONS.get(location, []))
        use_secret_passage = False
        if location in constants.SECRET_PASSAGES:
            passage_dest = constants.SECRET_PASSAGES[location]
            possible_moves.append(passage_dest)
            
            choice = input(f"You can use a secret passage to the {passage_dest.value}. Use it? (y/n): ").lower()
            if choice == 'y':
                use_secret_passage = True
                self.board.move_token(player.character, passage_dest)
                return

        if not use_secret_passage:
            # Simplified movement: any roll lets you move to an adjacent room.
            print("You can move to the following rooms:")
            for i, move in enumerate(possible_moves):
                print(f"  {i+1}: {move.value}")
            
            if not possible_moves:
                print("You are in a corner room with no standard exits. Your turn continues.")
                return

            while True:
                try:
                    move_choice = int(input("Enter the number of your destination: "))
                    if 1 <= move_choice <= len(possible_moves):
                        destination = possible_moves[move_choice - 1]
                        self.board.move_token(player.character, destination)
                        break
                    else:
                        print("Invalid choice.")
                except ValueError:
                    print("Please enter a valid number.")

    def handle_suggestion(self, player, room):
        """Handles the suggestion part of a turn."""
        print(f"\nYou have entered the {room.value}. You must make a suggestion.")
        
        # Get Character Suggestion
        print("\nWhich character do you suspect?")
        chars = list(constants.Character)
        for i, char in enumerate(chars):
            print(f"  {i+1}: {char.value}")
        while True:
            try:
                choice = int(input("Enter number: ")) - 1
                if 0 <= choice < len(chars):
                    suggested_char = chars[choice]
                    break
            except (ValueError, IndexError):
                print("Invalid input.")
        
        # Get Weapon Suggestion
        print("\nWith which weapon?")
        weapons = list(constants.Weapon)
        for i, weapon in enumerate(weapons):
            print(f"  {i+1}: {weapon.value}")
        while True:
            try:
                choice = int(input("Enter number: ")) - 1
                if 0 <= choice < len(weapons):
                    suggested_weapon = weapons[choice]
                    break
            except (ValueError, IndexError):
                print("Invalid input.")
        
        print("\n--- Suggestion Made ---")
        print(f"{player.character.value} suggests it was {suggested_char.value} with the {suggested_weapon.value} in the {room.value}.")
        
        # Move the suggested character and weapon to the current room
        self.board.move_token(suggested_char, room)
        self.board.move_token(suggested_weapon, room)

        # Refutation logic would follow here, where other players check their hands.
        # For Part 1, making the suggestion and moving the tokens is sufficient.
        print("-----------------------")