# tests/test_cube.py
from cube import Cube


def test_initial_cube_is_solved():
    c = Cube()
    assert c.is_solved()


def test_move_and_inverse_return_to_solved():
    pairs = [
        ("U", "U'"),
        ("D", "D'"),
        ("F", "F'"),
        ("B", "B'"),
        ("L", "L'"),
        ("R", "R'"),
    ]
    for move, inv in pairs:
        c = Cube()
        c.apply_alg(f"{move} {inv}")
        assert c.is_solved()


def test_double_moves_twice_return_to_solved():
    moves2 = ["U2", "D2", "F2", "B2", "L2", "R2"]
    for m2 in moves2:
        c = Cube()
        c.apply_alg(f"{m2} {m2}")
        assert c.is_solved()


def test_random_scramble_length_and_structure():
    c = Cube()
    length = 25
    alg = c.random_scramble(length)
    moves = alg.split()
    assert len(moves) == length
    # faces stay of size 9
    for face in c.faces.values():
        assert len(face) == 9
