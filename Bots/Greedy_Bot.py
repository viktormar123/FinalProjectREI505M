import random

class Greedy_Bot:
    def __init__(self):
        """
        Initialize the Greedy Bot.
        """
        pass

    def play(self, env, done=False, training=False):
        """
        Executes a turn for the Greedy Bot using the provided game environment and state.
        """
        if done:
            return state, done
        action = self.choose_action(env, state, env.turn)
        state, reward, done = env.step(action)
        return state, done

        return state, done


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
        opponent = -player
        for move in possible_actions:
            env.place_token(move)
            if env.check_winner(opponent):
                env.undo_move(move)
                return move
            env.undo_move(move)

        # Fallback to random move
        possible_moves = possible_actions
        return random.choice(possible_moves) if possible_moves else None
