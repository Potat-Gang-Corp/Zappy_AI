#!/usr/bin/env python3

import unittest
from unittest.mock import Mock
from zappy_ai import inventory
import os
import sys

script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, script_dir)

class MockPlayer:
    def __init__(self):
        self.starve = 0  # Initial value doesn't really matter for tests
        self.level = 1    # Mocking level for testing purposes

class TestInventory(unittest.TestCase):

    def test_update_food_quantity(self):
        player = MockPlayer()
        data_rec = "[food 5, linemate 2, deraumere 3]"
        inventory(player, data_rec)
        self.assertEqual(player.starve, 5)

    def test_no_food_information(self):
        player = MockPlayer()
        data_rec = "[linemate 2, deraumere 3]"
        inventory(player, data_rec)
        self.assertEqual(player.starve, 0)  # Should remain unchanged

    def test_empty_data(self):
        player = MockPlayer()
        data_rec = ""
        inventory(player, data_rec)
        self.assertEqual(player.starve, 0)  # Should remain unchanged

if __name__ == "__main__":
    unittest.main()
