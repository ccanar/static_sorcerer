import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node NOT", TextType.BOLD)
        node4 = TextNode("This is a text node", TextType.NORMAL)
        node5 = TextNode("This is a text node", TextType.BOLD, "None")
        node6 = TextNode("This is a text node", TextType.BOLD, "THATAHTHAHTAH")
        node7 = TextNode("This is a text node", TextType.ITALIC, "THATAHTHAHTAH")
        node8 = TextNode("", TextType.BOLD, "THATAHTHAHTAH")
        node9 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node, node4)
        self.assertNotEqual(node, node5)
        self.assertNotEqual(node, node6)
        self.assertNotEqual(node, node7)
        self.assertNotEqual(node, node8)
        self.assertEqual(node, node9)

if __name__ == "__main__":
    unittest.main()        