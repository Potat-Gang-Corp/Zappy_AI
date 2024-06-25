#!/usr/bin/env python3

import unittest
from unittest.mock import Mock
from zappy_ai import going_forward, turning_right, turning_left, make_random_move, moving_level, go_to_need, moving_player
import os
import sys

script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, script_dir)

class MockClientSocket(Mock):
    def send(self, data):
        pass

class MockPlayer:
    def __init__(self):
        self.queue = []

class TestMovements(unittest.TestCase):

    def setUp(self):
        self.client_socket = MockClientSocket()
        self.player = MockPlayer()

    def test_going_forward(self):
        going_forward(self.client_socket, self.player)
        self.assertEqual(self.player.queue, ["Forward\n"])

    def test_turning_right(self):
        turning_right(self.client_socket, self.player)
        self.assertEqual(self.player.queue, ["Right\n"])

    def test_turning_left(self):
        turning_left(self.client_socket, self.player)
        self.assertEqual(self.player.queue, ["Left\n"])

    def test_socket_send_called(self):
        with unittest.mock.patch.object(self.client_socket, 'send') as mock_send:
            going_forward(self.client_socket, self.player)
            mock_send.assert_called_once_with(b"Forward\n")
            
            turning_right(self.client_socket, self.player)
            mock_send.assert_called_with(b"Right\n")
            
            turning_left(self.client_socket, self.player)
            mock_send.assert_called_with(b"Left\n")

class TestMovementFunctions(unittest.TestCase):

    def setUp(self):
        self.client_socket = Mock()
        self.player = Mock()
        self.player.view = []
        self.player.queue = []

    def test_make_random_move(self):
        make_random_move(self.client_socket, self.player)
        self.assertTrue(self.client_socket.send.called)
        self.assertTrue(self.player.queue)

    def test_moving_level_random_move(self):
        self.player.level = 1
        self.player.view = ["player"]
        moving_level(self.client_socket, self.player)
        self.assertTrue(self.client_socket.send.called)
        self.assertTrue(self.player.queue)

    def test_go_to_need(self):
        self.player.need_to_go = 0
        go_to_need(self.client_socket, self.player)
        self.assertTrue(self.client_socket.send.called)
        self.assertTrue(self.player.queue)

    def test_moving_player_with_need(self):
        self.player.need_to_go = 1
        moving_player(self.client_socket, self.player)
        self.assertTrue(self.client_socket.send.called)
        self.assertTrue(self.player.queue)

    def test_moving_player_no_need(self):
        self.player.need_to_go = None
        moving_player(self.client_socket, self.player)
        self.assertTrue(self.client_socket.send.called)
        self.assertTrue(self.player.queue)

    def test_make_random_move_called_twice_in_moving_level(self):
        self.player.level = 2
        self.player.view = ["player"]
        with unittest.mock.patch('random.choice', side_effect=[lambda s, p: None, lambda s, p: None]):
            moving_level(self.client_socket, self.player)
            self.assertEqual(self.client_socket.send.call_count, 2)

if __name__ == "__main__":
    unittest.main()
