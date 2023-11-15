import random

class AgentClass:
    def __init__(self, q_table):
        """
        Initialize the Q-learning agent with a pre-trained Q-table.
        :param q_table: A dictionary representing the Q-table, where keys are state-action pairs and values are Q-values.
        """
        self.q_table = q_table

    def get_state_key(self, state):
        """
        Convert the state to a string key that can be used to look up in the Q-table.
        This may need to be adjusted based on how states are represented in your specific problem.
        :param state: The current state of the environment.
        :return: A string representing the state.
        """
        return str(state.reshape(-1))

    def choose_action(self, possible_actions, env):
        """
        Choose the best action based on the current state and the Q-table.
        :param state: The current state of the environment.
        :param possible_actions: A list of possible actions in the current state.
        :return: The action with the highest Q-value for the current state.
        """
        state = env.board
        state_key = self.get_state_key(state)
        # Find the action with the highest Q-value for the current state
        best_action = None
        best_q_value = float('-inf')
        
        for action in possible_actions:
            q_value = self.q_table.get((state_key, action), 0)  # Default Q-value is 0 if not found in the table
            if q_value > best_q_value:
                best_q_value = q_value
                best_action = action
                #if best_q_value == 0:
                    #best_action = random.choice(possible_actions)
        return best_action


