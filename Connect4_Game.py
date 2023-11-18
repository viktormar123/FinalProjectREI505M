import numpy as np

class Connect4_Game:
    def __init__(self, rows=4, columns=5, in_a_row=4):
        self.rows = rows
        self.columns = columns
        self.in_a_row = in_a_row
        self.board = np.zeros((rows, columns), dtype=int)
        self.turn = 1  # Player 1 starts

    def reset(self):
        self.board = np.zeros((self.rows, self.columns), dtype=int)
        self.turn = 1
        return self.board

    def switch_turn(self):
        self.turn = 3 - self.turn  # Alternate between 1 and 2 

    def place_token(self, column):
        # Check for valid move
        if not self.is_valid_location(column):
            return False

        # Find the lowest empty spot in the column and place the token
        for row in reversed(range(self.rows)):
            if self.board[row][column] == 0:
                self.board[row][column] = self.turn
                return True
        return False

    def is_valid_location(self, column):
        return self.board[0][column] == 0

    def possible_actions(self):
        return [col for col in range(self.columns) if self.is_valid_location(col)]

    def check_winner(self, player):
        # Horizontal, vertical, and diagonal checks
        for c in range(self.columns - 3):
            for r in range(self.rows):
                if np.all(self.board[r, c:c+4] == player):
                    return True
        for c in range(self.columns):
            for r in range(self.rows - 3):
                if np.all(self.board[r:r+4, c] == player):
                    return True
        for c in range(self.columns - 3):
            for r in range(self.rows - 3):
                if np.all([self.board[r+i, c+i] == player for i in range(4)]):
                    return True
        for c in range(self.columns - 3):
            for r in range(3, self.rows):
                if np.all([self.board[r-i, c+i] == player for i in range(4)]):
                    return True
        return False

    def check_draw(self):
        return np.all(self.board[0, :] != 0)

    def step(self, column):
        # Place the token and switch turns only if the move is valid
        if not self.place_token(column):
            return self.board, -1, False  # Invalid move penalty

        # Check for a win or draw
        if self.check_winner(3 - self.turn):  # Check if the previous player won
            reward = 1
            done = True
        elif self.check_draw():
            reward = 0
            done = True
        else:
            reward = self.calculate_reward(3 - self.turn)  # Intermediate rewards for the current board state
            done = False
            self.switch_turn()  # Only switch turns if the game is not done

        return self.board.copy(), reward, done

    def calculate_reward(self, player):
        # Check for an immediate win or loss
        win = self.check_winner(player)  # Pass the player variable
        #draw = self.check_draw(player)
        if win:
            return 1 if player == 1 else -1 # Win reward for player 1, loss for player 2
        #elif draw:
        #    return 0.5

        # Implement reward shaping with intermediate rewards
        reward = 0
        opponent = 3 - player
    
        # # Reward for potential '3 in a row' sequences that can lead to a win
        # reward += self.count_sequences(self.in_a_row - 1, player) * 0.5
        
        # # Penalize '3 in a row' for the opponent to avoid them winning in the next move
        # reward -= self.count_sequences(self.in_a_row - 1, opponent) * 0.5

        # # Reward for potential '2 in a row' sequences that can lead to a '3 in a row'
        # reward += self.count_sequences(self.in_a_row - 2, player) * 0.1
    
        # # Penalize '2 in a row' for the opponent to avoid them getting a '3 in a row'
        # reward -= self.count_sequences(self.in_a_row - 2, opponent) * 0.1

        # # Central column preference
        # central_column_index = self.columns // 2
        # central_column_count = sum(1 for row in self.board if row[central_column_index] == self.turn)
        # reward += central_column_count * 0.05

        # # Height preference - assuming higher rows are indexed with smaller numbers
        # for row in range(self.rows):
        #     for col in range(self.columns):
        #         if self.board[row][col] == self.turn:
        #             # Reward higher pieces more
        #             reward += (self.rows - row) * 0.01

        # Additional shaping can be added here, such as for creating forks,
        # blocking opponent's forks, etc.

        return round(reward, 3)

    def count_sequences(self, sequence_length, player):
        count = 0
        state = self.board
        rows = len(state)
        cols = len(state[0])
        opponent = 3 - player

        # Function to check if a position is within the board boundaries
        def is_within_bounds(row, col):
            return 0 <= row < rows and 0 <= col < cols

        # Function to check the status of a sequence
        def check_sequence_status(r, c, dr, dc):
            sequence_status = 0
            if all(state[r + i * dr][c + i * dc] == player or state[r + i * dr][c + i * dc] == 0 for i in range(sequence_length)):
                before = (r - dr, c - dc)
                after = (r + sequence_length * dr, c + sequence_length * dc)
                blocked_before = not is_within_bounds(*before) or state[before[0]][before[1]] == opponent
                blocked_after = not is_within_bounds(*after) or state[after[0]][after[1]] == opponent

                if not blocked_before and not blocked_after:
                    sequence_status = 2
                elif blocked_before != blocked_after:
                    sequence_status = 1
            return sequence_status

        # Horizontal sequences
        for r in range(rows):
            for c in range(cols - sequence_length + 1):
                count += check_sequence_status(r, c, 0, 1)

        # Vertical sequences
        for c in range(cols):
            for r in range(rows - sequence_length + 1):
                count += check_sequence_status(r, c, 1, 0)

        # Positive diagonal sequences
        for c in range(cols - sequence_length + 1):
            for r in range(rows - sequence_length + 1):
                count += check_sequence_status(r, c, 1, 1)

        # Negative diagonal sequences
        for c in range(cols - sequence_length + 1):
            for r in range(sequence_length - 1, rows):
                count += check_sequence_status(r, c, -1, 1)

        return count

    
    def print_board(self):
        print(self.board)  # Print the board top-down

    def undo_move(self, column):
        # Find the topmost token in the column and remove it
        for row in range(self.rows):
            if self.board[row][column] != 0:
                self.board[row][column] = 0
                return
