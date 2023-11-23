import numpy as np

class Connect4_Game:
    def __init__(self, rows=4, columns=5, connect=4):
        self.rows = rows
        self.columns = columns
        self.connect = connect
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
        connect = self.connect
        # Horizontal, vertical, and diagonal checks
        for c in range(self.columns + 1 - connect):
            for r in range(self.rows):
                if np.all(self.board[r, c:c+connect] == player):
                    return True
        for c in range(self.columns):
            for r in range(self.rows + 1 - connect):
                if np.all(self.board[r:r+connect, c] == player):
                    return True
        for c in range(self.columns + 1 - connect):
            for r in range(self.rows + 1 - connect):
                if np.all([self.board[r+i, c+i] == player for i in range(connect)]):
                    return True
        for c in range(self.columns + 1 - connect):
            for r in range(connect - 1, self.rows):
                if np.all([self.board[r-i, c+i] == player for i in range(connect)]):
                    return True
        return False

    def check_draw(self):
        return np.all(self.board[0, :] != 0)

    def step(self, column):
        # Place the token and switch turns only if the move is valid
        if not self.place_token(column):
            return self.board, -1, False  # Invalid move penalty

        # Check for a win or draw
        if self.check_winner(self.turn):  # Check if the previous player won
            reward = 1
            done = True
        elif self.check_draw():
            reward = 0
            done = True
        else:
            reward = self.calculate_reward(self.turn)  # Intermediate rewards for the current board state
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
        # reward += self.count_sequences(self.connect - 1, player) * 0.2
        
        # # Penalize '3 in a row' for the opponent to avoid them winning in the next move
        # reward -= self.count_sequences(self.connect - 1, opponent) * 0.2

        # # Reward for potential '2 in a row' sequences that can lead to a '3 in a row'
        # reward += self.count_sequences(self.connect - 2, player) * 0.05
    
        # # Penalize '2 in a row' for the opponent to avoid them getting a '3 in a row'
        # reward -= self.count_sequences(self.connect - 2, opponent) * 0.05

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
        rows, cols = state.shape
        opponent = 3 - player

        def is_within_bounds(r, c):
            return 0 <= r < rows and 0 <= c < cols

        def check_sequence(r, c, dr, dc):
            player_count = 0
            sequence_cells = []

            for i in range(sequence_length):
                nr, nc = r + i * dr, c + i * dc
                if not is_within_bounds(nr, nc) or state[nr, nc] != player:
                    return 0
                sequence_cells.append((nr, nc))

            # Check if blocked at the start or end
            blocked_start = not is_within_bounds(r - dr, c - dc) or state[r - dr, c - dc] == opponent
            blocked_end = not is_within_bounds(r + sequence_length * dr, c + sequence_length * dc) or state[r + sequence_length * dr, c + sequence_length * dc] == opponent

            if blocked_start and blocked_end:
                return 0
            elif blocked_start or blocked_end:
                return 1
            else:
                return 3

        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for r in range(rows):
            for c in range(cols):
                for dr, dc in directions:
                    count += check_sequence(r, c, dr, dc)

        return count
    
    def print_board(self):
        print(self.board)  # Print the board top-down

    def undo_move(self, column):
        # Find the topmost token in the column and remove it
        for row in range(self.rows):
            if self.board[row][column] != 0:
                self.board[row][column] = 0
                return
