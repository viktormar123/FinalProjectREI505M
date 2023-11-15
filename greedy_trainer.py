def greedy_move(board, player, columns, in_a_row):

    def count_sequences(board, sequence_length, player):
        # Add your 'count_sequences' code here from your Connect4Game class.
        pass

    def possible_actions(board):
        # Returns a list of columns that are not full (valid moves).
        return [c for c in range(columns) if board[0][c] == 0]

    # Check for a winning move
    for move in possible_actions(board):
        temp_board = board.copy()
        # Add your 'place_token' code here to place a token in the temporary board.
        if connect4.check_winner(temp_board, player):
            return move

    # Check to block opponent's winning move
    opponent = -player
    for move in possible_actions(board):
        temp_board = board.copy()
        # Add your 'place_token' code here to place a token in the temporary board.
        if connect4.check_winner(temp_board, opponent):
            return move

    # Extend the longest sequence
    best_move = None
    longest_sequence = 0
    for move in possible_actions(board):
        temp_board = board.copy()
        # Add your 'place_token' code here to place a token in the temporary board.
        sequence_length = count_sequences(temp_board, in_a_row - 1, player)  # Check for the longest sequence
        if sequence_length > longest_sequence:
            longest_sequence = sequence_length
            best_move = move

    # Prefer center column if no other strategy applies
    center_column = columns // 2
    if center_column in possible_actions(board) and best_move is None:
        return center_column

    # Fallback to random move
    return best_move if best_move is not None else random.choice(possible_actions(board))