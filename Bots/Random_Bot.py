import random

class Random_Bot:
    def __init__(self):
        """
        Initialize the Random Bot with a reference to the Connect4 game.
        :param game: Instance of Connect4_Game.
        """

    def choose_action(self, env: object) -> list:
        """
        Choose a random valid action (column) from the Connect4 game.
        :return: A random valid column number.
        """
        return random.choice(env.possible_actions())

    def play(self, env, done=False):
        """
        Executes a turn for the Random Bot.
        """
        if done:
            return env, env.board, done
        action = self.choose_action(env)
        env.place_token(action)  # Update the game state by placing the token

        # Check if the game has reached a terminal state
        done = env.check_winner(env.turn) or env.check_draw()
        
        # Switch turn if the game is not done
        if not done:
            env.switch_turn()

        return env.board, done
    
    
