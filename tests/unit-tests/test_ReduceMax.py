#!/usr/bin/env python3

import unittest
from zappy_ai import reduce_max
import os
import sys

script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, script_dir)

class MockPlayer:
    def __init__(self, level, max_linemate, max_deraumere, max_sibur, max_phiras, max_mendiane, max_thystame):
        self.level = level
        self.max_linemate = max_linemate
        self.max_deraumere = max_deraumere
        self.max_sibur = max_sibur
        self.max_phiras = max_phiras
        self.max_mendiane = max_mendiane
        self.max_thystame = max_thystame

class TestReduceMax(unittest.TestCase):

    def test_reduce_max_level_2(self):
        player = MockPlayer(level=2, max_linemate=3, max_deraumere=4, max_sibur=5, max_phiras=6, max_mendiane=7, max_thystame=8)
        reduce_max(player)
        self.assertEqual(player.max_linemate, 2)
        self.assertEqual(player.max_deraumere, 4)
        self.assertEqual(player.max_sibur, 5)
        self.assertEqual(player.max_phiras, 6)
        self.assertEqual(player.max_mendiane, 7)
        self.assertEqual(player.max_thystame, 8)

    def test_reduce_max_level_3(self):
        player = MockPlayer(level=3, max_linemate=3, max_deraumere=4, max_sibur=5, max_phiras=6, max_mendiane=7, max_thystame=8)
        reduce_max(player)
        self.assertEqual(player.max_linemate, 2)
        self.assertEqual(player.max_deraumere, 3)
        self.assertEqual(player.max_sibur, 4)
        self.assertEqual(player.max_phiras, 6)
        self.assertEqual(player.max_mendiane, 7)
        self.assertEqual(player.max_thystame, 8)

    def test_reduce_max_level_4(self):
        player = MockPlayer(level=4, max_linemate=3, max_deraumere=4, max_sibur=5, max_phiras=6, max_mendiane=7, max_thystame=8)
        reduce_max(player)
        self.assertEqual(player.max_linemate, 1)
        self.assertEqual(player.max_deraumere, 4)
        self.assertEqual(player.max_sibur, 4)
        self.assertEqual(player.max_phiras, 4)
        self.assertEqual(player.max_mendiane, 7)
        self.assertEqual(player.max_thystame, 8)

    # Add more tests for other levels (5 to 8) similarly

    def test_reduce_max_other_levels(self):
        player = MockPlayer(level=1, max_linemate=3, max_deraumere=4, max_sibur=5, max_phiras=6, max_mendiane=7, max_thystame=8)
        reduce_max(player)
        self.assertEqual(player.max_linemate, 3)
        self.assertEqual(player.max_deraumere, 4)
        self.assertEqual(player.max_sibur, 5)
        self.assertEqual(player.max_phiras, 6)
        self.assertEqual(player.max_mendiane, 7)
        self.assertEqual(player.max_thystame, 8)

if __name__ == "__main__":
    unittest.main()
