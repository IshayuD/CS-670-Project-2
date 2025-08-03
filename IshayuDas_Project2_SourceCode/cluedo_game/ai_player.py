# cluedo_game/ai_player.py

import random
from .player import Player
from . import constants

class ClueSheet:
    """Represents the AI's knowledge base and deduction engine."""
    def __init__(self, my_cards):
        self.my_cards = set(my_cards)
        
        # Initialize all possibilities
        self.possible_characters = set(constants.Character)
        self.possible_weapons = set(constants.Weapon)
        self.possible_rooms = set(constants.Room)

        # A dictionary to track who holds which card: {card_enum: player_object}
        self.known_card_owners = {}

        # Remove my own cards from the possibilities
        for card in self.my_cards:
            self.eliminate(card, self)

    def eliminate(self, card, owner):
        """Eliminates a card from possibilities and records its owner."""
        self.known_card_owners[card] = owner
        if isinstance(card, constants.Character):
            self.possible_characters.discard(card)
        elif isinstance(card, constants.Weapon):
            self.possible_weapons.discard(card)
        elif isinstance(card, constants.Room):
            self.possible_rooms.discard(card)

    def process_suggestion(self, suggestion, refuting_player, shown_card):
        """Updates knowledge based on the outcome of a suggestion."""
        suggester = suggestion['suggester']
        suggested_cards = {suggestion['character'], suggestion['weapon'], suggestion['room']}

        if shown_card:
            # A card was shown to the suggester.
            # If I am the suggester, I know the exact card.
            if suggester == self:
                print(f"AI LOGIC: I was shown '{shown_card.value}' by {refuting_player.name}. Eliminating it.")
                self.eliminate(shown_card, refuting_player)
        
        elif refuting_player:
            # I am not the suggester, but I know someone refuted.
            # I know the refuter has one of the three cards.
            # This is complex to model perfectly without more info, but we can note it.
            print(f"AI LOGIC: {refuting_player.name} refuted. They have one of { {c.value for c in suggested_cards} }.")
            # A more advanced AI could track these "OR" conditions.

        else:
            # No one refuted the suggestion.
            # This means NO ONE (except the suggester) has any of those cards.
            # Therefore, any of these cards still in my 'possibilities' list are now stronger candidates for the solution.
            print(f"AI LOGIC: No one refuted the suggestion. The solution might contain one of these cards.")
            # An advanced AI could increase a "confidence score" for these cards.

    def can_accuse(self):
        """Checks if the AI has deduced the solution. Returns solution tuple or None."""
        if len(self.possible_characters) == 1 and \
           len(self.possible_weapons) == 1 and \
           len(self.possible_rooms) == 1:
            return {
                "character": list(self.possible_characters)[0],
                "weapon": list(self.possible_weapons)[0],
                "room": list(self.possible_rooms)[0]
            }
        return None

    def get_suggestion(self, current_room):
        """Generates a strategic suggestion."""
        # The room is fixed by the AI's location
        suggestion_room = current_room

        # Try to suggest a character and weapon that are still possibilities
        try:
            suggestion_char = random.choice(list(self.possible_characters))
            suggestion_weapon = random.choice(list(self.possible_weapons))
        except IndexError:
            # This happens if we've solved a category but can't accuse yet.
            # Fallback to any unknown card.
            all_unknowns = (set(constants.Character) | set(constants.Weapon)) - set(self.known_card_owners.keys())
            if not all_unknowns: return None # Should not happen in a real game
            
            fallback_card = random.choice(list(all_unknowns))
            if isinstance(fallback_card, constants.Character):
                suggestion_char = fallback_card
                suggestion_weapon = random.choice(list(self.possible_weapons) or list(constants.Weapon))
            else:
                suggestion_weapon = fallback_card
                suggestion_char = random.choice(list(self.possible_characters) or list(constants.Character))

        return {
            "character": suggestion_char,
            "weapon": suggestion_weapon,
            "room": suggestion_room
        }


class AIPlayer(Player):
    """Represents a computer-controlled player."""
    def __init__(self, player_name, character_enum):
        super().__init__(player_name, character_enum)
        self.is_ai = True
        self.clue_sheet = None # Will be initialized after cards are dealt

    def initialize_ai(self):
        """Initializes the AI's brain after it has received its cards."""
        self.clue_sheet = ClueSheet(self.hand)
        print(f"AI player {self.name} initialized with {len(self.hand)} cards.")

    def update_knowledge(self, suggestion, refuting_player, shown_card):
        """Processes new information and updates the clue sheet."""
        self.clue_sheet.process_suggestion(suggestion, refuting_player, shown_card)

    def choose_card_to_show(self, suggested_cards):
        """Decides which card to show when refuting a suggestion."""
        my_matching_cards = [card for card in self.hand if card in suggested_cards]
        if my_matching_cards:
            # Simple strategy: just show the first matching card found.
            # A smarter AI might choose to show a card it thinks others already know about.
            return my_matching_cards[0]
        return None

    def decide_move(self, current_location):
        """Decides where to move based on unknown rooms."""
        possible_destinations = list(constants.BOARD_CONNECTIONS.get(current_location, []))
        
        # Prioritize moving to a room that is still a possibility
        unknown_rooms = self.clue_sheet.possible_rooms
        strategic_moves = [dest for dest in possible_destinations if dest in unknown_rooms]

        if current_location in constants.SECRET_PASSAGES:
            passage_dest = constants.SECRET_PASSAGES[current_location]
            # If the secret passage leads to an unknown room, it's a good move.
            if passage_dest in unknown_rooms:
                print(f"AI DECISION: Taking secret passage to {passage_dest.value} (strategic).")
                return passage_dest
        
        if strategic_moves:
            destination = random.choice(strategic_moves)
            print(f"AI DECISION: Moving to {destination.value} (strategic).")
            return destination
        elif possible_destinations:
            # If no strategic moves, just move to any valid adjacent room.
            destination = random.choice(possible_destinations)
            print(f"AI DECISION: Moving to {destination.value} (random).")
            return destination
        
        # No possible moves
        return None
