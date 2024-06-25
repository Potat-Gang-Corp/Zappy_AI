#!/usr/bin/env python3

import unittest
from unittest.mock import Mock
from zappy_ai import (
    check_level_two,
    check_level_three,
    check_level_four,
    check_level_five,
    check_level_six,
    check_level_seven,
    can_evolve,
    incant_nb,
    Player
)
import os
import sys

script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, script_dir)

class TestIncantNb(unittest.TestCase):

    def test_level_2(self):
        self.assertFalse(incant_nb(MockPlayer(level=2, nb_r=0)))
        self.assertFalse(incant_nb(MockPlayer(level=2, nb_r=1)))
        self.assertTrue(incant_nb(MockPlayer(level=2, nb_r=2)))
        self.assertTrue(incant_nb(MockPlayer(level=2, nb_r=3)))

    def test_level_3(self):
        self.assertFalse(incant_nb(MockPlayer(level=3, nb_r=0)))
        self.assertFalse(incant_nb(MockPlayer(level=3, nb_r=1)))
        self.assertFalse(incant_nb(MockPlayer(level=3, nb_r=3)))
        self.assertTrue(incant_nb(MockPlayer(level=3, nb_r=4)))
        self.assertTrue(incant_nb(MockPlayer(level=3, nb_r=5)))

    def test_level_4(self):
        self.assertFalse(incant_nb(MockPlayer(level=4, nb_r=0)))
        self.assertFalse(incant_nb(MockPlayer(level=4, nb_r=3)))
        self.assertTrue(incant_nb(MockPlayer(level=4, nb_r=4)))
        self.assertTrue(incant_nb(MockPlayer(level=4, nb_r=5)))

    def test_level_5(self):
        self.assertFalse(incant_nb(MockPlayer(level=5, nb_r=0)))
        self.assertFalse(incant_nb(MockPlayer(level=5, nb_r=5)))
        self.assertTrue(incant_nb(MockPlayer(level=5, nb_r=6)))
        self.assertTrue(incant_nb(MockPlayer(level=5, nb_r=7)))

    def test_level_6(self):
        self.assertFalse(incant_nb(MockPlayer(level=6, nb_r=0)))
        self.assertFalse(incant_nb(MockPlayer(level=6, nb_r=5)))
        self.assertTrue(incant_nb(MockPlayer(level=6, nb_r=6)))
        self.assertTrue(incant_nb(MockPlayer(level=6, nb_r=7)))

    def test_level_7(self):
        self.assertFalse(incant_nb(MockPlayer(level=7, nb_r=0)))
        self.assertFalse(incant_nb(MockPlayer(level=7, nb_r=6)))
        self.assertTrue(incant_nb(MockPlayer(level=7, nb_r=7)))
        self.assertTrue(incant_nb(MockPlayer(level=7, nb_r=8)))

    def test_level_not_in_condition(self):
        self.assertFalse(incant_nb(MockPlayer(level=1, nb_r=2)))
        self.assertFalse(incant_nb(MockPlayer(level=8, nb_r=7)))

class MockPlayer:
    def __init__(self, level, nb_r):
        self.level = level
        self.nb_r = nb_r

class TestCheckLevelTwo(unittest.TestCase):

    def setUp(self):
        # Setup mock client socket
        self.client_socket = Mock()
        # Setup mock Player instance
        self.player = Player()
        self.player.view = ["linemate"]  # Example setup, adjust as per your Player class

    def test_can_evolve_to_level_two(self):
        # Test case where player can evolve to level two
        self.player.view = ["linemate"]  # Simulate player's view
        self.player.linemate = 1  # Simulate player having 1 linemate
        result = check_level_two(self.player, self.client_socket)
        self.assertTrue(result)
        self.assertTrue(self.player.wants_incanting)  # Check player state
        self.assertIn("Broadcast \"Level 2 r\"", self.player.queue)  # Check command sent

    def test_cannot_evolve_to_level_two_insufficient_resources(self):
        # Test case where player cannot evolve due to insufficient resources
        self.player.view = ["linemate"]  # Simulate player's view
        self.player.linemate = 0  # Simulate player having 0 linemate
        result = check_level_two(self.player, self.client_socket)
        self.assertFalse(result)
        self.assertFalse(self.player.wants_incanting)  # Check player state

    def test_cannot_evolve_to_level_two_no_view(self):
        # Test case where player has no view (should not attempt to evolve)
        self.player.view = []  # Simulate player's view being empty
        result = check_level_two(self.player, self.client_socket)
        self.assertFalse(result)
        self.assertFalse(self.player.wants_incanting)  # Check player state


