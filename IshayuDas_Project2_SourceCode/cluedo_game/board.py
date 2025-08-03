from . import constants
import random

class Board:
    """Manages the state of the game board, including token positions."""
    def __init__(self):
        self.character_positions = {}
        self.weapon_positions = {}

    def initialize_positions(self):
        """Sets the starting positions for all characters and weapons."""
        # Set character starting positions
        for character, room in constants.START_POSITIONS.items():
            self.character_positions[character] = room
        
        # Place weapons randomly in rooms
        rooms = list(constants.Room)
        random.shuffle(rooms)
        for i, weapon in enumerate(constants.Weapon):
            self.weapon_positions[weapon] = rooms[i]

    def move_token(self, token, new_location_enum):
        """Moves a character or weapon to a new room."""
        if isinstance(token, constants.Character):
            self.character_positions[token] = new_location_enum
            print(f"INFO: {token.value}'s token has been moved to the {new_location_enum.value}.")
        elif isinstance(token, constants.Weapon):
            self.weapon_positions[token] = new_location_enum
            print(f"INFO: The {token.value} token has been moved to the {new_location_enum.value}.")

    def get_location(self, token):
        """Gets the current location of a character or weapon."""
        if isinstance(token, constants.Character):
            return self.character_positions.get(token)
        elif isinstance(token, constants.Weapon):
            return self.weapon_positions.get(token)
        return None