import numpy as np
import random

class MiniMax_Agent():
    def __init__(self, rows, columns, depth = 1, starting_policy = True):
        self.rows = rows
        self.cols = columns
        self.depth = depth
        self.BOT_PIECE = 2 if starting_policy else 1
        self.PLAYER_PIECE = 3 - self.BOT_PIECE

    def play(self, game_env, done=False):
        """
        Executes a turn for the AlphaBetaAgent using the provided game environment and state.
        """
        if done:
            return game_env.board, done
        action = self.choose_action(game_env)
        game_env.place_token(action)  # Update the game state by placing the token

        # Check if the game has reached a terminal state
        done = game_env.check_winner(game_env.turn) or game_env.check_draw()
        
        # Switch turn if the game is not done
        if not done:
            game_env.switch_turn()
        return game_env.board, done
    
    def choose_action(self, game_env):
        """
        Choose an action using the Alpha-Beta pruning algorithm.
        """
        column, score = self.minimax(game_env.board, self.depth, -np.inf, np.inf, True)
        return column        

    # Place a piece on the board
    @staticmethod
    def drop_piece(board, row, col, piece):
        board[row][col] = piece

    # Check if chosen column has an empty slot
    def is_valid_location(self, board, col):
        return board[0][col] == 0

    # Check which row the piece falls into
    def get_next_open_row(self, board, col):
        for r in reversed(range(self.rows)):
            if board[r][col] == 0:
                return r

    # Get all locations that could contain a piece
    def get_valid_locations(self, board):
        valid_locations= []
        for col in range(self.cols):
            if self.is_valid_location(board, col):
                valid_locations.append(col)
        return valid_locations

    # Look at the board using a 4-piece window to evaluate the whole board & choose a move
    def score_position(self, board, piece):
        score = 0

        # Score centre column
        centre_array = [int(i) for i in list(board[:, self.cols//2])]
        centre_count = centre_array.count(piece)
        score += centre_count * 3

        # Score horizontal positions
        for r in range(self.rows):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(self.cols-3):
                # Create a horizontal window of 4
                window = row_array[c:c+4]
                score += self.evaluate_window(window, piece)

        # Score vertical positions
        for c in range(self.cols):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(self.rows-3):
                # Create a vertical window of 4
                window = col_array[r:r+4]
                score += self.evaluate_window(window, piece)

        # Score positive diagonals
        for r in range(self.rows-3):
            for c in range(self.cols-3):
                # Create a positive diagonal window of 4
                window = [board[r+i][c+i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        # Score negative diagonals
        for r in range(self.rows-3):
            for c in range(self.cols-3):
                # Create a negative diagonal window of 4
                window = [board[r+3-i][c+i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        return score

    # Set window scores based on contents
    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = 3 - piece

        if np.count_nonzero(window == piece) == 4:
            score += 100
        elif np.count_nonzero(window == piece) == 3 and np.count_nonzero(window == 0) == 1:
            score += 5
        elif np.count_nonzero(window == piece) == 2 and np.count_nonzero(window == 0) == 2:
            score += 2

        if np.count_nonzero(window == opp_piece) == 3 and np.count_nonzero(window == 0) == 1:
            score -= 4

        return score

    # Check to see if the game has been won
    def winning_move(self, board, piece):
        # Check valid horizontal locations for win
        for c in range(self.cols-3):
            for r in range(self.rows):
                if board[r][c] == piece and board [r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                    return True

        # Check valid vertical locations for win
        for c in range(self.cols):
            for r in range(self.rows-3):
                if board[r][c] == piece and board [r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                    return True

        # Check valid positive diagonal locations for win
        for c in range(self.cols-3):
            for r in range(self.rows-3):
                if board[r][c] == piece and board [r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                    return True

        # check valid negative diagonal locations for win
        for c in range(self.cols-3):
            for r in range(3, self.rows):
                if board[r][c] == piece and board [r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                    return True
                

    # Define winning moves or no remaining valid locations as terminal nodes (end points)
    def is_terminal_node(self, board):
        return self.winning_move(board, 1) or self.winning_move(board, 2) or len(self.get_valid_locations(board)) == 0

    # Pick the best move by looking at all possible future moves and comparing their scores
    def minimax(self, board, depth, alpha, beta, maximisingPlayer):
        valid_locations = self.get_valid_locations(board)

        is_terminal = self.is_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                # Weight the bot winning really high
                if self.winning_move(board, self.BOT_PIECE):
                    return (None, 10000000)
                # Weight the human winning really low
                elif self.winning_move(board, self.PLAYER_PIECE):
                    return (None, -10000000)
                else: # No more valid moves
                    return (None, 0)
            # Return the bot's score
            else:
                return (None, self.score_position(board, self.BOT_PIECE))

        if maximisingPlayer:
            value = -10000000
            # Randomise column to start
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                # Create a copy of the board
                b_copy = board.copy()
                # Drop a piece in the temporary board and record score
                self.drop_piece(b_copy, row, col, self.BOT_PIECE)
                new_score = self.minimax(b_copy, depth-1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    # Make 'column' the best scoring column we can get
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else: # Minimising player
            value = 10000000
            # Randomise column to start
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                # Create a copy of the board
                b_copy = board.copy()
                # Drop a piece in the temporary board and record score
                self.drop_piece(b_copy, row, col, self.PLAYER_PIECE)
                new_score = self.minimax(b_copy, depth-1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    # Make 'column' the best scoring column we can get
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value
