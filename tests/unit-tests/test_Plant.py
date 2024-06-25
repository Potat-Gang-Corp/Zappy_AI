#!/usr/bin/env python3

import unittest
from unittest.mock import Mock
from zappy_ai import plant_egg
import os
import sys

script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, script_dir)

class TestPlantEgg(unittest.TestCase):

    def test_plant_egg(self):
        client_socket = Mock()
        player = Mock()
        plant_egg(client_socket, player)
        client_socket.send.assert_called_once_with(b"Fork\n")
        self.assertEqual(player.queue, ["Fork\n"])

    def test_invalid_client_socket(self):
        client_socket = None
        player = Mock()
        with self.assertRaises(AttributeError):
            plant_egg(client_socket, player)

    def test_invalid_player(self):
        client_socket = Mock()
        player = None
        with self.assertRaises(AttributeError):
            plant_egg(client_socket, player)

if __name__ == "__main__":
    unittest.main()
