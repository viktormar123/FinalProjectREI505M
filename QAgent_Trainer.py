from Connect4_Game import Connect4_Game
from Bots.QLearning_Agent import QLearning_Agent
import matplotlib.pyplot as plt

class QAgent_Trainer:
    def __init__(self, 
                opponent: object=None,
                num_episodes: int=500,
                q_table_path: str= "Q_tables",
                epsilon_decay: float=None,
                min_epsilon: float=None,
                q_table_name:str = "q_table.pkl",
                connect: int=4,
                starting_policy: bool= True):
        self.num_episodes = num_episodes
        self.q_table_path = q_table_path
        # Initialize the Q-learning agent
        self.agent = QLearning_Agent(
            action_space=Connect4_Game(rows=connect, columns=connect + 1).columns,
            learning_rate=0.1,
            discount_factor=0.9,
            epsilon=1.0,
            epsilon_decay=0.99999 if not epsilon_decay else epsilon_decay,
            min_epsilon=0.05 if not min_epsilon else min_epsilon,
            q_table_name = q_table_name
        )
        self.opponent = opponent() if opponent else self.agent
        self.starting_policy = starting_policy if starting_policy else False

    def train(self):
        # Initialize the Connect4 environment
        connect4_env = Connect4_Game(rows=4, columns=5, connect=4)

        Q_size = []
        for episode in range(self.num_episodes):
            current_state = connect4_env.reset()
            done = False
            
            # If opponent starts, make the first move for the opponent
            if not self.starting_policy and self.opponent:
                connect4_env, current_state, done = self.opponent.play(connect4_env, current_state, False)

            while not done:
                # Get the action from the agent
                action = self.agent.choose_action(connect4_env)

                # Apply the action to the environment
                next_state, reward, done = connect4_env.step(action)

                # If there is an opponent, let the opponent play here
                if self.opponent:
                    connect4_env, next_state, done = self.opponent.play(connect4_env, done)

                # Agent learns from the action
                self.agent.update_q_table(connect4_env, action, reward, next_state, done)
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



