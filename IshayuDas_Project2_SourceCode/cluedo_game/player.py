class Player:
    """Represents a human player in the game."""
    def __init__(self, player_name, character_enum):
        self.name = player_name
        self.character = character_enum
        self.hand = []
        self.has_lost = False # Flag for incorrect accusations

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

    def update_knowledge(self, suggestion, refuting_player, shown_card):
        """
        Processes information from a suggestion to help the human player.
        For a human player, this simply prints the outcome.
        """
        if refuting_player:
            if self == refuting_player:
                # This player is the one who showed a card.
                return
            if self == suggestion['suggester']:
                # This player is the one who made the suggestion.
                print(f"INFO: {refuting_player.name} showed you the '{shown_card.value}' card.")
            else:
                # This is a third-party player observing.
                print(f"INFO: {refuting_player.name} refuted the suggestion.")
        else:
            print("INFO: No one could refute the suggestion.")
