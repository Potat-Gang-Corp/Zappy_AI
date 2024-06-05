#!/usr/bin/env python3

import unittest
from unittest.mock import Mock, patch
import sys
import os

script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, script_dir)

from zappy_ai import (
    split_by_commas,
    find_keyword_in_list,
    count_words_at_index,
    remove_element,
    send_and_remove,
    going_forward,
    turning_right,
    turning_left,
    looking,
    check_stones,
    can_evolve,
    received_look,
    command_received,
    moving_level_one,
    moving_player,
    command_send,
    Player
)

class TestZappyAI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tests = [
            'test_split_by_commas',
            'test_find_keyword_in_list',
            'test_count_words_at_index',
            'test_remove_element',
            'test_send_and_remove',
            'test_going_forward',
            'test_turning_right',
            'test_turning_left',
            'test_looking',
            'test_check_stones',
            'test_can_evolve',
            'test_received_look',
            'test_command_received',
            'test_moving_level_one',
            'test_moving_player',
            'test_command_send',
        ]
        cls.success_count = 0
        cls.failure_count = 0

    def setUp(self):
        self.player = Player()

    def tearDown(self):
        test_name = self._testMethodName
        result = self.defaultTestResult()
        self._feedErrorsToResult(result, self._outcome.errors)
        if any(error for (test, error) in result.errors):
            print(f"{test_name} ... FAILURE")
            TestZappyAI.failure_count += 1
        elif any(failure for (test, failure) in result.failures):
            print(f"{test_name} ... FAILURE")
            TestZappyAI.failure_count += 1
        else:
            print(f"{test_name} ... SUCCESS")
            TestZappyAI.success_count += 1

    @classmethod
    def tearDownClass(cls):
        print(f"\nTotal tests run: {len(cls.tests)}")
        print(f"Tests succeeded: {cls.success_count}")
        print(f"Tests failed: {cls.failure_count}")

    def test_split_by_commas(self):
        self.assertEqual(split_by_commas('[a, b, c]'), ['a', 'b', 'c'])

    def test_find_keyword_in_list(self):
        strings = ["apple", "banana", "cherry", "date", "apple pie"]
        self.assertEqual(find_keyword_in_list(strings, "apple"), [0, 4])

    def test_count_words_at_index(self):
        strings = ["hello egg player", "hello world", "foo bar egg player"]
        self.assertEqual(count_words_at_index(strings, 0), 1)
        self.assertEqual(count_words_at_index(strings, 1), 2)
        self.assertEqual(count_words_at_index(strings, 2), 2)

    def test_remove_element(self):
        strings = ["hello world", "foo bar"]
        remove_element(strings, 0, "world")
        self.assertEqual(strings, ["hello ", "foo bar"])

    def test_send_and_remove(self):
        client_socket = Mock()
        self.player.view = ["food", "linemate"]
        send_and_remove(client_socket, self.player, 0, "food")
        client_socket.send.assert_called_with(b"Take food\n")
        self.assertEqual(self.player.view, ["", "linemate"])

    def test_going_forward(self):
        client_socket = Mock()
        going_forward(client_socket, self.player)
        client_socket.send.assert_called_with(b"Forward\n")
        self.assertFalse(self.player.look)
        self.assertEqual(self.player.view, [])

    def test_turning_right(self):
        client_socket = Mock()
        turning_right(client_socket, self.player)
        client_socket.send.assert_called_with(b"Right\n")

    def test_turning_left(self):
        client_socket = Mock()
        turning_left(client_socket, self.player)
        client_socket.send.assert_called_with(b"Left\n")

    def test_looking(self):
        client_socket = Mock()
        looking(client_socket, self.player)
        client_socket.send.assert_called_with(b"Look\n")
        self.assertTrue(self.player.look)

    def test_check_stones(self):
        self.player.view = ["linemate", "deraumere"]
        self.assertEqual(check_stones(self.player, 0), "linemate")
        self.player.linemate = 9
        self.assertEqual(check_stones(self.player, 1), "deraumere")

    @patch('zappy_ai.send_and_remove')
    def test_can_evolve(self, mock_send_and_remove):
        client_socket = Mock()
        self.player.view = ["linemate"]
        self.assertTrue(can_evolve(client_socket, self.player))
        self.assertTrue(self.player.incanting)

    def test_received_look(self):
        data_rec = Mock()
        data_rec.decode.return_value = "[linemate, deraumere]"
        received_look(self.player, data_rec)
        self.assertEqual(self.player.view, ["linemate", "deraumere"])

    def test_command_received(self):
        data_rec = Mock()
        data_rec.decode.return_value = "Current level: 2\n"
        self.player.queue.append("Incantation\n")
        command_received(self.player, data_rec)
        self.assertEqual(self.player.level, 2)

    @patch('zappy_ai.going_forward')
    @patch('zappy_ai.turning_left')
    @patch('zappy_ai.turning_right')
    def test_moving_level_one(self, mock_turning_right, mock_turning_left, mock_going_forward):
        client_socket = Mock()
        self.player.view = ["", "", "foo"]
        moving_level_one(client_socket, self.player)
        mock_going_forward.assert_called()

    @patch('zappy_ai.moving_level_one')
    def test_moving_player(self, mock_moving_level_one):
        client_socket = Mock()
        self.player.level = 1
        moving_player(client_socket, self.player)
        mock_moving_level_one.assert_called()

    @patch('zappy_ai.looking')
    def test_command_send(self, mock_looking):
        client_socket = Mock()
        self.player.look = False
        command_send(client_socket, self.player)
        mock_looking.assert_called()

if __name__ == "__main__":
    unittest.main()
