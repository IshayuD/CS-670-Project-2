from .board import Character

class Player:
    def __init__(self, character, cards):
        self.character = character
        self.cards = cards
        self.position = None
        self.current_room = None
    
    def set_position(self, position):
        self.position = position
    
    def set_current_room(self, room):
        self.current_room = room
    
    def can_refute(self, suggestion):
        """Check if player can refute a suggestion with their cards"""
        for card in self.cards:
            if (card.type == "Character" and card.value == suggestion["character"]) or \
               (card.type == "Weapon" and card.value == suggestion["weapon"]) or \
               (card.type == "Room" and card.value == suggestion["room"]):
                return card
        return None
    
    def __str__(self):
        return f"{self.character.value} (Cards: {len(self.cards)})"