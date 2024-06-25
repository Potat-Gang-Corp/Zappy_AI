#!/usr/bin/env python3

import unittest
from zappy_ai import find_keyword_in_list
import os
import sys

script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, script_dir)

class TestFindKeywordInList(unittest.TestCase):

    def test_keyword_multiple_occurrences(self):
        strings = ["apple", "banana", "cherry", "date", "apple pie"]
        self.assertEqual(find_keyword_in_list(strings, "apple"), [0, 4])

    def test_keyword_not_present(self):
        strings = ["apple", "banana", "cherry", "date", "apple pie"]
        self.assertEqual(find_keyword_in_list(strings, "orange"), [])

    def test_empty_list(self):
        strings = []
        self.assertEqual(find_keyword_in_list(strings, "apple"), [])

    def test_keyword_as_substring(self):
        strings = ["pineapple", "banana", "cherry", "apple pie"]
        self.assertEqual(find_keyword_in_list(strings, "apple"), [0, 3])

    def test_keyword_as_whole_word(self):
        strings = ["apple", "banana", "cherry", "apple"]
        self.assertEqual(find_keyword_in_list(strings, "apple"), [0, 3])

    def test_keyword_at_various_positions(self):
        strings = ["apple", "banana", "cherry", "apple", "date", "apple pie"]
        self.assertEqual(find_keyword_in_list(strings, "apple"), [0, 3, 5])

if __name__ == "__main__":
    unittest.main()
