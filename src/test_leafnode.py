import unittest

from leafnode import LeafNode, text_node_to_html_node
from textnode import TextNode, TextType


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        ln1 = LeafNode(None, "There is no tag")
        ln2 = LeafNode("p", "There is a P!")
        ln3 = LeafNode("b", "Bold text")
        ln4 = LeafNode("i", "Italic text")
        ln5 = LeafNode("code", "Some code")
        ln6 = LeafNode("link", "link", {"rel": "stylesheet", "href": "styles.css"})
        ln7 = LeafNode(
            "img",
            "image",
            {
                "src": "img_test.jpg",
                "alt": "Test image",
                "width": "500",
                "height": "600",
            },
        )

        self.assertEqual(ln1.to_html(), "There is no tag")
        self.assertEqual(ln2.to_html(), "<p>There is a P!</p>")
        self.assertEqual(ln3.to_html(), "<b>Bold text</b>")
        self.assertEqual(ln4.to_html(), "<i>Italic text</i>")
        self.assertEqual(ln5.to_html(), "<code>Some code</code>")
        self.assertEqual(ln6.to_html(), '<link rel="stylesheet" href="styles.css" />')
        self.assertEqual(
            ln7.to_html(),
            '<img src="img_test.jpg" alt="Test image" width="500" height="600" />',
        )

    def test_text_node_to_html_node(self):
        text_node1 = TextNode("Normal text", TextType.NORMAL)
        html_node1 = text_node_to_html_node(text_node1)
        self.assertEqual(html_node1.tag, None)
        self.assertEqual(html_node1.value, "Normal text")
        self.assertEqual(html_node1.children, None)
        self.assertEqual(html_node1.props, None)


if __name__ == "__main__":
    unittest.main()
