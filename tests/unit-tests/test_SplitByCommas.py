#!/usr/bin/env python3

import unittest
from zappy_ai import split_by_commas
import os
import sys

script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, script_dir)

class TestSplitByCommas(unittest.TestCase):

    def test_basic_split(self):
        self.assertEqual(split_by_commas('[a, b, c]'), ['a', 'b', 'c'])

    def test_split_with_extra_spaces(self):
        self.assertEqual(split_by_commas('[  a  , b , c  ]'), ['a', 'b', 'c'])

    def test_empty_brackets(self):
        self.assertEqual(split_by_commas('[]'), [])

    def test_no_spaces(self):
        self.assertEqual(split_by_commas('[a,b,c]'), ['a', 'b', 'c'])

    def test_internal_spaces(self):
        self.assertEqual(split_by_commas('[a, b c, d e f]'), ['a', 'b c', 'd e f'])

    def test_empty_elements(self):
        self.assertEqual(split_by_commas('[a, , b, , c]'), ['a', '', 'b', '', 'c'])

if __name__ == "__main__":
    unittest.main()
