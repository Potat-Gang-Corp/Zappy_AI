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
        self.deraumere = 0
        self.max_deraumere = 5
        self.sibur = 0
        self.max_sibur = 5
        self.mendiane = 0
        self.max_mendiane = 5
        self.phiras = 0
        self.max_phiras = 5
        self.thystame = 0
        self.max_thystame = 5


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

    def test_deraumere_needed(self):
        self.player.view = ["deraumere"]
        self.assertEqual(check_stones(self.player, 0), "deraumere")

    def test_deraumere_not_needed(self):
        self.player.view = ["deraumere"]
        self.player.deraumere = 5
        self.assertIsNone(check_stones(self.player, 0))

    def test_sibur_needed(self):
        self.player.view = ["sibur"]
        self.assertEqual(check_stones(self.player, 0), "sibur")

    def test_sibur_not_needed(self):
        self.player.view = ["sibur"]
        self.player.sibur = 5
        self.assertIsNone(check_stones(self.player, 0))

    def test_mendiane_needed(self):
        self.player.view = ["mendiane"]
        self.assertEqual(check_stones(self.player, 0), "mendiane")

    def test_mendiane_not_needed(self):
        self.player.view = ["mendiane"]
        self.player.mendiane = 5
        self.assertIsNone(check_stones(self.player, 0))

    def test_phiras_needed(self):
        self.player.view = ["phiras"]
        self.assertEqual(check_stones(self.player, 0), "phiras")

    def test_phiras_not_needed(self):
        self.player.view = ["phiras"]
        self.player.phiras = 5
        self.assertIsNone(check_stones(self.player, 0))

    def test_thystame_needed(self):
        self.player.view = ["thystame"]
        self.assertEqual(check_stones(self.player, 0), "thystame")

    def test_thystame_not_needed(self):
        self.player.view = ["thystame"]
        self.player.thystame = 5
        self.assertIsNone(check_stones(self.player, 0))

    def test_index_out_of_range(self):
        self.assertIsNone(check_stones(self.player, 1))

    def test_empty_view(self):
        self.assertIsNone(check_stones(self.player, 0))

if __name__ == "__main__":
    unittest.main()
