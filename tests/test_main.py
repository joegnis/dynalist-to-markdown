#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from dynalist_to_md.__main__ import main
from io import StringIO


class MainTestCase(unittest.TestCase):
    @patch('sys.stdout', new_callable=StringIO)
    def test_simple_input(self, mock_stdout):
        main(["script_name", "* Heading"])
        self.assertEqual("# Heading\n\n", mock_stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
