import random

class Greedy_Bot:
    def __init__(self):
        """
        Initialize the Greedy Bot.
        """
        pass

    def play(self, env, done=False):
        """
        Executes a turn for the Greedy Bot using the provided game environment and state.
        """
        if done:
            return env.board, done
        action = self.choose_action(env)
        env.place_token(action)  # Update the game state by placing the token

        # Check if the game has reached a terminal state
        done = env.check_winner(env.turn) or env.check_draw()
        
        # Switch turn if the game is not done
        if not done:
            env.switch_turn()
        return env.board, done


    def choose_action(self, env):
        """
            Choose a move based on a greedy strategy.
        """
        possible_actions = env.possible_actions()
        player = env.turn
        # Check for a winning move
        for move in possible_actions:
            env.place_token(move)
            if env.check_winner(player):
                env.undo_move(move)
                return move
            env.undo_move(move)

        # Check to block opponent's winning move
        opponent = 3-player
        for move in possible_actions:
            env.place_token(move) # Þarf að laga þetta
            if env.check_winner(opponent):
                env.undo_move(move)
                return move
            env.undo_move(move)

        # Fallback to random move
        possible_moves = possible_actions
        return random.choice(possible_moves) if possible_moves else None
