import numpy as np
def evaluate_agent_vs_random(agent, env, games=1000):
    results = {'win': 0, 'loss': 0, 'draw': 0}
    for _ in range(games):
        state = env.reset()
        done = False
        while not done:
            # Agent's turn
            possible_actions = env.possible_actions()
            action = agent.choose_action(state, possible_actions)
            state, reward, done = env.step(action)
            if done:
                if env.check_winner(-1 * env.turn): # Agent wins
                    results['win'] += 1
                elif env.check_winner(env.turn):  # Agent loses
                    results['loss'] += 1
                elif env.check_draw(): # Draw
                    results['draw'] += 1
                break

            # Random player's turn
            valid_actions = env.possible_actions()
            random_action = np.random.choice(valid_actions)
            state, reward, done = env.step(random_action)
            # In Connect4, if it's a win for the random player, it's a loss for the agent
            if done:
                if env.check_winner(-1 * env.turn): # Agent wins
                    results['win'] += 1
                elif env.check_winner(env.turn):  # Agent loses
                    results['loss'] += 1
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


