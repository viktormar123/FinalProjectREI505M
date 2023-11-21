import numpy as np
import random

class LinearApprox_Agent:
    def __init__(self, game, learning_rate=0.1, discount_factor=0.9, epsilon=1.0, epsilon_decay=0.99995, min_epsilon=0.02):
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
        return 5  # Adjust as needed

    def extract_features(self, state):
        features = np.zeros(self.num_features())
        # Assuming player's token is 1, and opponent's is 2.
        player_token = 1
        opponent_token = 2

        # Feature 1-2: Count open '3 in a row' for the player and opponent
        features[0] = self.game.count_sequences(3, player_token) / 20
        features[1] = self.game.count_sequences(3, opponent_token) / 20

        # Feature 3-4: Count '2 in a row' for the player and opponent
        features[2] = self.game.count_sequences(2, player_token) / 50
        features[3] = self.game.count_sequences(2, opponent_token) / 50
        
        # Feature 5: Number of free slots in the game
        features[4] = np.sum(state == 0) / (self.game.rows * self.game.columns)
        
        # # Feature 7: Central column count for the player
        # central_column_index = self.game.columns // 2
        # features[4] = sum(1 for row in state if row[central_column_index] == player_token)

        # # Feature 8: Height preference - Reward for pieces placed higher on the board
        # for row in range(self.game.rows):
        #     for col in range(self.game.columns):
        #         if state[row][col] == player_token:
        #             features[5] += self.game.rows - row
        
        # Check for features exceeding 1, which grow exponentially
        if np.any(features > 1):
            print(f"Warning: Feature values exceed 1: {features}")
            # Optional: Clip features to [0, 1] range
            features = np.clip(features, 0, 1)

        return features

    def choose_action(self, env):
        state = env.board
        possible_actions = env.possible_actions()
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(possible_actions)
        else:
            q_values = [self.get_q_value(state, action) for action in possible_actions]
            
            # Check for NaN in Q-values
            if any(np.isnan(q_values)):
                print(f"NaN detected in Q-values: {q_values}")
                # Handle NaN situation, for example by choosing a random action
                return random.choice(possible_actions)
            
            max_q_value = max(q_values)
            best_actions = [action for action, q in zip(possible_actions, q_values) if q == max_q_value]
            
            # Check if best_actions is empty which should not be the case
            if not best_actions:
                print(f"No best actions found, which should not happen. Q-values: {q_values}")
                return random.choice(possible_actions)
            
            return random.choice(best_actions)

    def get_q_value(self, state, action):
        features = self.extract_features(state)
        return np.dot(features, self.weights[:, action])

    def update(self, state, action, reward, next_state, done, possible_actions):
        features = self.extract_features(state)
        q_value = self.get_q_value(state, action)
        future_reward = 0 if done else max([self.get_q_value(next_state, a) for a in possible_actions])
        
        if np.isnan(future_reward) or np.isnan(q_value):
            print(f"NaN detected: q_value={q_value}, future_reward={future_reward}")
        target = reward + self.discount_factor * future_reward
        error = target - q_value
        self.weights[:, action] += self.learning_rate * error * features

        # Decay epsilon
        if done:
            self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)
