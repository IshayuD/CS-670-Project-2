# main.py

from cluedo_game.game import Game

def main():
    """
    Initializes and runs the Cluedo game, allowing for a mix of human and AI players.
    """
    print("--- 🎲 Welcome to Cluedo! 🕵️ ---")
    
    while True:
        try:
            total_players = int(input("Enter the total number of players (2-6): "))
            if 2 <= total_players <= 6:
                break
            else:
                print("Invalid number. Please enter a number between 2 and 6.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    while True:
        try:
            # The project requires at least one AI player.
            num_ai = int(input(f"Enter the number of AI players (1-{total_players}): "))
            if 1 <= num_ai <= total_players:
                break
            else:
                print(f"Invalid number. Please enter a number between 1 and {total_players}.")
        except ValueError:
            print("Invalid input. Please enter a number.")
            
    game = Game(total_players, num_ai)
    game.run()

if __name__ == "__main__":
    main()
