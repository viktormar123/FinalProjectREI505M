import numpy as np
import random

class LinearApprox_Agent:
    def __init__(self, game, learning_rate=0.1, discount_factor=0.9, epsilon=1.0, epsilon_decay=0.9999, min_epsilon=0.02):
        self.game = game
        self.action_space = game.columns
        self.weights = np.zeros((self.num_features(), self.action_space))  # Weights are now a matrix
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon

    def num_features(self):
        # Number of features
        return 8  # Adjust as needed

    def extract_features(self, state):
        # Extract features based on the state only
        features = []
        # Add your feature extraction logic here
        # ...
        return np.array(features)

    def choose_action(self, state, possible_actions):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(possible_actions)
        else:
            q_values = [self.get_q_value(state, action) for action in possible_actions]
            max_q_value = max(q_values)
            best_actions = [action for action, q in zip(possible_actions, q_values) if q == max_q_value]
            return random.choice(best_actions)

    def get_q_value(self, state, action):
        features = self.extract_features(state)
        return np.dot(features, self.weights[:, action])

    def update(self, state, action, reward, next_state, done, possible_actions):
        features = self.extract_features(state)
        q_value = self.get_q_value(state, action)
        future_reward = 0 if done else max([self.get_q_value(next_state, a) for a in possible_actions])
        target = reward + self.discount_factor * future_reward
        error = target - q_value
        self.weights[:, action] += self.learning_rate * error * features

        # Decay epsilon
        if done:
            self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)
