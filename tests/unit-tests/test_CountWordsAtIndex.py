#!/usr/bin/env python3

import unittest
from zappy_ai import count_words_at_index
import os
import sys

script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, script_dir)

class TestCountWordsAtIndex(unittest.TestCase):

    def test_valid_index_with_words(self):
        strings = ["hello world", "foo bar", "baz qux"]
        self.assertEqual(count_words_at_index(strings, 0), 2)
        self.assertEqual(count_words_at_index(strings, 1), 2)
        self.assertEqual(count_words_at_index(strings, 2), 2)

    def test_valid_index_with_excluded_words(self):
        strings = ["hello egg player", "egg foo player", "player bar egg"]
        self.assertEqual(count_words_at_index(strings, 0), 1)
        self.assertEqual(count_words_at_index(strings, 1), 1)
        self.assertEqual(count_words_at_index(strings, 2), 1)

    def test_index_out_of_range(self):
        strings = ["hello world", "foo bar", "baz qux"]
        self.assertEqual(count_words_at_index(strings, 3), 0)
        self.assertEqual(count_words_at_index(strings, -1), 0)

    def test_empty_list(self):
        strings = []
        self.assertEqual(count_words_at_index(strings, 0), 0)

    def test_empty_string_at_index(self):
        strings = ["hello world", "", "baz qux"]
        self.assertEqual(count_words_at_index(strings, 1), 0)

    def test_string_with_only_excluded_words(self):
        strings = ["egg player", "egg", "player"]
        self.assertEqual(count_words_at_index(strings, 0), 0)
        self.assertEqual(count_words_at_index(strings, 1), 0)
        self.assertEqual(count_words_at_index(strings, 2), 0)

if __name__ == "__main__":
    unittest.main()
