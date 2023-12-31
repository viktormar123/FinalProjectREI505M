from Connect4_Game import Connect4_Game
from QAgent_Trainer import QAgent_Trainer
from Evaluate_Agent import Evaluate_Agent
from ApproxAgent_Trainer import ApproxAgent_Trainer

from Bots.QLearning_Agent import QLearning_Agent
from Bots.Random_Bot import Random_Bot
from Bots.Greedy_Bot import Greedy_Bot
from Bots.AlphaBeta_Agent import AlphaBetaAgent

import os
import pickle
import time
import sys
from configs_extra.training_config import initialize_variables

if __name__ == "__main__":
    #Timer
    start_time = time.time() # Get the current time at the start of your code block
    # Variable Initialization
    args = [x.lower() for x in sys.argv]
    train, eval, print_q, num_episodes, epsilon, epsilon_decay, min_epsilon, q_table_name = initialize_variables(args)

    #Train model if specified.
    if train:
        Trainer = QAgent_Trainer(opponent=AlphaBetaAgent,
                                num_episodes=num_episodes if num_episodes else 500,
                                epsilon_decay=epsilon_decay if epsilon_decay else 0.99999,
                                min_epsilon=min_epsilon if min_epsilon else 0.05,
                                q_table_name=q_table_name,
                                connect=4,
                                )
        Q_size = Trainer.train()
        print("epsilon decay: ", Trainer.agent.epsilon_decay, "min epsilon: ", Trainer.agent.min_epsilon)

    # Evaluate the agent if specified.
    if eval:
        cwd = os.getcwd() + "/Q_tables/"
        #q_table_path_list =   [cwd + "/Q_tables/" + x for x in ["random_200k.pkl", "random_50k.pkl", "random_100k.pkl", "random_30k.pkl", "random_10k.pkl"]]
        q_table_path_list = [cwd + "mvsm_50k.pkl"]
        for q_table_path in q_table_path_list:
            with open(q_table_path, 'rb') as f:
                q_table = pickle.load(f)
                agent = QLearning_Agent()
                agent.load_q_table(q_table)

                Evaluate_Agent(agent, Random_Bot(), Connect4_Game())
            
        end_time = time.time()  # Get the current time after your code block ends
        elapsed_time = end_time - start_time  # Calculate the elapsed time

    # Print the Q-table if specified.
    if print_q:
        import pickle
        file_path = q_table_path_list[0]
        with open(file_path, 'rb') as file:
            data = pickle.load(file)
            for line in data.items():
                print(line)

    print(f"The code took {elapsed_time:0.3f} seconds to run")