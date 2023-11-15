import random

class RandomBotClass:
    def __init__(self):
        """
        Initialize the Random Bot with a reference to the Connect4 game.
        :param game: Instance of Connect4GameClass.
        """

    def choose_action(self, possible_actions, env=None):
        """
        Choose a random valid action (column) from the Connect4 game.
        :return: A random valid column number.
        """
        return random.choice(possible_actions)

    def play(self, game_env, state, done=False, training=True):
        """
        Executes a turn for the Random Bot.
        """
        if done:
            return state, done
        possible_actions = game_env.possible_actions()
        action = self.choose_action(possible_actions)
        state, reward, done = game_env.step(action)
        return state, done
    
    
