def human_vs_agent_game(connect4, agent):
    connect4.reset()
    game_over = False
    turn = 1  # Human starts as Player 1

    while not game_over:
        connect4.print_board()
        if turn == 1:
            # Human turn
            valid_move = False
            while not valid_move:
                try:
                    human_move = int(input("Your move (0-6): "))  # Adjust if necessary for the number of columns
                    if connect4.is_valid_location(human_move):
                        valid_move = True
                        _, _, game_over = connect4.step(human_move)
                    else:
                        print("Invalid move. Try again.")
                except ValueError:
                    print("Please enter a number between 0 and the number of columns.")
        else:
            # Agent's turn
            valid_actions = [col for col in range(connect4.columns) if connect4.is_valid_location(col)]
            agent_move = agent.choose_action(connect4.board, valid_actions)
            print(f"Agent's move: {agent_move}")
            _, _, game_over = connect4.step(agent_move)

        # Check for a winner or a draw
        if connect4.check_winner(turn):  # Check if the current player won
            game_over = True
            connect4.print_board()
            if turn == 1:
                print("You've won.")
            else:
                print("The agent has won.")
        elif connect4.check_draw():  # Check if the game is a draw
            game_over = True
            connect4.print_board()
            print("It's a draw.")

        # No winner or draw, switch turns
        if not game_over:
            turn *= -1
if __name__ == "__main__":
    connect4_game = Connect4Game(rows=4, columns=5, in_a_row=4)
    human_vs_agent_game(connect4_game, agent_load)