import numpy as np
def Evaluate_Agent(agent, opponent, env, games=10):
    results = {'win': 0, 'loss': 0, 'draw': 0}
    for _ in range(games):
        state = env.reset()
        done = False
        while not done:
            # Agent's turn
            possible_actions = env.possible_actions()
            action = agent.choose_action(env)
            state, reward, done = env.step(action)
            print(env.turn)
            if done:
                if env.check_winner(3 - env.turn): # Agent wins
                    print("AgentWin")
                    results['win'] += 1
                elif env.check_winner(env.turn):  # Agent loses
                    print("AgentLose")
                    results['loss'] += 1
                elif env.check_draw(): # Draw
                    results['draw'] += 1
                break

            # Opponents turn
            if not done:
                possible_actions = env.possible_actions()
                opponents_action = opponent.choose_action(env)
                state, reward, done = env.step(opponents_action)
            print(env.turn)
            # In Connect4, if it's a win for the random player, it's a loss for the agent    
            if done: 
                if env.check_winner(3 - env.turn): # Agent wins
                    print("AgentLose")
                    results['loss'] += 1
                elif env.check_winner(env.turn):  # Agent loses
                    print("AgentWin")
                    results['win'] += 1
                elif env.check_draw(): # Draw
                    results['draw'] += 1
                break
            
    win_rate = results['win'] / games
    loss_rate = results['loss'] / games
    draw_rate = results['draw'] / games
    print(f"Results after {games} games:")
    print(f"Wins: {results['win']} ({win_rate*100:.2f}%)")
    print(f"Losses: {results['loss']} ({loss_rate*100:.2f}%)")
    print(f"Draws: {results['draw']} ({draw_rate*100:.2f}%)")
    return results


