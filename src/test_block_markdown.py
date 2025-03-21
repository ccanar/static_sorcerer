import unittest
from block_markdown import markdown_to_blocks


class test_block_markdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        block1 = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        block2 = """
   This is **bolded** paragraph           




       This is another paragraph with _italic_ text and `code` here            






              This is the same paragraph on a new line            






          - This is a list
- with items
"""
        self.assertEqual(
            markdown_to_blocks(block1),
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        self.assertEqual(
            markdown_to_blocks(block2),
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here",
                "This is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


if __name__ == "__main__":
    unittest.main()
