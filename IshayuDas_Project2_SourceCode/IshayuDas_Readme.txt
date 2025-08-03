# Cluedo Game Project - Part 2

This project is a Python implementation of the classic board game Cluedo. This version features a command-line interface (CLI) and includes a fully functional AI player that uses logical deduction to participate in the game.

## Features

-   **Full Cluedo Rules:** Implements movement, suggestions, and accusations.
-   **Human & AI Players:** Supports a mix of 2-6 human and AI players.
-   **Logic-Based AI:** The AI player maintains a "clue sheet" to track known information and makes decisions based on logical deduction.
-   **Full Suggestion/Refutation Cycle:** Players refute suggestions in order, and information is revealed privately.
-   **Winning/Losing Conditions:** Players can win by making a correct accusation or lose by making an incorrect one.

## How to Run the Game

### Prerequisites

-   Python 3.8 or higher is recommended.
-   No external libraries are required to run this project.

### Steps to Run

1.  **Navigate to the Source Code Directory:**
    Open a terminal or command prompt and navigate to the root folder of the project.
    ```bash
    cd path/to/Studentname_Project2_SourceCode/
    ```

2.  **Run the Game:**
    Execute the `main.py` script using Python.
    ```bash
    python main.py
    ```

3.  **Game Setup:**
    Follow the on-screen prompts. You will be asked for:
    -   The total number of players (2-6).
    -   How many of those players should be controlled by the AI (at least 1).

4.  **Playing the Game:**
    -   **Human Turns:** You will be prompted to either move or make an accusation. Follow the prompts to select rooms, suggest suspects, and refute others' suggestions.
    -   **AI Turns:** The AI will automatically take its turn, announcing its decisions (movement, suggestions, accusations) as it makes them.

### Running Tests

To run the included unit tests, navigate to the project's root directory and run the test file. Note: The tests for Part 2 would need to be expanded to cover the new AI and refutation logic.
```bash
python -m unittest tests/test_cluedo.py
