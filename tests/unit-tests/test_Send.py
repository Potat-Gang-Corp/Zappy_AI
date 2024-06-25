#!/usr/bin/env python3

import unittest
from unittest.mock import Mock, patch
from zappy_ai import command_send
import os
import sys

script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, script_dir)

class TestCommandSend(unittest.TestCase):

    @patch('zappy_ai.plant_egg')
    def test_plant_egg_called(self, mock_plant_egg):
        player = Mock()
        player.plant = True
        client_socket = Mock()
        command_send(client_socket, player)
        mock_plant_egg.assert_called_once_with(client_socket, player)
        self.assertFalse(player.plant)

    @patch('zappy_ai.incant_nb', return_value=True)
    @patch('zappy_ai.client_socket')
    def test_incantation_true(self, mock_client_socket, mock_incant_nb):
        player = Mock()
        player.wants_incanting = True
        player.should_stop = None
        player.queue = []
        command_send(mock_client_socket, player)
        mock_client_socket.send.assert_called_once()
        self.assertTrue(player.incanting)
        self.assertEqual(player.nb_r, 0)
        self.assertFalse(player.wants_incanting)

    @patch('zappy_ai.client_socket')
    def test_broadcast_r(self, mock_client_socket):
        player = Mock()
        player.wants_incanting = True
        player.should_stop = 2
        player.queue = []
        command_send(mock_client_socket, player)
        mock_client_socket.send.assert_called_once()
        self.assertTrue(player.queue[0].startswith('Broadcast "Level'))
        self.assertFalse(player.incanting)
        self.assertEqual(player.nb_r, 0)
        self.assertTrue(player.wants_incanting)

    @patch('zappy_ai.looking')
    def test_look_false(self, mock_looking):
        player = Mock()
        player.look = False
        player.queue = []
        client_socket = Mock()
        command_send(client_socket, player)
        mock_looking.assert_called_once_with(client_socket, player)

    @patch('zappy_ai.can_evolve', return_value=True)
    def test_can_evolve_true(self, mock_can_evolve):
        player = Mock()
        player.look = True
        player.view = []
        player.queue = []
        client_socket = Mock()
        command_send(client_socket, player)
        mock_can_evolve.assert_called_once_with(client_socket, player)

    @patch('zappy_ai.client_socket')
    def test_inventory_b_false(self, mock_client_socket):
        player = Mock()
        player.inventory_b = False
        player.look = True
        player.view = []
        player.queue = []
        command_send(mock_client_socket, player)
        mock_client_socket.send.assert_not_called()

    @patch('zappy_ai.send_and_remove')
    @patch('zappy_ai.check_stones', return_value='stone')
    def test_send_and_remove_food_present(self, mock_check_stones, mock_send_and_remove):
        player = Mock()
        player.look = True
        player.view = ['food, 1']
        player.queue = []
        client_socket = Mock()
        command_send(client_socket, player)
        mock_send_and_remove.assert_called_once_with(client_socket, player, 0, 'food')
        mock_check_stones.assert_not_called()

    @patch('zappy_ai.check_stones', return_value='stone')
    @patch('zappy_ai.moving_player')
    def test_check_stones_not_food(self, mock_moving_player, mock_check_stones):
        player = Mock()
        player.look = True
        player.view = ['stone, 1']
        player.queue = []
        client_socket = Mock()
        command_send(client_socket, player)
        mock_moving_player.assert_called_once_with(client_socket, player)
        mock_check_stones.assert_called_once_with(player, 0)

if __name__ == "__main__":
    unittest.main()
