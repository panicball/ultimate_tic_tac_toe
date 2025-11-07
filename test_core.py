import unittest
from ..core import make_move, check_winner, is_full, render


class TestCore(unittest.TestCase):
    def setUp(self):
        self.board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]

    def tearDown(self):
        self.board = None

    @classmethod
    def setUpClass(cls):
        print("in set up class")

    @classmethod
    def tearDownClass(cls):
        print("in teardown class")

    def test_make_moves(self):
        self.assertEqual(make_move(board=self.board, row=0, column=0, player_value="X"), True, "")
        self.assertFalse(make_move(board=[['O', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']], row=0, column=0, player_value="X"))

        with self.assertRaises(IndexError):
            make_move(board=self.board, row=2, column=3, player_value="X")
            make_move(board=self.board, row=-1, column=3, player_value="X")

    def test_check_winner(self):
        self.assertEqual(check_winner(board=[['O', ' ', ' '], [' ', 'O', ' '], [' ', ' ', 'O']], current_player="X"), None)
        self.assertEqual(check_winner(board=[['O', ' ', ' '], [' ', 'O', ' '], [' ', ' ', 'O']], current_player="O"), "O")
        self.assertEqual(check_winner(board=[['O', 'O', 'O']], current_player="O"), "O")
        self.assertEqual(check_winner(board=[[]], current_player="O"), None)

    def test_is_full(self):
        self.assertFalse(is_full(board=[['O', ' ', ' '], [' ', 'O', ' '], [' ', ' ', 'O']]))
        self.assertTrue(is_full(board=[['O', 'X', ' X'], ['X', 'O', 'X'], ['X', 'X', 'O']]))
        self.assertEqual(is_full(board=[['O', 'O', 'O']]), True)
        self.assertEqual(is_full(board=[[]]), True)

    def test_render(self):
        self.assertEqual(render(board=[['O', ' ', ' '], [' ', 'O', ' '], [' ', ' ', 'O']]), 'O| | \n-----\n |O| \n-----\n | |O')
        self.assertEqual(render(board=[['O', 'X', 'X'], ['X', 'O', 'X'], ['X', 'X', 'O']]), 'O|X|X\n-----\nX|O|X\n-----\nX|X|O')
        self.assertEqual(render(board=[['O', 'O', 'O']]), 'O|O|O')
        self.assertEqual(render(board=[[]]), '')


if __name__ == '__main__':
    unittest.main()
