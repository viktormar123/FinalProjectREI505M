import os

if __name__ == '__main__':
    Connect4Game = 'Running/Objects/Tests/GameClass/Connect4Game_test'
    Connect4Win = "Running/Objects/Tests/GameClass/game_win_test.py"
    Connect4Draw = "Running/Objects/Tests/GameClass/game_draw_test.py"
    QLearningAgent = 'Running/Objects/Classes/QLearningAgentClass.py'


    os.system(f'pytest {Connect4Game}.py')
    os.system(f"pytest {Connect4Win}")
    os.system(f"pytest {Connect4Draw}")
    

