#!/usr/bin/env python3

import unittest
from unittest.mock import Mock
from zappy_ai import looking, received_look
import os
import sys

script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, script_dir)

class MockClientSocket(Mock):
    def send(self, data):
        pass

class MockPlayer:
    def __init__(self):
        self.look = False
        self.queue = []

class TestLooking(unittest.TestCase):

    def setUp(self):
        self.client_socket = MockClientSocket()
        self.player = MockPlayer()

    def test_looking_command_sent(self):
        looking(self.client_socket, self.player)
        self.assertIn("Look\n", self.player.queue)

    def test_player_look_set_to_true(self):
        looking(self.client_socket, self.player)
        self.assertTrue(self.player.look)

    def test_socket_send_called(self):
        with unittest.mock.patch.object(self.client_socket, 'send') as mock_send:
            looking(self.client_socket, self.player)
            mock_send.assert_called_once_with(b"Look\n")

class TestReceivedLook(unittest.TestCase):

    def test_received_look_ko(self):
        player = MockPlayer()
        data_rec = Mock()
        data_rec.decode.return_value = "ko\n"
        received_look(player, data_rec)
        self.assertFalse(player.look)
        self.assertEqual(player.view, [])

    def test_received_look_valid_data(self):
        player = MockPlayer()
        data_rec = Mock()
        data_rec.decode.return_value = "[linemate, deraumere]"
        received_look(player, data_rec)
        self.assertTrue(player.look)  # Should remain True if not "ko"
        self.assertEqual(player.view, ["linemate", "deraumere"])

    def test_received_look_empty_data(self):
        player = MockPlayer()
        data_rec = Mock()
        data_rec.decode.return_value = ""
        received_look(player, data_rec)
        self.assertTrue(player.look)  # Should remain True if data is empty
        self.assertEqual(player.view, [])

if __name__ == "__main__":
    unittest.main()
