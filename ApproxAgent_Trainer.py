from Connect4_Game import Connect4_Game
from Bots.LinearApprox_Agent import LinearApprox_Agent
import matplotlib.pyplot as plt

class ApproxAgent_Trainer:
    def __init__(self, 
                opponent: object = None,
                num_episodes: int = 500,
                learning_rate: float = 0.1,
                discount_factor: float = 0.9,
                epsilon: float = 1.0,
                epsilon_decay: float = 0.9999,
                min_epsilon: float = 0.05,
                connect: int = 4,
                starting_policy: bool = True):
        self.num_episodes = num_episodes

        # Initialize the Linear Approximation Agent
        self.agent = LinearApprox_Agent(
            game=Connect4_Game(rows=connect, columns=connect + 1),
            learning_rate=learning_rate,
            discount_factor=discount_factor,
            epsilon=epsilon,
            epsilon_decay=epsilon_decay,
            min_epsilon=min_epsilon
        )

        self.opponent = opponent if opponent else self.agent
        self.starting_policy = starting_policy if starting_policy else False

    def train(self):
        connect4_env = Connect4_Game(rows=4, columns=5, in_a_row=4)

        for episode in range(self.num_episodes):
            current_state = connect4_env.reset()
            done = False
            
            if not self.starting_policy and self.opponent:
                current_state, done = self.opponent.play(connect4_env, current_state, False)

            while not done:
                action = self.agent.choose_action(connect4_env)
                next_state, reward, done = connect4_env.step(action)

                if self.opponent:
                    next_state, done = self.opponent.play(connect4_env, done)

                self.agent.update(current_state, action, reward, next_state, done, connect4_env.possible_actions())
                current_state = next_state

            if episode % 1000 == 0:
                print(f"Episode {episode} complete. Epsilon: {self.agent.epsilon}")
                
        return self.agent.weights
