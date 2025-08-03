class Player:
    """A player in the game."""
    def __init__(self, player_name, character_enum):
        self.name = player_name
        self.character = character_enum
        self.hand = []

    def add_card_to_hand(self, card):
        """Adds a card to the player's hand."""
        self.hand.append(card)

    def display_hand(self):
        """Prints the player's cards to the console."""
        print(f"\n{self.name}'s Hand ({self.character.value}):")
        if not self.hand:
            print("  No cards.")
            return
        
        sorted_hand = sorted(self.hand, key=lambda card: card.__class__.__name__)
        for card in sorted_hand:
            print(f"  - {card.value}")