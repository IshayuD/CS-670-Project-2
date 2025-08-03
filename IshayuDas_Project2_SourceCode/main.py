from cluedo_game.game import Game

def main():
    """
    Initializes and runs the Cluedo game.
    """
    print("--- Welcome to Cluedo! ---")
    
    while True:
        try:
            num_players = int(input("Enter the number of players (2-6): "))
            if 2 <= num_players <= 6:
                break
            else:
                print("Invalid number. Please enter a number between 2 and 6.")
        except ValueError:
            print("Invalid input. Please enter a number.")
            
    game = Game(num_players)
    game.run()

if __name__ == "__main__":
    main()