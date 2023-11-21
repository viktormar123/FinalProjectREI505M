from matplotlib import pyplot as plt
import numpy as np

from Connect4_Game import Connect4_Game

from Bots.LinearApprox_Agent import LinearApprox_Agent
from Bots.QLearning_Agent import QLearning_Agent
from Bots.Random_Bot import Random_Bot
from Bots.Greedy_Bot import Greedy_Bot
from Bots.AlphaBeta_Agent import AlphaBeta_Agent

from ApproxAgent_Trainer import ApproxAgent_Trainer
from QAgent_Trainer import QAgent_Trainer

from Evaluate_Agent import Evaluate_Agent
from Human_vs_Agent import Human_vs_Agent

# Define the parameters for game enviroment and training 
rows, cols, connect = 4, 5, 4 # Smaller board size, less computation
alpha = 0.3 # 0.5 was bad
epsilon = 0.2 # 20% exploration ~ 2 random moves if played 40 moves

# Define the game environment and ApproxAgent
game_env = Connect4_Game(rows, cols, connect) 
ApproxAgent = LinearApprox_Agent(game_env, alpha, 1, 0.2, 1, 0.2)

# Define the opponent, both for training and evaluation
opponent = Random_Bot()

# Parameters for training and evaluation
num_episodes = 5000
evaluation_interval = 500
evaluation_games = 100

win_rates = []
loss_rates = []
draw_rates = []
evaluation_episodes = []

for episode in range(num_episodes):
            current_state = game_env.reset()
            done = False

            while not done:
                action = ApproxAgent.choose_action(game_env)
                next_state, reward, done = game_env.step(action)

                next_state, done = opponent.play(game_env, done)

                ApproxAgent.update(current_state, action, reward, next_state, done, game_env.possible_actions())
                current_state = next_state

            if episode == 0 or (episode + 1) % evaluation_interval == 0:
                print(f"\nEpisode {episode + 1} complete.")
                results = Evaluate_Agent(ApproxAgent, opponent, game_env, games = evaluation_games)
                
                # Store the results
                win_rates.append(results['win'] / evaluation_games)
                loss_rates.append(results['loss'] / evaluation_games)
                draw_rates.append(results['draw'] / evaluation_games)
                evaluation_episodes.append(episode)
                
                
plt.figure(figsize=(10, 6))
plt.plot(evaluation_episodes, win_rates, label='Win Rate')
plt.plot(evaluation_episodes, loss_rates, label='Loss Rate')
plt.plot(evaluation_episodes, draw_rates, label='Draw Rate')

plt.xlim(-1, num_episodes)
plt.ylim(0, 1)
plt.xticks(np.arange(0, num_episodes + 1, evaluation_interval))
plt.yticks(np.arange(0, 1.1, 0.1))

plt.xlabel('Episodes')
plt.ylabel('Rate')
plt.title(f'ApproxAgent Performance vs {opponent.__class__.__name__} on {rows}x{cols} board in Connect-{game_env.connect}')
plt.legend()
plt.show()  