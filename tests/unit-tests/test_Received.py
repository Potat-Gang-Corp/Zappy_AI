#!/usr/bin/env python3

import unittest
from unittest.mock import Mock
from zappy_ai import command_received, inventory, received_look, reduce_max
import os
import sys

script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, script_dir)

class MockPlayer:
    def __init__(self):
        self.level = 1
        self.view = []
        self.look = False
        self.nb_r = 0
        self.wants_incanting = False
        self.incanting = False
        self.need_to_go = None
        self.starve = None
        self.queue = []
        self.follow = 0
        self.should_stop = None
        self.plant = False

class TestDataRec(Mock):
    def __init__(self, data):
        super().__init__()
        self.decode.return_value = data

class TestCommandReceived(unittest.TestCase):

    def test_end_command(self):
        player = MockPlayer()
        data_rec = TestDataRec("end\n")
        result = command_received(player, data_rec)
        self.assertEqual(result, -10)

    def test_dead_command(self):
        player = MockPlayer()
        data_rec = TestDataRec("dead\n")
        result = command_received(player, data_rec)
        self.assertEqual(result, -1)

    def test_elevation_underway_command(self):
        player = MockPlayer()
        data_rec = TestDataRec("Elevation underway\n")
        result = command_received(player, data_rec)
        self.assertEqual(result, 0)

    def test_message_with_level_change(self):
        player = MockPlayer()
        data_rec = TestDataRec('message "player" c Level 2')
        result = command_received(player, data_rec)
        self.assertEqual(player.nb_r, 1)
        self.assertEqual(player.should_stop, None)

    def test_current_level_up(self):
        player = MockPlayer()
        data_rec = TestDataRec(f"Current level: {player.level + 1}\n")
        result = command_received(player, data_rec)
        self.assertEqual(player.level, 2)
        self.assertEqual(player.view, [])
        self.assertFalse(player.look)
        self.assertEqual(player.nb_r, 0)
        self.assertFalse(player.wants_incanting)
        self.assertFalse(player.incanting)
        self.assertIsNone(player.need_to_go)
        self.assertIsNone(player.starve)
        self.assertIsNone(player.should_stop)
        self.assertTrue(player.plant)

    # Add more tests to cover other scenarios in command_received function

if __name__ == "__main__":
    unittest.main()
