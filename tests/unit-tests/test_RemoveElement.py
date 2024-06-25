#!/usr/bin/env python3

import unittest
from zappy_ai import remove_element
import os
import sys

script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, script_dir)

class TestRemoveElement(unittest.TestCase):

    def test_remove_existing_element(self):
        strings = ["hello world", "foo bar", "baz qux"]
        remove_element(strings, 0, "world")
        self.assertEqual(strings, ["hello ", "foo bar", "baz qux"])

    def test_remove_nonexistent_element(self):
        strings = ["hello world", "foo bar", "baz qux"]
        remove_element(strings, 1, "world")
        self.assertEqual(strings, ["hello world", "foo bar", "baz qux"])

    def test_remove_first_occurrence_only(self):
        strings = ["hello world world", "foo bar", "baz qux"]
        remove_element(strings, 0, "world")
        self.assertEqual(strings, ["hello  world", "foo bar", "baz qux"])

    def test_index_out_of_range(self):
        strings = ["hello world", "foo bar", "baz qux"]
        with self.assertLogs(level='INFO') as log:
            remove_element(strings, 3, "world")
            self.assertIn("Index out of range (remove_element).", log.output[0])

    def test_empty_list(self):
        strings = []
        with self.assertLogs(level='INFO') as log:
            remove_element(strings, 0, "world")
            self.assertIn("Index out of range (remove_element).", log.output[0])

    def test_remove_entire_string(self):
        strings = ["hello world", "foo bar", "baz qux"]
        remove_element(strings, 2, "baz qux")
        self.assertEqual(strings, ["hello world", "foo bar", ""])

if __name__ == "__main__":
    unittest.main()
