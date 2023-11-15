import sys
import os
import pytest
import numpy as np

# Add the directory above Tests to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from Classes.Connect4Game import Connect4GameClass

@pytest.mark.parametrize("setup, player, expected", [
    # Horizontal win
    (np.array([[1, 1, 1, 1, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]), 1, True),
    # Vertical win
    (np.array([[1, 0, 0, 0, 0], [1, 0, 0, 0, 0], [1, 0, 0, 0, 0], [1, 0, 0, 0, 0]]), 1, True),
    # Positive diagonal win
    (np.array([[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0]]), 1, True),
    # Negative diagonal win
    (np.array([[0, 0, 0, 1, 0], [0, 0, 1, 0, 0], [0, 1, 0, 0, 0], [1, 0, 0, 0, 0]]), 1, True),
    # No win
    (np.array([[1, 1, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]), 1, False),
])
def test_check_winner(setup, player, expected):
    game = Connect4GameClass(rows=4, columns=5)
    game.board = setup
    assert game.check_winner(player) == expected


