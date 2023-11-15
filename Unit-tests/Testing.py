import os

if __name__ == '__main__':
    Connect4Game = 'Connect-4_test'
    Connect4Win = "Win_test.py"
    Connect4Draw = "Draw_test.py"
    QLearningAgent = 'Bots/Q-Learning_Agent.py'


    os.system(f'pytest {Connect4Game}.py')
    os.system(f"pytest {Connect4Win}")
    os.system(f"pytest {Connect4Draw}")
    

