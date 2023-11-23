from matplotlib import pyplot as plt
import numpy as np

from Connect4_Game import Connect4_Game

from Bots.LinearApprox_Agent import LinearApprox_Agent
from Bots.QLearning_Agent import QLearning_Agent
from Bots.Random_Bot import Random_Bot
from Bots.Greedy_Bot import Greedy_Bot
from Bots.AlphaBeta_Agent import AlphaBeta_Agent
from Bots.MiniMax_Agent import MiniMax_Agent

from ApproxAgent_Trainer import ApproxAgent_Trainer
from QAgent_Trainer import QAgent_Trainer

from Evaluate_Agent import Evaluate_Agent
from Human_vs_Agent import Human_vs_Agent

# Define the parameters for game enviroment and training 
rows, cols, connect = 6, 7, 4 # Smaller board size, less computation
alpha = 0.001 # 0.001 

# Define the game environment and ApproxAgent
game_env = Connect4_Game(rows, cols, connect) 
ApproxAgent = LinearApprox_Agent(game_env, alpha, 0.97, 0.6, 0.999, 0.02) #0.99 0.6 0.999 0.02

# Define the opponent, both for training and evaluation
opponent = MiniMax_Agent(rows, cols, 1, True)
# opponent = Random_Bot()
# Load the weights into Approx agent
load = 'RandomP2'
loaded_weights = np.load('ApproxWeights/' + load + '.npy')
print(f'Loaded weights of {load} are {loaded_weights}\n')
ApproxAgent.weights = loaded_weights

# Parameters for training and evaluation
num_episodes = 10000 #  10000   20000, 1000, 500
evaluation_interval = 1000 # 1000
evaluation_games = 1000 # 500

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
                
# Evaluate_Agent(ApproxAgent, Random_Bot(), game_env, games = evaluation_games)                                          
plt.figure(figsize=(10, 6))
plt.plot(evaluation_episodes, win_rates, label='Win Rate') # Winrate for player 1
plt.plot(evaluation_episodes, loss_rates, label='Loss Rate') # Loss rate for player 1
plt.plot(evaluation_episodes, draw_rates, label='Draw Rate') # Draw rate

plt.xlim(-1, num_episodes)
plt.ylim(0, 1)
plt.xticks(np.arange(0, num_episodes + 1, evaluation_interval))
plt.yticks(np.arange(0, 1.1, 0.1))

plt.xlabel('Episodes')
plt.ylabel('Rate')
plt.title(f'ApproxAgent Performance vs {opponent.__class__.__name__} on {rows}x{cols} board in Connect-{game_env.connect}')
plt.legend()
plt.grid(axis = 'y')
plt.show()  

# Save the weights after training
# np.save('ApproxWeights/MiniMaxP2d2.npy', ApproxAgent.weights)

# Human_vs_Agent(game_env, ApproxAgent, 2)

# Weigts of the agent after training
print(f'Weights of the ApproxAgent after training:\n {ApproxAgent.weights}')
