def display_board(mansion, players):
    """Display a simple text representation of the board"""
    board = [[" " for _ in range(6)] for _ in range(3)]
    
    # Mark rooms
    for room, data in mansion.rooms.items():
        x, y = data["position"]
        board[x][y] = room.value[0]  # First letter of room name
    
    # Mark players
    for player in players:
        x, y = player.position
        if board[x][y].isalpha():
            board[x][y] += player.character.value[0]
        else:
            board[x][y] = player.character.value[0]
    
    # Print board
    print("Current Board:")
    for row in board:
        print(" ".join(f"[{cell:3}]" for cell in row))
    print()