class TestCheckLevelThree(unittest.TestCase):

    def setUp(self):
        # Setup mock client socket
        self.client_socket = Mock()
        # Setup mock Player instance
        self.player = Player()
        self.player.view = ["linemate", "deraumere", "sibur", "phiras"]  # Example setup, adjust as per your Player class

    def test_can_evolve_to_level_three(self):
        # Test case where player can evolve to level three
        self.player.linemate = 1
        self.player.deraumere = 1
        self.player.sibur = 1
        self.player.phiras = 2
        result = check_level_three(self.player, self.client_socket)
        self.assertTrue(result)
        self.assertTrue(self.player.wants_incanting)
        self.assertIn("Broadcast \"Level 3 r\"", self.player.queue)

    def test_cannot_evolve_to_level_three_insufficient_resources(self):
        # Test case where player cannot evolve due to insufficient resources
        self.player.linemate = 0
        self.player.deraumere = 0
        self.player.sibur = 0
        self.player.phiras = 1
        result = check_level_three(self.player, self.client_socket)
        self.assertFalse(result)
        self.assertFalse(self.player.wants_incanting)

    def test_cannot_evolve_to_level_three_no_view(self):
        # Test case where player has no view (should not attempt to evolve)
        self.player.view = []
        result = check_level_three(self.player, self.client_socket)
        self.assertFalse(result)
        self.assertFalse(self.player.wants_incanting)

    # Add more tests as needed for edge cases and specific scenarios

class TestCheckLevelFour(unittest.TestCase):
    # Repeat the structure for check_level_four, check_level_five, check_level_six, and check_level_seven

    def setUp(self):
        self.client_socket = Mock()
        self.player = Player()
        self.player.view = ["linemate", "deraumere", "sibur", "phiras", "thystame"]  # Example setup

    def test_can_evolve_to_level_four(self):
        self.player.linemate = 1
        self.player.deraumere = 2
        self.player.sibur = 2
        self.player.phiras = 1
        self.player.thystame = 1
        result = check_level_four(self.player, self.client_socket)
        self.assertTrue(result)
        self.assertTrue(self.player.wants_incanting)
        self.assertIn("Broadcast \"Level 4 r\"", self.player.queue)

class TestCheckLevelFive(unittest.TestCase):

    def setUp(self):
        # Setup mock client socket
        self.client_socket = Mock()
        # Setup mock Player instance
        self.player = Player()
        self.player.view = ["linemate", "deraumere", "sibur", "phiras", "mendiane"]  # Example setup, adjust as per your Player class

    def test_can_evolve_to_level_five(self):
        # Test case where player can evolve to level five
        self.player.linemate = 1
        self.player.deraumere = 1
        self.player.sibur = 2
        self.player.phiras = 1
        self.player.mendiane = 3
        result = check_level_five(self.player, self.client_socket)
        self.assertTrue(result)
        self.assertTrue(self.player.wants_incanting)
        self.assertIn("Broadcast \"Level 5 r\"", self.player.queue)

    def test_cannot_evolve_to_level_five_insufficient_resources(self):
        # Test case where player cannot evolve due to insufficient resources
        self.player.linemate = 0
        self.player.deraumere = 0
        self.player.sibur = 1
        self.player.phiras = 1
        self.player.mendiane = 2
        result = check_level_five(self.player, self.client_socket)
        self.assertFalse(result)
        self.assertFalse(self.player.wants_incanting)

    def test_cannot_evolve_to_level_five_no_view(self):
        # Test case where player has no view (should not attempt to evolve)
        self.player.view = []
        result = check_level_five(self.player, self.client_socket)
        self.assertFalse(result)
        self.assertFalse(self.player.wants_incanting)

