Cluedo Game Project - Part 2

Features

-   Cluedo Rules: Implements movement, suggestions, and accusations.
-   Human & AI Players: Supports a mix of 2-6 human and AI players.
-   Logic-Based AI: The AI player maintains a "clue sheet" to track known information and makes decisions based on logical deduction.
-   Full Suggestion/Refutation Cycle: Players refute suggestions in order, and information is revealed privately.
-   Winning/Losing Conditions: Players can win by making a correct accusation or lose by making an incorrect one.

Prerequisites

-   Python 3.8 or higher is recommended.
-   No external libraries are required to run this project.

Steps to Run

1.  Clone the Repository:
    git clone https://github.com/IshayuD/CS-670-Project-2/tree/part2

2.  Navigate to the Source Code Directory:
    Open a terminal and navigate to the root folder of the project:
    cd path/to/Studentname_Project2_SourceCode/

3.  Run the Game:
    Execute the `main.py` script using Python:
    python main.py

4.  Playing the Game:
    -   Human Turns: You will be prompted to either move or make an accusation. Follow the prompts to select rooms, suggest suspects, and refute others' suggestions.
    -   AI Turns: The AI will automatically take its turn, announcing its decisions (movement, suggestions, accusations) as it makes them.

Running Tests
To run the included unit tests, navigate to the project's root directory and run the test file. Note: The tests for Part 2 would need to be expanded to cover the new AI and refutation logic:
python -m unittest tests/test_cluedo.py