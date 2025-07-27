from cluedo_game.game import CluedoGame
from cluedo_game.utils import display_board
from cluedo_game.board import Character, Weapon, Room
import sys

def main():
    print("Welcome to Cluedo Game!")
    
    # Get number of players
    while True:
        try:
            num_players = int(input("Enter number of players (3-6): "))
            if 3 <= num_players <= 6:
                break
            print("Please enter a number between 3 and 6.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Initialize game
    game = CluedoGame(num_players)
    
    # Main game loop
    while not game.game_over and game.num_players > 0:
        current_player = game.get_current_player()
        
        print("\n" + "="*50)
        print(f"{current_player.character.value}'s turn")
        print(f"Current position: {current_player.position}")
        if current_player.current_room:
            print(f"Current room: {current_player.current_room.value}")
        
        display_board(game.mansion, game.players)
        
        # Roll dice
        input("Press Enter to roll the dice...")
        roll = game.roll_dice()
        print(f"You rolled a {roll}!")
        
        # Movement phase
        moves_remaining = roll
        while moves_remaining > 0:
            print(f"\nMoves remaining: {moves_remaining}")
            
            if current_player.current_room:
                # In a room - must exit first
                print("You're in a room. You must exit before moving.")
                exit_roll = game.roll_dice()
                print(f"You need to roll to exit. You rolled: {exit_roll}")
                if exit_roll <= moves_remaining:
                    print("You successfully exited the room!")
                    current_player.set_current_room(None)
                    moves_remaining -= exit_roll
                    continue
                else:
                    print("You didn't roll high enough to exit. Your turn ends.")
                    break
            
            # Get movement input
            print("Possible directions: UP, DOWN, LEFT, RIGHT")
            print("Or type SECRET to use secret passage (if in a room with one)")
            move_input = input("Enter your move (e.g., UP 2) or SECRET: ").strip().upper()
            
            if move_input == "SECRET":
                if game.use_secret_passage(current_player):
                    print(f"You used the secret passage to {current_player.current_room.value}!")
                    break
                else:
                    print("No secret passage available here.")
                    continue
            
            try:
                direction, steps = move_input.split()
                steps = int(steps)
                if steps > moves_remaining:
                    print(f"You can't move that far. You have {moves_remaining} moves left.")
                    continue
                
                if direction not in ["UP", "DOWN", "LEFT", "RIGHT"]:
                    print("Invalid direction. Use UP, DOWN, LEFT, or RIGHT.")
                    continue
                
                if game.move_player(current_player, direction, steps):
                    moves_remaining -= steps
                    if current_player.current_room:
                        print(f"You entered {current_player.current_room.value}!")
                        break
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input. Format: DIRECTION STEPS (e.g., UP 2)")
        
        # Check if player entered a room (can make suggestion)
        if current_player.current_room:
            print("\nYou're in a room. Time to make a suggestion!")
            print("Available characters:")
            for i, character in enumerate(Character):
                print(f"{i+1}. {character.value}")
            
            print("\nAvailable weapons:")
            for i, weapon in enumerate(Weapon):
                print(f"{i+1}. {weapon.value}")
            
            # Get suggestion input
            while True:
                try:
                    char_choice = int(input("Choose character (1-6): ")) - 1
                    weapon_choice = int(input("Choose weapon (1-6): ")) - 1
                    
                    if 0 <= char_choice < 6 and 0 <= weapon_choice < 6:
                        suggested_char = list(Character)[char_choice]
                        suggested_weapon = list(Weapon)[weapon_choice]
                        suggestion, refutation = game.make_suggestion(
                            current_player, suggested_char, suggested_weapon
                        )
                        
                        print(f"\nYou suggested: {suggested_char.value} with the {suggested_weapon.value} in the {current_player.current_room.value}")
                        
                        if refutation:
                            print(f"{refutation['player'].character.value} showed you: {refutation['card']}")
                        else:
                            print("No one could refute your suggestion.")
                        break
                    else:
                        print("Please enter numbers between 1 and 6.")
                except ValueError:
                    print("Please enter valid numbers.")
        
        # Option to make accusation
        accuse = input("\nDo you want to make an accusation? (y/n): ").lower()
        if accuse == 'y':
            print("Make your accusation:")
            print("Available characters:")
            for i, character in enumerate(Character):
                print(f"{i+1}. {character.value}")
            
            print("\nAvailable weapons:")
            for i, weapon in enumerate(Weapon):
                print(f"{i+1}. {weapon.value}")
            
            print("\nAvailable rooms:")
            for i, room in enumerate(Room):
                print(f"{i+1}. {room.value}")
            
            while True:
                try:
                    char_choice = int(input("Choose character (1-6): ")) - 1
                    weapon_choice = int(input("Choose weapon (1-6): ")) - 1
                    room_choice = int(input("Choose room (1-9): ")) - 1
                    
                    if (0 <= char_choice < 6 and 0 <= weapon_choice < 6 and 0 <= room_choice < 9):
                        accused_char = list(Character)[char_choice]
                        accused_weapon = list(Weapon)[weapon_choice]
                        accused_room = list(Room)[room_choice]
                        
                        if game.make_accusation(current_player, accused_char, accused_weapon, accused_room):
                            print("\n" + "="*50)
                            print(f"Congratulations {current_player.character.value}!")
                            print("Your accusation was correct!")
                            print(f"The solution was: {accused_char.value} with the {accused_weapon.value} in the {accused_room.value}")
                            print("You win the game!")
                            print("="*50)
                            sys.exit(0)
                        else:
                            print("Wrong accusation! You're out of the game.")
                            break
                    else:
                        print("Please enter valid numbers.")
                except ValueError:
                    print("Please enter valid numbers.")
        
        # Move to next player
        game.next_turn()
    
    print("Game over!")

if __name__ == "__main__":
    main()