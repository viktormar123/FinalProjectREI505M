import random

class GreedyBotClass:
    def __init__(self):
        """
        Initialize the Greedy Bot.
        """
        pass

    def play(self, game_env, state, done=False, training=False):
        """
        Executes a turn for the Greedy Bot using the provided game environment and state.
        """
        if done:
            return state, done
        action = self.choose_action(game_env, state, game_env.turn)
        state, reward, done = game_env.step(action)
        return state, done

        return state, done


    def choose_action(self, possible_actions, game_env):
        """
            Choose a move based on a greedy strategy.
        """
        player = game_env.turn
        # Check for a winning move
        for move in possible_actions:
            game_env.place_token(move)
            if game_env.check_winner(player):
                game_env.undo_move(move)
                return move
            game_env.undo_move(move)

        # Check to block opponent's winning move
        opponent = -player
        for move in possible_actions:
            game_env.place_token(move)
            if game_env.check_winner(opponent):
                game_env.undo_move(move)
                return move
            game_env.undo_move(move)

        # Fallback to random move
        possible_moves = possible_actions
        return random.choice(possible_moves) if possible_moves else None
