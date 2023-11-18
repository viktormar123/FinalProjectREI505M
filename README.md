# Connect4 Reinforcement Learning Project

## Project Overview
This repository contains the Connect4 Reinforcement Learning Project developed as part of the REI505M Machine Learning course at the University of Iceland. Our project focuses on training reinforcement learning agents to play the game of Connect4, experimenting with various algorithms and strategies.

## Usage
- `Connect4_Game.py`: Script to initialize and manage the game environment.
- `QLearning_Agent.py` and `LinearApprox_Agent.py`: Implementations of the reinforcement learning agents.
- `QAgent_Trainer.py` and `ApproxAgent_Trainer.py`: Scripts to train the respective agents.
- `Evaluate_Agent.py`: Evaluate the performance of the agents against various opponents.
- `Random_Bot.py`, `Greedy_Bot.py`, `AlphaBeta_Agent.py`: Different types of bots for evaluation and training purposes.
- `Human_vs_Agent.py`: Play Connect4 against a trained agent.

## Playing Against Agents
To play against a trained agent, run the `Human_vs_Agent.py` script:
```python
python Human_vs_Agent.py 
```
Follow the on-screen instructions to make your moves against the agent.

## Overview of Agents and Algorithms
- **Q-Learning Agent**: Uses tabular Q-learning for decision-making.
- **Linear Approximation Agent**: Employs linear function approximation in decision-making.
- **Random Bot**: Makes moves randomly, useful as a baseline opponent.
- **Greedy Bot**: Chooses moves based on immediate gains.
- **Alpha Beta Bot**: Uses the Alpha-Beta pruning strategy for more strategic gameplay.

## Training and Evaluation
Train the agents using the provided training scripts and evaluate their performance with `Evaluate_Agent.py`. Example:
```python
python QAgent_Trainer.py
python Evaluate_Agent.py
```

## Contribution and Feedback
We welcome contributions and feedback. Please submit pull requests for contributions and use the issue tracker for feedback and bug reports.

## Authors and Acknowledgements
This project was developed by Björn Thor Stefánsson, Kristján Sölvi Örnólfsson, and Viktor Már Guðmundsson. Special thanks to Steinn Guðmundsson our professor at the University of Iceland.
