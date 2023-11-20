import numpy as np
import random
import copy

class AlphaBeta_Agent:
    def __init__(self, depth=4):
        """
        Initialize the AlphaBetaAgent.
        """
        self.depth = depth

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
        column, score = self.minimax(game_env, self.depth, -np.inf, np.inf, True)
        return column

    def minimax(self, game_env, depth, alpha, beta, maximizingPlayer):
        valid_locations = game_env.possible_actions()
        is_terminal = self.is_terminal_node(game_env)
        if depth == 0 or is_terminal:
            if is_terminal:
                if game_env.check_winner(game_env.turn):
                    return (None, float('inf') if game_env.turn == 1 else float('-inf'))
                elif game_env.check_winner(3 - game_env.turn):
                    return (None, float('-inf') if game_env.turn == 1 else float('inf'))
                else:  # Game is over (draw)
                    return (None, 0)
            else:  # Depth is zero
                return (None, self.evaluate(game_env.board, game_env))

        if maximizingPlayer:
            value = float('-inf')
            column = random.choice(valid_locations)
            for col in valid_locations:
                # Simulate the move
                if game_env.place_token(col):
                    new_score = self.minimax(game_env, depth - 1, alpha, beta, False)[1]
                    game_env.undo_move(col)  # Undo the move
                    if new_score > value:
                        value = new_score
                        column = col
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break
            return column, value
        else:  # Minimizing player
            value = float('inf')
            column = random.choice(valid_locations)
            for col in valid_locations:
                # Simulate the move
                if game_env.place_token(col):
                    new_score = self.minimax(game_env, depth - 1, alpha, beta, True)[1]
                    game_env.undo_move(col)  # Undo the move
                    if new_score < value:
                        value = new_score
                        column = col
                    beta = min(beta, value)
                    if alpha >= beta:
                        break
            return column, value
        
    def is_terminal_node(self, game_env):
        """
        Check if the board is a terminal node (win, lose, or draw).
        """
        return game_env.check_winner(game_env.turn) or \
               game_env.check_winner(3 - game_env.turn) or \
               game_env.check_draw()

    def evaluate(self, board, game_env):
        score = 0

        # Center column preference (typically a good strategy in Connect 4)
        center_array = board[:, game_env.columns // 2]
        center_count = np.count_nonzero(center_array == game_env.turn)
        score += center_count * 3

        # Score Horizontal
        for r in range(game_env.rows):
            row_array = board[r, :]
            for c in range(game_env.columns - 3):
                window = row_array[c:c + 4]
                score += self.evaluate_window(window, game_env.turn)

        # Score Vertical
        for c in range(game_env.columns):
            col_array = board[:, c]
            for r in range(game_env.rows - 3):
                window = col_array[r:r + 4]
                score += self.evaluate_window(window, game_env.turn)

        # Score positive sloped diagonals
        for r in range(game_env.rows - 3):
            for c in range(game_env.columns - 3):
                window = [board[r + i][c + i] for i in range(4)]
                score += self.evaluate_window(window, game_env.turn)

        # Score negative sloped diagonals
        for r in range(game_env.rows - 3):
            for c in range(3, game_env.columns):
                window = [board[r + i][c - i] for i in range(4)]
                score += self.evaluate_window(window, game_env.turn)

        return score

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


# Additional methods required for AlphaBetaAgent would go here,
# such as `evaluate_window`, `get_next_open_row`, etc.
