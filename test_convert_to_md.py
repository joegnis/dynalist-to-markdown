#!/usr/bin/env python3
import unittest
from convert_to_md import convert_to_md


class ConvertTestCase(unittest.TestCase):
    def test_convert_to_markdown_without_comment(self):
        for exported, expected_md, start_hd, hd_depth, expected_ret_val in [
            ("""* Heading1
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
""", 1, 1, 0),
            ("""* Heading1
    * Paragraph1
        * item1
* Heading2
    * Paragraph2
        * item2
""", """## Heading1

Paragraph1

* item1

## Heading2

Paragraph2

* item2
""", 2, 0, 0)
        ]:
            with self.subTest(input=exported,
                              start_heading=start_hd,
                              heading_depth=hd_depth,
                              expected_ret_val=expected_ret_val):
                ret_val, md = convert_to_md(iter(exported.split("\n")),
                                            start_hd, hd_depth)
                self.assertEqual(expected_ret_val, ret_val)
                self.assertEqual(expected_md, md)

    def test_convert_to_md_with_comment(self):
        for exported, expected_md, start_hd, hd_depth, expected_ret_val in [
            ("""* Heading1
  CommentH1
    * Heading2
      CommentH2
        * Paragraph1
          CommentP1
            * Item1
              CommentItem1
            * Item2
        * Paragraph2
          CommentP2
""", """# Heading1

CommentH1

## Heading2

CommentH2

Paragraph1
* CommentP1
* Item1
    * CommentItem1
* Item2

Paragraph2
* CommentP2
""", 1, 1, 0),
            ("""* Heading1
  ```some
  code1
  ```
""", """# Heading1

```
some
code1
```
""", 1, 1, 0),
            ("""* Heading1
    * Paragraph1
      ```somecode1
      ```
""", """# Heading1

Paragraph1
```
somecode1
```
""", 1, 0, 0),
            ("""* Heading1
  `onelinecode`
""", """# Heading1

`onelinecode`
""", 1, 1, 0),
            ("""* Heading1
    * Paragraph1
        * Item1
          ```some
          code
          ```
""", """# Heading1

Paragraph1

* Item1
  ```
  some
  code
  ```
""", 1, 0, 0),
        ]:
            with self.subTest(input=exported,
                              start_heading=start_hd,
                              heading_depth=hd_depth,
                              expected_ret_val=expected_ret_val):
                ret_val, md = convert_to_md(iter(exported.split("\n")),
                                            start_hd, hd_depth)
                self.assertEqual(expected_ret_val, ret_val)
                self.assertEqual(expected_md, md)


if __name__ == "__main__":
    unittest.main()
