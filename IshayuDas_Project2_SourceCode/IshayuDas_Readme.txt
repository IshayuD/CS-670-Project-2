Cluedo (Clue) Game Implementation - Part 1

Instructions to Run the Game:

1. Prerequisites:
   - Python 3.6 or higher installed on your system
   - No additional packages required (uses only standard library)

2. Running the Game:
   - Navigate to the project directory in your terminal/command prompt
   - Run the command: python main.py

3. Game Instructions:
   - The game supports 3-6 players (automatically assigned characters)
   - On your turn, you'll roll a die and move your character
   - Movement is done by entering direction and steps (e.g., "UP 2")
   - When you enter a room, you must make a suggestion
   - Suggestions involve choosing a character and weapon to suggest
   - Other players will refute if they have cards that match
   - You can make an accusation at any time, but be careful - wrong accusations eliminate you!

4. Game Rules:
   - Standard Cluedo rules apply
   - Secret passages connect: Study-Kitchen and Conservatory-Lounge
   - Players must roll to exit rooms
   - Suggested characters are moved to the suggestion room
   - Correct accusation wins the game

5. Project Structure:
   - cluedo_game/ contains all game logic modules
   - board.py: Mansion layout and game components
   - cards.py: Card and deck implementation
   - player.py: Player class and logic
   - game.py: Main game logic and turn management
   - utils.py: Helper functions
   - main.py: Entry point and user interface

6. Notes:
   - This is a text-based implementation (Part 1 requirements)
   - Error handling is basic in this version (will be expanded in Part 2)
   - The game follows standard Cluedo rules with some simplifications for the CLI interface