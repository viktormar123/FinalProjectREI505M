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

    def play(self, env, state, done=False):
        """
        Executes a turn for the Random Bot.
        """
        if done:
            return env, state, done
        action = self.choose_action(env)
        state, reward, done = env.step(action)
        return env, state, done
    
    
