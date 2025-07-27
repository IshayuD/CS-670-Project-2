from enum import Enum
import random

class CardType(Enum):
    CHARACTER = "Character"
    WEAPON = "Weapon"
    ROOM = "Room"

class Card:
    def __init__(self, card_type, value):
        self.type = card_type
        self.value = value
    
    def __str__(self):
        return f"{self.value} ({self.type.value})"

class Deck:
    def __init__(self):
        self.cards = []
        self.initialize_deck()
    
    def initialize_deck(self):
        # Add character cards
        from .board import Character
        for character in Character:
            self.cards.append(Card(CardType.CHARACTER, character))
        
        # Add weapon cards
        from .board import Weapon
        for weapon in Weapon:
            self.cards.append(Card(CardType.WEAPON, weapon))
        
        # Add room cards
        from .board import Room
        for room in Room:
            self.cards.append(Card(CardType.ROOM, room))
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal(self, num_players):
        # Remove solution cards first
        solution = {
            CardType.CHARACTER: random.choice([c for c in self.cards if c.type == CardType.CHARACTER]),
            CardType.WEAPON: random.choice([c for c in self.cards if c.type == CardType.WEAPON]),
            CardType.ROOM: random.choice([c for c in self.cards if c.type == CardType.ROOM])
        }
        
        # Remove solution cards from deck
        remaining_cards = [card for card in self.cards 
                          if not (card.type == CardType.CHARACTER and card.value == solution[CardType.CHARACTER].value) and
                          not (card.type == CardType.WEAPON and card.value == solution[CardType.WEAPON].value) and
                          not (card.type == CardType.ROOM and card.value == solution[CardType.ROOM].value)]
        
        # Shuffle remaining cards
        random.shuffle(remaining_cards)
        
        # Distribute cards to players
        player_hands = [[] for _ in range(num_players)]
        for i, card in enumerate(remaining_cards):
            player_hands[i % num_players].append(card)
        
        return solution, player_hands