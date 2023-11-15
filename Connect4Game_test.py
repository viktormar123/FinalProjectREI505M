import sys
import os
import pytest
import numpy as np

# Add the directory above Tests to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from Classes.Connect4Game import Connect4GameClass

def test_initialization():
    game = Connect4GameClass()
    assert game.rows == 4
    assert game.columns == 5 
    assert game.in_a_row == 4
    assert game.turn == 1
    assert np.array_equal(game.board, np.zeros((4, 5)))

def test_reset():
    game = Connect4GameClass()
    game.board[0][0] = 1  # Make a move
    game.reset()
    assert np.array_equal(game.board, np.zeros((4, 5)))
    assert game.turn == 1

def test_switch_turn():
    game = Connect4GameClass()
    game.switch_turn()
    assert game.turn == -1
    game.switch_turn()
    assert game.turn == 1

def test_place_token():
    game = Connect4GameClass()
    success = game.place_token(0)
    assert success is True
    assert game.board[-1][0] == 1  # Bottom row should now have a 1
    # Place until column is full
    for _ in range(game.rows - 1):
        game.place_token(0)
    success = game.place_token(0)  # Attempt to place in full column
    assert success is False

def test_is_valid_location():
    game = Connect4GameClass()
    assert game.is_valid_location(0) == True
    # Fill column
    for _ in range(game.rows):
        game.place_token(0)
    assert game.is_valid_location(0) == False

def test_possible_actions():
    game = Connect4GameClass()
    assert game.possible_actions() == [0, 1, 2, 3, 4]
    # Fill column 0
    for _ in range(game.rows):
        game.place_token(0)
    assert game.possible_actions() == [1, 2, 3, 4]

def test_step():
    game = Connect4GameClass()
    board, reward, done = game.step(2)
    assert np.array_equal(board, game.board)
    assert reward == 0  # Places a token near middle so no negative reward.
    assert done is False  # Game is not finished after one step

# Add more tests for check_winner in diagonal and vertical cases, calculate_reward, and count_sequences methods.