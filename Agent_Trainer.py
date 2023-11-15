from Objects.Classes.Connect4Game import Connect4GameClass
from Objects.Classes.QLearningAgent import QLearningAgentClass
import matplotlib.pyplot as plt

class Connect4TrainerClass:
    def __init__(self, opponent=None, num_episodes=500, q_table_path= "Q_tables", starting_policy="alternate", espilon_decay=None, min_epsilon=None, q_table_name = "q_table.pkl"):
        self.num_episodes = num_episodes
        self.q_table_path = q_table_path
        # Initialize the Q-learning agent
        self.agent = QLearningAgentClass(
            action_space=Connect4GameClass().columns,
            learning_rate=0.1,
            discount_factor=0.9,
            epsilon=1.0,
            epsilon_decay=0.99999 if not espilon_decay else espilon_decay,
            min_epsilon=0.05 if not min_epsilon else min_epsilon,
            q_table_name = q_table_name
        )
        self.opponent = opponent() if opponent else self.agent
        # Starting policy
        self.starting_policy = starting_policy  # Added parameter for starting policy
        self.agent_starts = starting_policy != 'never_start'  # Determine if agent starts in the first game


    def train(self):
        # Initialize the Connect4 environment
        connect4_env = Connect4GameClass(rows=4, columns=5, in_a_row=4)

        Q_size = []
        for episode in range(self.num_episodes):
            current_state = connect4_env.reset()
            done = False

            # New logic for handling who starts the game
            if self.starting_policy == 'alternate':
                self.agent_starts = not self.agent_starts
            elif self.starting_policy == 'never_start':
                self.agent_starts = False  # Ensure agent never starts
            
            # If opponent starts, make the first move for the opponent
            if not self.agent_starts and self.opponent:
                current_state, _ = self.opponent.play(connect4_env, current_state, False)

            while not done:
                possible_actions = connect4_env.possible_actions()
                action = self.agent.choose_action(current_state, possible_actions)

                # Apply the action to the environment
                next_state, reward, done = connect4_env.step(action)

                # If there is an opponent, let the opponent play here
                if self.opponent:
                    next_state, done = self.opponent.play(connect4_env, next_state, done)

                # Agent learns from the action
                self.agent.update_q_table(current_state, action, reward, next_state, done, possible_actions)
                current_state = next_state

            # Progress tracking
            if episode % 1000 == 0:
                table = self.agent.q_table
                size = len(table)
                Q_size.append(size)
                print(f"Episode {episode} complete. Q-table size: {size}, epsilon: {self.agent.epsilon}")

        # Save the Q-table
        self.agent.save_q_table(self.q_table_path, q_table_name=self.agent.q_table_name)
        return Q_size
        # Plotting the Q-table size
        




    
