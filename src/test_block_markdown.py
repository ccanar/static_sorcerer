import unittest
from block_markdown import BlockType, markdown_to_blocks, block_to_block_type


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

    def test_block_to_block_type_heading(self):
        text1 = "# One"
        text2 = "## Two"
        text3 = "### Three"
        text4 = "#### Four"
        text5 = "##### Five"
        text6 = "###### Six"
        text7 = "####### Seven"
        text8 = "#Nospace"
        text9 = "Nothing"

        self.assertEqual(block_to_block_type(text1), BlockType.HEADING)
        self.assertEqual(block_to_block_type(text2), BlockType.HEADING)
        self.assertEqual(block_to_block_type(text3), BlockType.HEADING)
        self.assertEqual(block_to_block_type(text4), BlockType.HEADING)
        self.assertEqual(block_to_block_type(text5), BlockType.HEADING)
        self.assertEqual(block_to_block_type(text6), BlockType.HEADING)
        self.assertNotEqual(block_to_block_type(text7), BlockType.HEADING)
        self.assertNotEqual(block_to_block_type(text8), BlockType.HEADING)
        self.assertNotEqual(block_to_block_type(text9), BlockType.HEADING)

    def test_block_to_block_type_code(self):
        text1 = "```code```"
        text2 = "```code\nsome more\nand even more```"
        text3 = "```not code"
        text4 = "not code 2```"
        text5 = "``NOT```"
        text6 = "```NOT2`"
        text7 = "Just text"
        text8 = "# Just heading"

        self.assertEqual(block_to_block_type(text1), BlockType.CODE)
        self.assertEqual(block_to_block_type(text2), BlockType.CODE)
        self.assertNotEqual(block_to_block_type(text3), BlockType.CODE)
        self.assertNotEqual(block_to_block_type(text4), BlockType.CODE)
        self.assertNotEqual(block_to_block_type(text5), BlockType.CODE)
        self.assertNotEqual(block_to_block_type(text6), BlockType.CODE)
        self.assertNotEqual(block_to_block_type(text7), BlockType.CODE)
        self.assertNotEqual(block_to_block_type(text8), BlockType.CODE)

    def test_block_to_block_type_quote(self):
        text1 = "123"
        text2 = "123 "
        text3 = "Just text"
        text4 = "# a heading"
        text5 = "```here, have some code```"
        text6 = "1. One\n2. Two\n3. Three"
        text7 = ">Just one line"
        text8 = "> Another line"
        text9 = """>A line
>Another one
>And one more"""
        text10 = """>Starts good
Ends bad"""
        text11 = """Starts bad
>good ending"""

        self.assertNotEqual(block_to_block_type(text1), BlockType.QUOTE)
        self.assertNotEqual(block_to_block_type(text2), BlockType.QUOTE)
        self.assertNotEqual(block_to_block_type(text3), BlockType.QUOTE)
        self.assertNotEqual(block_to_block_type(text4), BlockType.QUOTE)
        self.assertNotEqual(block_to_block_type(text5), BlockType.QUOTE)
        self.assertNotEqual(block_to_block_type(text6), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(text7), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(text8), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(text9), BlockType.QUOTE)
        self.assertNotEqual(block_to_block_type(text10), BlockType.QUOTE)
        self.assertNotEqual(block_to_block_type(text11), BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        text1 = "123"
        text2 = "123 "
        text3 = "Just text"
        text4 = "# a heading"
        text5 = "```here, have some code```"
        text6 = "1. One\n2. Two\n3. Three"

        self.assertNotEqual(block_to_block_type(text1), BlockType.UNORDERED_LIST)
        self.assertNotEqual(block_to_block_type(text2), BlockType.UNORDERED_LIST)
        self.assertNotEqual(block_to_block_type(text3), BlockType.UNORDERED_LIST)
        self.assertNotEqual(block_to_block_type(text4), BlockType.UNORDERED_LIST)
        self.assertNotEqual(block_to_block_type(text5), BlockType.UNORDERED_LIST)
        self.assertNotEqual(block_to_block_type(text6), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        text1 = "123"
        text2 = "123 "
        text3 = "Just text"
        text4 = "# a heading"
        text5 = "```here, have some code```"

        self.assertNotEqual(block_to_block_type(text1), BlockType.ORDERED_LIST)
        self.assertNotEqual(block_to_block_type(text2), BlockType.ORDERED_LIST)
        self.assertNotEqual(block_to_block_type(text3), BlockType.ORDERED_LIST)
        self.assertNotEqual(block_to_block_type(text4), BlockType.ORDERED_LIST)
        self.assertNotEqual(block_to_block_type(text5), BlockType.ORDERED_LIST)

    def test_block_to_block_type_paragraph(self):
        text1 = "1. Smile"
        text2 = "- 123"
        text3 = "# a heading"
        text4 = "```here, have some code```"
        text5 = "1. One\n2. Two\n3. Three"

        self.assertNotEqual(block_to_block_type(text1), BlockType.PARAGRAPH)
        self.assertNotEqual(block_to_block_type(text2), BlockType.PARAGRAPH)
        self.assertNotEqual(block_to_block_type(text3), BlockType.PARAGRAPH)
        self.assertNotEqual(block_to_block_type(text4), BlockType.PARAGRAPH)
        self.assertNotEqual(block_to_block_type(text5), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
