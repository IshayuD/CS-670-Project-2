import random
from .board import Mansion, Character, Weapon, Room
from .cards import Deck
from .player import Player

class CluedoGame:
    def __init__(self, num_players):
        self.mansion = Mansion()
        self.deck = Deck()
        self.num_players = num_players
        self.players = []
        self.current_player_index = 0
        self.solution = None
        self.game_over = False
        self.initialize_game()
    
    def initialize_game(self):
        # Deal cards and get solution
        self.solution, player_hands = self.deck.deal(self.num_players)
        
        # Create players
        all_characters = list(Character)
        random.shuffle(all_characters)
        
        for i in range(self.num_players):
            character = all_characters[i]
            start_pos = self.mansion.get_character_start_position(character)
            player = Player(character, player_hands[i])
            player.set_position(start_pos)
            self.players.append(player)
    
    def get_current_player(self):
        return self.players[self.current_player_index]
    
    def next_turn(self):
        self.current_player_index = (self.current_player_index + 1) % self.num_players
    
    def roll_dice(self):
        return random.randint(1, 6)
    
    def move_player(self, player, direction, steps):
        x, y = player.position
        if direction == "UP":
            new_pos = (x - steps, y)
        elif direction == "DOWN":
            new_pos = (x + steps, y)
        elif direction == "LEFT":
            new_pos = (x, y - steps)
        elif direction == "RIGHT":
            new_pos = (x, y + steps)
        else:
            return False
        
        # Check if new position is valid (not out of bounds)
        if 0 <= new_pos[0] <= 2 and 0 <= new_pos[1] <= 5:
            player.set_position(new_pos)
            # Check if player entered a room
            for room, data in self.mansion.rooms.items():
                if data["position"] == new_pos:
                    player.set_current_room(room)
                    return True
            player.set_current_room(None)
            return True
        return False
    
    def use_secret_passage(self, player):
        if player.current_room and self.mansion.has_secret_passage(player.current_room):
            destination = self.mansion.get_secret_passage(player.current_room)
            player.set_current_room(destination)
            player.set_position(self.mansion.get_room_position(destination))
            return True
        return False
    
    def make_suggestion(self, player, character, weapon):
        if not player.current_room:
            return False
        
        suggestion = {
            "character": character,
            "weapon": weapon,
            "room": player.current_room
        }
        
        # Move suggested character to the room (if not already there)
        for p in self.players:
            if p.character == character and p.current_room != player.current_room:
                p.set_current_room(player.current_room)
                p.set_position(self.mansion.get_room_position(player.current_room))
                break
        
        # Move suggested weapon to the room
        self.mansion.move_weapon(weapon, player.current_room)
        
        # Check for refutations
        refutation = self.check_refutations(player, suggestion)
        
        return suggestion, refutation
    
    def check_refutations(self, suggesting_player, suggestion):
        # Check players in order (starting next player) for refutations
        start_index = (self.players.index(suggesting_player) + 1) % self.num_players
        for i in range(self.num_players):
            player_index = (start_index + i) % self.num_players
            player = self.players[player_index]
            refutation_card = player.can_refute(suggestion)
            if refutation_card:
                return {
                    "player": player,
                    "card": refutation_card
                }
        return None
    
    def make_accusation(self, player, character, weapon, room):
        if (character == self.solution[CardType.CHARACTER].value and
            weapon == self.solution[CardType.WEAPON].value and
            room == self.solution[CardType.ROOM].value):
            self.game_over = True
            return True
        else:
            # Player made wrong accusation and is out of the game
            self.players.remove(player)
            self.num_players -= 1
            if self.current_player_index >= self.num_players:
                self.current_player_index = 0
            return False