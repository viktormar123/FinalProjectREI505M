import numpy as np

def Evaluate_Agent(agent, opponent, env, games=10):
    results = {'win': 0, 'loss': 0, 'draw': 0}
    for game_num in range(games):
        state = env.reset()
        done = False

        while not done:
            # Agent's turn
            possible_actions = env.possible_actions()
            action = agent.choose_action(env)
            state, reward, done = env.step(action)
            if done:
                if env.check_winner(1): # Agent wins
                    results['win'] += 1
                elif env.check_winner(2):  # Agent loses
                    results['loss'] += 1
                elif env.check_draw(): # Draw
                    results['draw'] += 1
                break

            # Opponent's turn
            if not done:
                possible_actions = env.possible_actions()
                opponents_action = opponent.choose_action(env)
                state, reward, done = env.step(opponents_action)
            
            # In Connect4, if it's a win for the random player, it's a loss for the agent    
            if done: 
                if env.check_winner(2): # Agent wins
                    results['loss'] += 1
                elif env.check_winner(1):  # Agent loses
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
