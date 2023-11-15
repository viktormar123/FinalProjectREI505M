from Objects.Classes.Connect4Game import Connect4GameClass
from Objects.Classes.Connect4Trainer import Connect4TrainerClass
from Objects.Classes.Bots.RandomBot import RandomBotClass
import os
import pickle

# Evaluators
from Objects.Functions.evaluate_agent import eval_agent
from Objects.Functions.evaluate_model_vs_random import evaluate_agent_vs_random
from Objects.Classes.Bots.RandomBot import RandomBotClass
from Objects.Classes.Bots.GreedyBot import GreedyBotClass
import matplotlib.pyplot as plt
import time
import sys

# Agent
from Objects.Classes.Agent import AgentClass

if __name__ == "__main__":
    #To run:
    train, eval, print_q = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    start_time = time.time()
    if train == 1:
        Trainer = Connect4TrainerClass(opponent=None, num_episodes=500000, espilon_decay=0.999996, min_epsilon=0.05, q_table_name="mvsm_500k.pkl")
        Q_size = Trainer.train()
        plt.plot(Q_size)
        plt.show(block=False)
        print("epsilon decay: ", Trainer.agent.epsilon_decay, "min epsilon: ", Trainer.agent.min_epsilon)

    # Evaluate the agent
    cwd = os.getcwd() + "/Q_tables/"
    #q_table_path_list =   [cwd + "/Q_tables/" + x for x in ["random_200k.pkl", "random_50k.pkl", "random_100k.pkl", "random_30k.pkl", "random_10k.pkl"]]
    q_table_path_list = [cwd + "mvsm_1Mk.pkl"]
    if eval == 1:   
        for q_table_path in q_table_path_list:
            with open(q_table_path, 'rb') as f:
                q_table = pickle.load(f)
                agent = AgentClass(q_table)
                eval_agent(agent, RandomBotClass(), Connect4GameClass())
                eval_agent(agent, GreedyBotClass(), Connect4GameClass())  
                eval_agent(RandomBotClass(), agent, Connect4GameClass())
                eval_agent(GreedyBotClass(), agent, Connect4GameClass())

                #eval_agent(RandomBotClass(), RandomBotClass(), Connect4GameClass())
                #eval_agent(GreedyBotClass(), RandomBotClass(), Connect4GameClass())
                #eval_agent(GreedyBotClass(),agent, Connect4GameClass())
                #eval_agent(RandomBotClass(), GreedyBotClass(), Connect4GameClass())
                #eval_agent(GreedyBotClass(), GreedyBotClass(), Connect4GameClass())
        
    end_time = time.time()  # Get the current time after your code block ends
    elapsed_time = end_time - start_time  # Calculate the elapsed time

    print(f"The code took {elapsed_time} seconds to run")

#ERed e = 0.99997, min_e = 0.05
#Emid e = 0.999985, min_e = 0.05
#EBlue e = 0.99999, min_e = 0.05
#ENorm e=0.999995, min_e = 0.05

    if print_q == 1:
        import pickle

        file_path = q_table_path_list[0]

        with open(file_path, 'rb') as file:
            data = pickle.load(file)
            for line in data.items():
                print(line)
