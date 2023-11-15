import sys
import os
import pytest
import numpy as np

# Add the directory above Tests to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from Classes.Connect4Game import Connect4GameClass

@pytest.mark.parametrize("board, expected", [
    # Full board w  ith alternating tokens, no winner, should be a draw
    (np.array([[2, 1, 1, 1, 2], [2, 1, 2, 1, 2], [1, 2, 1, 2, 1], [2, 1, 2, 1, 2]]), True),
    # Full board with the last move being a winning move, should not be a draw
    (np.array([[1, 2, 1, 1, 1], [2, 1, 2, 1, 2], [1, 2, 1, 2, 2], [2, 1, 2, 1, 2]]), True),
    # Full board with a different pattern, no winner, should be a draw
    (np.array([[1, 1, 2, 2, 1], [1, 2, 2, 2, 1], [2, 1, 2, 1, 2], [1, 2, 1, 2, 1]]), True),
])
def test_check_draw(board, expected):
    game = Connect4GameClass(rows=4, columns=5)
    game.board = board
    assert game.check_draw() == expected