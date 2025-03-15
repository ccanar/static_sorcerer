import unittest

from textnode import TextNode, TextType

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimeter,
    split_nodes_images,
    split_nodes_links,
    text_to_textnodes,
)


class TestInlineMarkdown(unittest.TestCase):
    def test_split_nodes_delimeter(self):
        empty_list = []
        new_list = split_nodes_delimeter(empty_list, "`", TextType.CODE)
        self.assertEqual(new_list, [])

        list1 = [TextNode("Text with no delimeter", TextType.NORMAL)]
        new_list2 = split_nodes_delimeter(list1, "`", TextType.CODE)
        self.assertEqual(
            new_list2, [TextNode("Text with no delimeter", TextType.NORMAL)]
        )
        list2 = [TextNode("THIS WAS BOLD", TextType.BOLD)]
        new_list3 = split_nodes_delimeter(list2, "`", TextType.CODE)
        self.assertEqual(new_list3, [TextNode("THIS WAS BOLD", TextType.BOLD)])

        list3 = [
            TextNode("THIS WAS BOLD", TextType.BOLD),
            TextNode("This has **bold** text.", TextType.NORMAL),
        ]
        new_list4 = split_nodes_delimeter(list3, "**", TextType.BOLD)
        self.assertEqual(
            new_list4,
            [
                TextNode("THIS WAS BOLD", TextType.BOLD),
                TextNode("This has ", TextType.NORMAL),
                TextNode("bold", TextType.BOLD),
                TextNode(" text.", TextType.NORMAL),
            ],
        )

        list4 = [
            TextNode("THIS WAS BOLD", TextType.BOLD),
            TextNode("This has **bold** text and some `code, too`.", TextType.NORMAL),
            TextNode("some code", TextType.CODE),
            TextNode("**b** ale i `c`", TextType.NORMAL),
        ]
        new_list5 = split_nodes_delimeter(list4, "**", TextType.BOLD)
        self.assertEqual(
            new_list5,
            [
                TextNode("THIS WAS BOLD", TextType.BOLD),
                TextNode("This has ", TextType.NORMAL),
                TextNode("bold", TextType.BOLD),
                TextNode(" text and some `code, too`.", TextType.NORMAL),
                TextNode("some code", TextType.CODE),
                TextNode("b", TextType.BOLD),
                TextNode(" ale i `c`", TextType.NORMAL),
            ],
        )

        list5 = [
            TextNode("THIS WAS BOLD", TextType.BOLD),
            TextNode("This has **bold** text and some `code, too`.", TextType.NORMAL),
            TextNode("some code", TextType.CODE),
            TextNode("**b** ale i `c`", TextType.NORMAL),
        ]
        new_list6 = split_nodes_delimeter(list5, "`", TextType.CODE)
        self.assertEqual(
            new_list6,
            [
                TextNode("THIS WAS BOLD", TextType.BOLD),
                TextNode("This has **bold** text and some ", TextType.NORMAL),
                TextNode("code, too", TextType.CODE),
                TextNode(".", TextType.NORMAL),
                TextNode("some code", TextType.CODE),
                TextNode("**b** ale i ", TextType.NORMAL),
                TextNode("c", TextType.CODE),
            ],
        )

    def test_extract_markdown_images(self):
        md_txt1 = ""
        md_txt2 = "There is no image in this bitch"
        md_txt3 = "This one is a bait [bait](baiting more)"
        md_txt4 = "Here is an image, tho ![THE IMAGE](https://the.image.com/theimage2)"
        md_txt5 = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        md_txt6 = "Ohh, a bait! ![Trololo]"
        md_txt7 = "Ohh, a bait v2! ![Trololo]()"
        md_txt8 = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(md_txt1), [])
        self.assertEqual(extract_markdown_images(md_txt2), [])
        self.assertEqual(extract_markdown_images(md_txt3), [])
        self.assertEqual(
            extract_markdown_images(md_txt4),
            [("THE IMAGE", "https://the.image.com/theimage2")],
        )
        self.assertEqual(
            extract_markdown_images(md_txt5),
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )
        self.assertEqual(extract_markdown_images(md_txt6), [])
        self.assertEqual(extract_markdown_images(md_txt7), [("Trololo", "")])
        self.assertEqual(
            extract_markdown_images(md_txt8),
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif")],
        )

    def test_extract_markdown_links(self):
        md_txt1 = ""
        md_txt2 = "There is no image in this bitch"
        md_txt3 = "This one is a bait [bait](baiting more)"
        md_txt4 = "Here is an image, tho [THE IMAGE](https://the.image.com/theimage2)"
        md_txt5 = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        md_txt6 = "Ohh, a bait! [Trololo]"
        md_txt7 = "Ohh, a bait v2! [Trololo]()"
        md_txt8 = "Normal text with [normal link](https://normal.link)"
        self.assertEqual(extract_markdown_links(md_txt1), [])
        self.assertEqual(extract_markdown_links(md_txt2), [])
        self.assertEqual(extract_markdown_links(md_txt3), [("bait", "baiting more")])
        self.assertEqual(
            extract_markdown_links(md_txt4),
            [("THE IMAGE", "https://the.image.com/theimage2")],
        )
        self.assertEqual(
            extract_markdown_links(md_txt5),
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )
        self.assertEqual(extract_markdown_links(md_txt6), [])
        self.assertEqual(extract_markdown_links(md_txt7), [("Trololo", "")])
        self.assertEqual(
            extract_markdown_links(md_txt8), [("normal link", "https://normal.link")]
        )

    def test_split_nodes_images(self):
        list1 = [
            TextNode("THIS WAS BOLD", TextType.BOLD),
            TextNode("This has **bold** text and some `code, too`.", TextType.NORMAL),
            TextNode("some code", TextType.CODE),
            TextNode("**b** ale i `c`", TextType.NORMAL),
        ]
        self.assertEqual(
            split_nodes_images(list1),
            [
                TextNode("THIS WAS BOLD", TextType.BOLD),
                TextNode(
                    "This has **bold** text and some `code, too`.", TextType.NORMAL
                ),
                TextNode("some code", TextType.CODE),
                TextNode("**b** ale i `c`", TextType.NORMAL),
            ],
        )

        list2 = [
            TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
                TextType.NORMAL,
            )
        ]

        split_nodes1 = split_nodes_images(list2)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            split_nodes1,
        )
        list3 = [
            TextNode(
                "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
                TextType.NORMAL,
            )
        ]

        split_nodes2 = split_nodes_images(list3)
        self.assertListEqual(
            [
                TextNode(
                    "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
                    TextType.NORMAL,
                )
            ],
            split_nodes2,
        )

        list4 = [
            TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
                TextType.NORMAL,
            )
        ]

        split_nodes3 = split_nodes_images(list4)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    " and another [second image](https://i.imgur.com/3elNhQu.png)",
                    TextType.NORMAL,
                ),
            ],
            split_nodes3,
        )

        list5 = [
            TextNode(
                "This is text with an ![](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
                TextType.NORMAL,
            )
        ]

        split_nodes4 = split_nodes_images(list5)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    " and another [second image](https://i.imgur.com/3elNhQu.png)",
                    TextType.NORMAL,
                ),
            ],
            split_nodes4,
        )

    def test_split_nodes_links(self):
        list = [
            TextNode("Bold", TextType.BOLD),
            TextNode(
                "Normal text with [normal link](https://normal.link)",
                TextType.NORMAL,
            ),
        ]
        self.assertEqual(
            split_nodes_links(list),
            [
                TextNode("Bold", TextType.BOLD),
                TextNode("Normal text with ", TextType.NORMAL),
                TextNode("normal link", TextType.LINK, "https://normal.link"),
            ],
        )

    def test_text_to_textnodes(self):
        text1 = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual(
            text_to_textnodes(text1),
            [
                TextNode("This is ", TextType.NORMAL),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.NORMAL),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
