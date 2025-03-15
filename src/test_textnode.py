import unittest
from textnode import (
    TextNode,
    TextType,
    split_nodes_delimeter,
    split_nodes_images,
    split_nodes_links,
    text_node_to_html_node,
    extract_markdown_images,
    extract_markdown_links,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("TEST", TextType.BOLD)
        node2 = TextNode("TEST", TextType.BOLD)
        node3 = TextNode("TEST", TextType.BOLD, None)
        node4 = TextNode("TEST", TextType.NORMAL)
        node5 = TextNode("TEST", TextType.NORMAL, None)
        node6 = TextNode("TEST", TextType.ITALIC, "Test.com")
        node7 = TextNode("TEST", TextType.ITALIC, "Test.com")

        self.assertEqual(node, node2)
        self.assertEqual(node2, node3)
        self.assertEqual(node, node3)
        self.assertEqual(node4, node5)
        self.assertEqual(node6, node7)

    def test_not_eq(self):
        node = TextNode("TEST", TextType.BOLD)
        node4 = TextNode("TEST", TextType.NORMAL)
        node6 = TextNode("TEST", TextType.ITALIC, "Test.com")
        node7 = TextNode("TEST", TextType.ITALIC, "Test.com")
        node8 = TextNode("NOT_TEST", TextType.ITALIC, "Test.com")
        node9 = TextNode("TEST", TextType.BOLD)
        node10 = TextNode("Test", TextType.BOLD)
        node11 = TextNode("", TextType.BOLD)

        self.assertNotEqual(node9, node10)
        self.assertNotEqual(node9, node11)
        self.assertNotEqual(node10, node11)
        self.assertNotEqual(node, node4)
        self.assertNotEqual(node, node6)
        self.assertNotEqual(node4, node6)
        self.assertNotEqual(node7, node8)

    def test_repr(self):
        node = TextNode("Some text", TextType.BOLD, "www.google.com")
        self.assertEqual(
            node.__repr__(),
            "TextNode(self.text='Some text', self.text_type.value='bold', self.url='www.google.com')",
        )

    def test_text_node_to_html_node(self):
        text_node1 = TextNode("Normal text", TextType.NORMAL)
        html_node1 = text_node_to_html_node(text_node1)
        self.assertEqual(html_node1.tag, None)
        self.assertEqual(html_node1.value, "Normal text")
        self.assertEqual(html_node1.children, None)
        self.assertEqual(html_node1.props, None)

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


if __name__ == "__main__":
    unittest.main()
