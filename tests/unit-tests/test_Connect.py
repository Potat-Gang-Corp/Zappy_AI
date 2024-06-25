#!/usr/bin/env python3

import unittest
from unittest.mock import Mock, patch
from io import BytesIO
# import socket
# import sys
# import time
# import select
from zappy_ai import netcat_client, command_received, command_send
import os
import sys

script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, script_dir)

class MockClientSocket:
    def __init__(self):
        self.buffer = BytesIO()
        self.connected = False

    def connect(self, host_port):
        self.connected = True

    def send(self, data):
        self.buffer.write(data)

    def recv(self, bufsize):
        return self.buffer.getvalue()

    def close(self):
        self.connected = False

class TestNetcatClient(unittest.TestCase):

    @patch('socket.socket', side_effect=MockClientSocket)
    def test_netcat_client(self, mock_socket):
        host = "localhost"
        port = 12345
        name = "test_team"

        # Simulate server responses
        server_responses = [
            b"Welcome to the game!\n",
            b"This team is full, please wait\n",
            b"Current level: 2\n",
            b"ko\n",
            b"end\n"
        ]

        mock_socket_instance = mock_socket.return_value

        # Test with server responses
        mock_socket_instance.buffer.write(server_responses[0])
        mock_socket_instance.buffer.write(server_responses[1])
        mock_socket_instance.buffer.write(server_responses[2])
        mock_socket_instance.buffer.write(server_responses[3])
        mock_socket_instance.buffer.write(server_responses[4])

        with patch('sys.stdout', new_callable=BytesIO) as mock_stdout:
            with patch('time.sleep', return_value=None):
                with patch('select.select', return_value=([mock_socket_instance], [], [])):
                    result = netcat_client(host, port, name)

        output = mock_stdout.getvalue().strip().split("\n")
        self.assertIn("Received: Welcome to the game!", output)
        self.assertIn(f"Sending : {name}", output)
        self.assertIn("Player session ended", output)

    @patch('socket.socket', side_effect=MockClientSocket)
    def test_keyboard_interrupt(self, mock_socket):
        host = "localhost"
        port = 12345
        name = "test_team"

        mock_socket_instance = mock_socket.return_value

        # Simulate KeyboardInterrupt
        with patch('sys.stdout', new_callable=BytesIO):
            with patch('time.sleep', side_effect=KeyboardInterrupt):
                result = netcat_client(host, port, name)

        self.assertFalse(mock_socket_instance.connected)

if __name__ == "__main__":
    unittest.main()
