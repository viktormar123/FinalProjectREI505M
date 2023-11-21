from matplotlib import pyplot as plt
import numpy as np

from Connect4_Game import Connect4_Game
rows, cols = 6, 7
game_env = Connect4_Game(rows, cols, 4)

from Evaluate_Agent import Evaluate_Agent

from Bots.Random_Bot import Random_Bot
from Bots.AlphaBeta_Agent import AlphaBeta_Agent

RandomAgent = Random_Bot()
AlphaBetaAgent = AlphaBeta_Agent(1)

eval_games = 1000

# print(f'Random vs Random on {rows}x{cols} board:')
# Evaluate_Agent(RandomAgent, RandomAgent, game_env, eval_games) 

print(f'\nRandom vs AlphaBeta:')
Evaluate_Agent(RandomAgent, AlphaBetaAgent, game_env, eval_games) 

print(f'\nAlphaBeta vs Random:')
Evaluate_Agent(AlphaBetaAgent, RandomAgent, game_env, eval_games) 

print(f'\nAlphaBeta vs AlphaBeta:')
Evaluate_Agent(AlphaBetaAgent, AlphaBetaAgent, game_env, eval_games) 
