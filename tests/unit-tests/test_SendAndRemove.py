#!/usr/bin/env python3

import unittest
from unittest.mock import Mock
from zappy_ai import send_and_remove
import os
import sys

script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, script_dir)

class MockClientSocket(Mock):
    def send(self, data):
        pass

class MockPlayer:
    def __init__(self):
        self.view = []
        self.queue = []

class TestSendAndRemove(unittest.TestCase):

    def setUp(self):
        self.client_socket = MockClientSocket()
        self.player = MockPlayer()

    def test_send_and_remove(self):
        self.player.view = ["food", "linemate"]
        send_and_remove(self.client_socket, self.player, 0, "food")
        self.assertEqual(self.player.view, ["", "linemate"])
        self.assertEqual(self.player.queue, ["Take food\n"])

    def test_socket_send_called(self):
        with unittest.mock.patch.object(self.client_socket, 'send') as mock_send:
            self.player.view = ["food", "linemate"]
            send_and_remove(self.client_socket, self.player, 0, "food")
            mock_send.assert_called_once_with(b"Take food\n")

    def test_remove_element_called(self):
        with unittest.mock.patch('zappy_ai.remove_element') as mock_remove_element:
            self.player.view = ["food", "linemate"]
            send_and_remove(self.client_socket, self.player, 0, "food")
            mock_remove_element.assert_called_once_with(self.player.view, 0, "food")

    def test_empty_view_after_remove(self):
        self.player.view = ["food"]
        send_and_remove(self.client_socket, self.player, 0, "food")
        self.assertEqual(self.player.view, [""])
        
    def test_add_to_queue(self):
        self.player.view = ["food", "linemate"]
        send_and_remove(self.client_socket, self.player, 0, "food")
        self.assertEqual(self.player.queue, ["Take food\n"])

if __name__ == "__main__":
    unittest.main()
