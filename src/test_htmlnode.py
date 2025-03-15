import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode("p", "Text inside a paragraph")
        node2 = HTMLNode("p", "Text inside a paragraph", None)
        node3 = HTMLNode("p", "Text inside a paragraph", None, None)
        node4 = HTMLNode("a", "Click me!", [{"href": "https://www.google.com"}])
        node5 = HTMLNode("a", "Click me!", [{"href": "https://www.google.com"}])
        self.assertEqual(node1, node2)
        self.assertEqual(node1, node3)
        self.assertEqual(node2, node3)
        self.assertEqual(node4, node5)

    def test_parameters(self):
        node = HTMLNode(
            "p",
            " There is something BOLD in here ",
            [HTMLNode("b", "BOLD BOI")],
            {"style": "text-align:left"},
        )

        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, " There is something BOLD in here ")
        self.assertEqual(node.children, [HTMLNode("b", "BOLD BOI")])
        self.assertEqual(node.props, {"style": "text-align:left"})

    def test_repr(self):
        n1 = HTMLNode(None, "Just plain text")
        n2 = HTMLNode("p", "This do be a paragraph, tho")
        n3 = HTMLNode("p", "Paragraph with style", None, {"style": "text-align:right"})
        n4 = HTMLNode(
            "p",
            "Paragraph and some italic",
            [HTMLNode("i", "Ohh, Italiano")],
            {"style": "text-align:left"},
        )

        self.assertEqual(
            n1.__repr__(),
            "HTMLNode(self.tag=None, self.value='Just plain text', self.children=None, self.props=None)",
        )
        self.assertEqual(
            n2.__repr__(),
            "HTMLNode(self.tag='p', self.value='This do be a paragraph, tho', self.children=None, self.props=None)",
        )
        self.assertEqual(
            n3.__repr__(),
            "HTMLNode(self.tag='p', self.value='Paragraph with style', self.children=None, self.props={'style': 'text-align:right'})",
        )
        self.assertEqual(
            n4.__repr__(),
            "HTMLNode(self.tag='p', \
self.value='Paragraph and some italic', \
self.children=[HTMLNode(self.tag='i', self.value='Ohh, Italiano', self.children=None, self.props=None)], \
self.props={'style': 'text-align:left'})",
        )


if __name__ == "__main__":
    unittest.main()
