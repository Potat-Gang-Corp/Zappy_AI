#!/usr/bin/env python3

import unittest
from zappy_ai import check_stones
import os
import sys

script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, script_dir)

class MockPlayer:
    def __init__(self):
        self.view = []
        self.linemate = 0
        self.max_linemate = 5
        # Initialize other attributes as needed for the tests

class TestCheckStones(unittest.TestCase):

    def setUp(self):
        self.player = MockPlayer()

    def test_food_needed(self):
        self.player.view = ["food"]
        self.assertEqual(check_stones(self.player, 0), "food")

    def test_linemate_needed(self):
        self.player.view = ["linemate"]
        self.assertEqual(check_stones(self.player, 0), "linemate")

    def test_linemate_not_needed(self):
        self.player.view = ["linemate"]
        self.player.linemate = 5
        self.assertIsNone(check_stones(self.player, 0))

    # Add similar tests for other stone types (deraumere, sibur, mendiane, phiras, thystame)

    def test_index_out_of_range(self):
        self.assertIsNone(check_stones(self.player, 1))

    def test_empty_view(self):
        self.assertIsNone(check_stones(self.player, 0))

if __name__ == "__main__":
    unittest.main()
