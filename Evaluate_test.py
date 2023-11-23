from matplotlib import pyplot as plt
import numpy as np

from Connect4_Game import Connect4_Game
rows, cols = 6, 7
game_env = Connect4_Game(rows, cols, 4)

from Evaluate_Agent import Evaluate_Agent

from Bots.Random_Bot import Random_Bot
from Bots.AlphaBeta_Agent import AlphaBeta_Agent
from Bots.MiniMax_Agent import MiniMax_Agent

RandomAgent = Random_Bot()
MiniMaxAgentP2 = MiniMax_Agent(rows, cols, 1, True)
MiniMaxAgentP1 = MiniMax_Agent(rows, cols, 1, False)

eval_games = 10000

# print(f'Random vs Random on {rows}x{cols} board:')
# Evaluate_Agent(RandomAgent, RandomAgent, game_env, eval_games) 

print(f'\nRandom vs MiniMax:')
Evaluate_Agent(RandomAgent, MiniMaxAgentP2, game_env, eval_games) 

print(f'\nMiniMax vs Random:')
Evaluate_Agent(MiniMaxAgentP1, RandomAgent, game_env, eval_games) 

print(f'\nMiniMax vs MiniMax:')
Evaluate_Agent(MiniMaxAgentP1, MiniMaxAgentP2, game_env, eval_games) 
