import numpy as np
import random

from Connect4_Game import Connect4_Game

rows, columns = 4, 5
sequence_length = 3

game = Connect4_Game(rows, columns)
max_count = 0
for _ in range(20):
    # Randomize the board
    for r in range(rows):
        for c in range(columns):
            game.board[r, c] = random.choice([0, 1, 2])
            
    count_player = game.count_sequences(sequence_length, 1)
    count_opponent = game.count_sequences(sequence_length, 2)
    max_count = max(max_count, count_player, count_opponent)

    # Optionally, print the board and the counts
    print("Board state:\n", game.board)
    print(f"Player count for sequence of {sequence_length}: {count_player}")
    print(f"Opponent count for sequence of {sequence_length}: {count_opponent}")
    print("\n")

print(f"Largest count encountered: {max_count}")

# Now call count_sequences on a board with a known sequence count
game.board = np.array([[1, 1, 1, 0, 2], [2, 0, 0, 2, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])
print("Board state:\n", game.board)
count_player = game.count_sequences(3, 1)
print(f"Player count for sequence of 3: {count_player}")
