#!/usr/bin/env python3
import unittest
from convert_to_md import convert_to_md


class ConvertTestCase(unittest.TestCase):
    def test_convert_to_markdown(self):
        for exported, expected_md, expected_ret_val in [("""* Heading1
    * Heading2
        * Paragraph1
            * item1
            * item2
        * Paragraph2
""", """# Heading1

## Heading2

Paragraph1

* item1
* item2

Paragraph2

""", 0)]:
            ret_val, md = convert_to_md(iter(exported.split("\n")), 1, 1)
            self.assertEqual(expected_ret_val, ret_val)
            self.assertEqual(expected_md, md)


if __name__ == "__main__":
    unittest.main()
