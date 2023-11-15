import numpy as np
import random
import pickle
import os

class QLearningAgentClass:
    def __init__(self, action_space, learning_rate=0.1, discount_factor=0.9, epsilon=1.0, epsilon_decay=0.9995, min_epsilon=0.01, q_table_name = "q_table.pkl"):
        self.action_space = action_space  # Number of possible actions
        print(action_space)
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        self.q_table_name = q_table_name
        self.q_table = self.init_q_table()  # Initialize Q-table as an empty dictionary

    def init_q_table(self):
        q_table = {}
        q_table["INFO"] = (f"Talbe name: {self.q_table_name}, Action space: {self.action_space}, Learning Rate: {self.learning_rate}, Discount Factor: {self.discount_factor}, Epsilon: {self.epsilon}, Epsilon Decay: {self.epsilon_decay}, Min Epsilon: {self.min_epsilon}")
        return q_table

    def get_state_key(self, state):
        # Flatten the board and convert to a string
        return ''.join(str(x) for x in state.reshape(-1))

    def flip(self, state):
            width = self.action_space

            # Flip the board since the board is symmetric, makes for faster Q-learning
            chunks = [state[i:i+width] for i in range(0, len(state), width)]
            flipped_state = ''.join(chunk[::-1] for chunk in chunks)

            return flipped_state

    def choose_action(self, state, possible_actions):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(possible_actions)
        else:
            state_key = self.get_state_key(state)
            q_values = {action: self.q_table.get((state_key, action), 0) for action in possible_actions}
            max_q_value = max(q_values.values())
            actions_with_max_q = [action for action, q in q_values.items() if q == max_q_value]
            return random.choice(actions_with_max_q)

    def update_q_table(self, state, action, reward, next_state, done, possible_actions):
        state_key = self.get_state_key(state)
        next_state_key = self.get_state_key(next_state)

        # Get the best Q value for the next state
        next_max = max([self.q_table.get((next_state_key, a), 0) for a in possible_actions]) if not done else 0

        # Update the Q value for the current state and action
        old_value = self.q_table.get((state_key, action), 0)
        new_value = round(old_value + self.learning_rate * (reward + self.discount_factor * next_max - old_value), 4)

        self.q_table[(state_key, action)] = new_value
      
        # Update the Q value for the flipped state (2x faster updateing):
        self.q_table[(self.flip(state_key), self.action_space-action)] = new_value

        # Decay epsilon
        if done:
            self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

    def save_q_table(self, file_path, q_table_name):
        # This gives you the current working directory
        current_working_directory = os.getcwd()
        # Relative path
        relative_path = file_path
        # Combine them
        full_path = os.path.join(current_working_directory, relative_path)
        file_path = os.path.join(full_path, q_table_name)
        with open(file_path, 'wb') as f:
            pickle.dump(self.q_table, f)

    def load_q_table(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                self.q_table = pickle.load(f)
                print(f"Q-table loaded from {file_path}")
        else:
            print(f"No Q-table found at {file_path}, starting fresh.")
    
    def play(self, env, state, done):
        if not done:
            possible_actions = env.possible_actions()
            action = self.choose_action(state, possible_actions)
            next_state, reward, done = env.step(action)
            return next_state, done
        else:
            return state, done

    # Add any additional methods needed for training, evaluation, etc.
