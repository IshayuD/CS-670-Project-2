from enum import Enum

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

class Room(Enum):
    KITCHEN = "Kitchen"
    BALLROOM = "Ballroom"
    CONSERVATORY = "Conservatory"
    DINING_ROOM = "Dining Room"
    BILLIARD_ROOM = "Billiard Room"
    LIBRARY = "Library"
    LOUNGE = "Lounge"
    HALL = "Hall"
    STUDY = "Study"

# Using an abstract graph where rooms are nodes. Hallways are abstracted away.
# Movement between adjacent rooms costs '1 move'.
BOARD_CONNECTIONS = {
    Room.STUDY: [Room.HALL, Room.LIBRARY],
    Room.HALL: [Room.STUDY, Room.LOUNGE, Room.DINING_ROOM],
    Room.LOUNGE: [Room.HALL, Room.CONSERVATORY],
    Room.LIBRARY: [Room.STUDY, Room.HALL, Room.BILLIARD_ROOM],
    Room.BILLIARD_ROOM: [Room.LIBRARY, Room.DINING_ROOM, Room.BALLROOM],
    Room.DINING_ROOM: [Room.BILLIARD_ROOM, Room.HALL, Room.KITCHEN],
    Room.CONSERVATORY: [Room.LOUNGE, Room.BALLROOM],
    Room.BALLROOM: [Room.CONSERVATORY, Room.BILLIARD_ROOM, Room.KITCHEN],
    Room.KITCHEN: [Room.DINING_ROOM, Room.BALLROOM]
}

SECRET_PASSAGES = {
    Room.STUDY: Room.KITCHEN,
    Room.KITCHEN: Room.STUDY,
    Room.LOUNGE: Room.CONSERVATORY,
    Room.CONSERVATORY: Room.LOUNGE
}

# Simplified starting positions for the text-based game.
# In a physical game, these are on hallway squares.
START_POSITIONS = {
    Character.MISS_SCARLETT: Room.HALL,
    Character.COLONEL_MUSTARD: Room.LOUNGE,
    Character.MRS_WHITE: Room.BALLROOM,
    Character.REVEREND_GREEN: Room.CONSERVATORY,
    Character.MRS_PEACOCK: Room.LIBRARY,
    Character.PROFESSOR_PLUM: Room.STUDY
}

TURN_ORDER = [
    Character.MISS_SCARLETT,
    Character.COLONEL_MUSTARD,
    Character.MRS_WHITE,
    Character.REVEREND_GREEN,
    Character.MRS_PEACOCK,
    Character.PROFESSOR_PLUM,
]