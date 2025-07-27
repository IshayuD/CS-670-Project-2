import random
from enum import Enum

class Room(Enum):
    HALL = "Hall"
    LOUNGE = "Lounge"
    DINING_ROOM = "Dining Room"
    KITCHEN = "Kitchen"
    BALLROOM = "Ballroom"
    CONSERVATORY = "Conservatory"
    BILLIARD_ROOM = "Billiard Room"
    LIBRARY = "Library"
    STUDY = "Study"

class Character(Enum):
    MISS_SCARLETT = "Miss Scarlett"
    COLONEL_MUSTARD = "Colonel Mustard"
    MRS_WHITE = "Mrs. White"
    REVEREND_GREEN = "Reverend Green"
    MRS_PEACOCK = "Mrs. Peacock"
    PROFESSOR_PLUM = "Professor Plum"

class Weapon(Enum):
    CANDLESTICK = "Candlestick"
    DAGGER = "Dagger"
    LEAD_PIPE = "Lead Pipe"
    REVOLVER = "Revolver"
    ROPE = "Rope"
    WRENCH = "Wrench"

class Mansion:
    def __init__(self):
        self.rooms = {
            Room.HALL: {"position": (1, 1), "adjacent": [Room.LOUNGE, Room.DINING_ROOM, Room.STUDY], "secret_passage": None},
            Room.LOUNGE: {"position": (0, 1), "adjacent": [Room.HALL, Room.DINING_ROOM], "secret_passage": Room.CONSERVATORY},
            Room.DINING_ROOM: {"position": (1, 2), "adjacent": [Room.HALL, Room.LOUNGE, Room.KITCHEN, Room.BILLIARD_ROOM], "secret_passage": None},
            Room.KITCHEN: {"position": (0, 3), "adjacent": [Room.DINING_ROOM, Room.BALLROOM], "secret_passage": Room.STUDY},
            Room.BALLROOM: {"position": (1, 4), "adjacent": [Room.KITCHEN, Room.CONSERVATORY, Room.BILLIARD_ROOM], "secret_passage": None},
            Room.CONSERVATORY: {"position": (0, 5), "adjacent": [Room.BALLROOM, Room.LIBRARY], "secret_passage": Room.LOUNGE},
            Room.BILLIARD_ROOM: {"position": (2, 3), "adjacent": [Room.DINING_ROOM, Room.BALLROOM, Room.LIBRARY, Room.STUDY], "secret_passage": None},
            Room.LIBRARY: {"position": (2, 4), "adjacent": [Room.BILLIARD_ROOM, Room.CONSERVATORY, Room.STUDY], "secret_passage": None},
            Room.STUDY: {"position": (2, 1), "adjacent": [Room.HALL, Room.BILLIARD_ROOM, Room.LIBRARY], "secret_passage": Room.KITCHEN}
        }
        
        self.character_start_positions = {
            Character.MISS_SCARLETT: (0, 0),
            Character.COLONEL_MUSTARD: (0, 2),
            Character.MRS_WHITE: (0, 4),
            Character.REVEREND_GREEN: (2, 0),
            Character.MRS_PEACOCK: (2, 2),
            Character.PROFESSOR_PLUM: (2, 5)
        }
        
        self.weapon_positions = {
            Weapon.CANDLESTICK: Room.LOUNGE,
            Weapon.DAGGER: Room.STUDY,
            Weapon.LEAD_PIPE: Room.KITCHEN,
            Weapon.REVOLVER: Room.BALLROOM,
            Weapon.ROPE: Room.CONSERVATORY,
            Weapon.WRENCH: Room.BILLIARD_ROOM
        }
    
    def get_adjacent_rooms(self, room):
        return self.rooms[room]["adjacent"]
    
    def has_secret_passage(self, room):
        return self.rooms[room]["secret_passage"] is not None
    
    def get_secret_passage(self, room):
        return self.rooms[room]["secret_passage"]
    
    def get_room_position(self, room):
        return self.rooms[room]["position"]
    
    def get_character_start_position(self, character):
        return self.character_start_positions[character]
    
    def get_weapon_position(self, weapon):
        return self.weapon_positions[weapon]
    
    def move_weapon(self, weapon, room):
        self.weapon_positions[weapon] = room