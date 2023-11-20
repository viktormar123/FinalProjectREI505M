from matplotlib import pyplot as plt

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

game_env = Connect4_Game(6, 7, 4)

# Training Linear Approx Agent vs Random Bot and plotting the results:

ApproxAgent = LinearApprox_Agent(game_env, 0.5, 1, 0.2, 1, 0.2)
RandomAgent = Random_Bot()

num_episodes = 2000
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

                next_state, done = RandomAgent.play(game_env, done)

                ApproxAgent.update(current_state, action, reward, next_state, done, game_env.possible_actions())
                current_state = next_state

            if episode % 250 == 0:
                print(f"\nEpisode {episode} complete.")
                results = Evaluate_Agent(ApproxAgent, RandomAgent, game_env, games = 50)
                
                # Store the results
                win_rates.append(results['win'] / 50)
                loss_rates.append(results['loss'] / 50)
                draw_rates.append(results['draw'] / 50)
                evaluation_episodes.append(episode)
                
                
plt.figure(figsize=(10, 6))
plt.plot(evaluation_episodes, win_rates, label='Win Rate')
plt.plot(evaluation_episodes, loss_rates, label='Loss Rate')
plt.plot(evaluation_episodes, draw_rates, label='Draw Rate')
plt.xlabel('Episodes')
plt.ylabel('Rate')
plt.title('ApproxAgent Performance Over Time vs RandomAgent')
plt.legend()
plt.show()
                