import numpy as np
import random

class Connect4():
    def __init__(self, n, m):
        self.height = n
        self.width = m
        self.board = np.zeros((n, m), dtype=int)
        self.turn = 1  # Player 1 starts

    def reset_board(self):
        self.board = np.zeros((self.height , self.width), dtype=int)
        self.turn = 1  # Player 1 starts
        return self.board

    def is_valid_move(self, col):
        return self.board[0, col] == 0

    def place_token(self, col):
        # Find the column and place a token
        col_token = self.board[:, col]

        if not np.any(col_token == 0):
          return False

        row_idx = np.where(col_token == 0)[0][-1] # Find the first line in the column where no player has played
        self.board[row_idx, col] = self.turn
        self.turn *= -1 # Next player to play

        return True

    def who_wins(self):
        # Check horizontal
        for r in range(self.height):
          for c in range(self.width - 3):
            line = self.board[r, c:c+4]
            if np.all(line == 1):
              return 1
            elif np.all(line == -1):
              return -1

        # Check vertical
        for c in range(self.width):
          for r in range(self.height - 3):
            line = self.board[r:r+4, c]
            if np.all(line == 1):
              return 1
            elif np.all(line == -1):
              return -1

        # Check positive diagonal
        for r in range(self.height - 3):
          for c in range(self.width - 3):
            line = np.array([self.board[r+i, c+i] for i in range(4)])
            if np.all(line == 1):
              return 1
            elif np.all(line == -1):
              return -1

        # Check negative diagonal
        for r in range(3, self.height):
          for c in range(self.width - 3):
            line = np.array([self.board[r-i, c+i] for i in range(4)])
            if np.all(line == 1):
              return 1
            elif np.all(line == -1):
              return -1

        # If no winner, check if board is full (draw)
        if np.all(self.board != 0):
          return 'draw'

        # No winner yet
        return None

    def step(self, col):
        # Place the token in the board
        self.place_token(col)
        # Check if the current player wins
        win = self.who_wins()
        if win is not None:
            # If the game ends, set reward accordingly
            if win == 1:
                reward = 1  # Player 1 wins
            elif win == -1:
                reward = -1  # Player 2 wins
            elif win == 'draw':
                reward = 0.5  # Draw
            return self.board.copy(), reward, True
        # Check for a draw (no more valid moves)
        if not np.any(self.board[0, :] == 0):
            # Game is a draw
            return self.board.copy(), 0, True
        # Game continues with no immediate reward
        return self.board.copy(), 0, False

    def is_game_over(self):
        return self.who_wins() is not None or not np.any(self.board[0, :] == 0)

    def print_board(self):
        # Create a simple text-based representation of the board
        print(" " + " ".join(map(str, range(self.width))))
        print("+---" * self.width + "+")
        for r in range(self.height):
            print("| " + " | ".join(self.board[r].astype(str)) + " |")
            print("+---" * self.width + "+")
        print("Player 1: 1, Player 2: -1\n")