class TestCheckLevelSix(unittest.TestCase):

    def setUp(self):
        # Setup mock client socket
        self.client_socket = Mock()
        # Setup mock Player instance
        self.player = Player()
        self.player.view = ["linemate", "deraumere", "sibur", "mendiane"]  # Example setup, adjust as per your Player class

    def test_can_evolve_to_level_six(self):
        # Test case where player can evolve to level six
        self.player.linemate = 1
        self.player.deraumere = 2
        self.player.sibur = 1
        self.player.mendiane = 3
        result = check_level_six(self.player, self.client_socket)
        self.assertTrue(result)
        self.assertTrue(self.player.wants_incanting)
        self.assertIn("Broadcast \"Level 6 r\"", self.player.queue)

    def test_cannot_evolve_to_level_six_insufficient_resources(self):
        # Test case where player cannot evolve due to insufficient resources
        self.player.linemate = 0
        self.player.deraumere = 1
        self.player.sibur = 1
        self.player.mendiane = 2
        result = check_level_six(self.player, self.client_socket)
        self.assertFalse(result)
        self.assertFalse(self.player.wants_incanting)

    def test_cannot_evolve_to_level_six_no_view(self):
        # Test case where player has no view (should not attempt to evolve)
        self.player.view = []
        result = check_level_six(self.player, self.client_socket)
        self.assertFalse(result)
        self.assertFalse(self.player.wants_incanting)

class TestCheckLevelSeven(unittest.TestCase):

    def setUp(self):
        # Setup mock client socket
        self.client_socket = Mock()
        # Setup mock Player instance
        self.player = Player()
        self.player.view = ["linemate", "deraumere", "sibur", "mendiane", "phiras", "thystame"]  # Example setup, adjust as per your Player class

    def test_can_evolve_to_level_seven(self):
        # Test case where player can evolve to level seven
        self.player.linemate = 1
        self.player.deraumere = 2
        self.player.sibur = 3
        self.player.mendiane = 2
        self.player.phiras = 1
        self.player.thystame = 1
        result = check_level_seven(self.player, self.client_socket)
        self.assertTrue(result)
        self.assertTrue(self.player.wants_incanting)  # Check player state
        self.assertIn("Broadcast \"Level 7 r\"", self.player.queue)  # Check command sent

    def test_cannot_evolve_to_level_seven_insufficient_resources(self):
        # Test case where player cannot evolve due to insufficient resources
        self.player.linemate = 0
        self.player.deraumere = 1
        self.player.sibur = 3
        self.player.mendiane = 2
        self.player.phiras = 1
        self.player.thystame = 1
        result = check_level_seven(self.player, self.client_socket)
        self.assertFalse(result)
        self.assertFalse(self.player.wants_incanting)  # Check player state

    def test_cannot_evolve_to_level_seven_no_view(self):
        # Test case where player has no view (should not attempt to evolve)
        self.player.view = []
        result = check_level_seven(self.player, self.client_socket)
        self.assertFalse(result)
        self.assertFalse(self.player.wants_incanting)

class TestCanEvolve(unittest.TestCase):

    def setUp(self):
        # Setup mock client socket
        self.client_socket = Mock()
        # Setup mock Player instance
        self.player = Player()
        self.player.level = 1  # Example setup, adjust as per your Player class
        self.player.view = ["linemate", "player"]  # Example setup, adjust as per your Player class

    def test_can_evolve_to_next_level(self):
        # Test case where player can evolve to next level
        self.player.view = ["linemate"]  # Player has required resources for level 1
        result = can_evolve(self.client_socket, self.player)
        self.assertTrue(result)
        self.assertTrue(self.player.incanting)  # Check player state
        self.assertIn("Incantation\n", self.player.queue)  # Check command sent

    def test_cannot_evolve_already_incanting(self):
        # Test case where player is already incanting
        self.player.incanting = True
        result = can_evolve(self.client_socket, self.player)
        self.assertFalse(result)
        self.assertTrue(self.player.incanting)  # Check player state

    def test_cannot_evolve_no_required_resources(self):
        # Test case where player does not have required resources
        self.player.view = []  # Player has no resources in view
        result = can_evolve(self.client_socket, self.player)
        self.assertFalse(result)
        self.assertFalse(self.player.incanting)
    # Add more tests for edge cases, such as exact resource requirements, etc.

if __name__ == "__main__":
    unittest.main()
