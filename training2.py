from Connect4_Game import Connect4_Game
from Evaluate_Agent import Evaluate_Agent
from ApproxAgent_Trainer import ApproxAgent_Trainer
from Bots.LinearApprox_Agent import LinearApprox_Agent
from Bots.Random_Bot import Random_Bot
from Bots.Greedy_Bot import Greedy_Bot
from Bots.AlphaBeta_Agent import AlphaBetaAgent

Connect4_Env = Connect4_Game(6,7,4)
Approx_Agent = LinearApprox_Agent(Connect4_Env)

#Trainer = ApproxAgent_Trainer(Random_Bot(), 20001)
#Weights = Trainer.train()

#Approx_Agent.weights = Weights

#Evaluate_Agent(Approx_Agent, Random_Bot(), Connect4_Env, 1000)
Evaluate_Agent(AlphaBetaAgent(), Random_Bot(),Connect4_Env, 100)
