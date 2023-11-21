import numpy as np

def Evaluate_Agent(agent, opponent, env, games=10):
    results = {'win': 0, 'loss': 0, 'draw': 0}
    for game_num in range(games):
        env.reset()

        while True:
            # Agent's turn
            action = agent.choose_action(env)
            env.place_token(action)
            if env.check_winner(1): # Agent wins
                results['win'] += 1
                break
            elif env.check_winner(2):  # Agent loses
                results['loss'] += 1
                print('Something is wrong with Evaluate_Agent, agent loses after placing his own token')
                break
            elif env.check_draw(): # Draw
                results['draw'] += 1
                break
            
            env.switch_turn()
            # Opponent's turn
            opponents_action = opponent.choose_action(env)
            env.place_token(opponents_action)
            
            # In Connect4, if it's a win for the random player, it's a loss for the agent    
            if env.check_winner(2): # Agent wins
                results['loss'] += 1
                break
            elif env.check_winner(1):  # Agent loses
                results['win'] += 1
                print('\nSomething is wrong with Evaluate_Agent, opponent loses after placing his own token')
                env.print_board()                
                break
            elif env.check_draw(): # Draw
                results['draw'] += 1
                break
            
            env.switch_turn()

    win_rate = results['win'] / games
    loss_rate = results['loss'] / games
    draw_rate = results['draw'] / games
    print(f"Results after {games} games:")
    print(f"Wins: {results['win']} ({win_rate*100:.2f}%)")
    print(f"Losses: {results['loss']} ({loss_rate*100:.2f}%)")
    print(f"Draws: {results['draw']} ({draw_rate*100:.2f}%)")
    return results
