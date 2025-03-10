import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("TEST", TextType.BOLD)
        node2 = TextNode("TEST", TextType.BOLD)
        node3 = TextNode("TEST", TextType.BOLD, None)
        node4 = TextNode("TEST", TextType.NORMAL)
        node5 = TextNode("TEST", TextType.NORMAL, None)
        node6 = TextNode("TEST", TextType.ITALIC, "Test.com")
        node7 = TextNode("TEST", TextType.ITALIC, "Test.com")
        node8 = TextNode("NOT_TEST", TextType.ITALIC, "Test.com")
        node9 = TextNode("TEST", TextType.BOLD)
        node10 = TextNode("Test", TextType.BOLD)
        node11 = TextNode("", TextType.BOLD)

        self.assertEqual(node, node2)
        self.assertEqual(node2, node3)
        self.assertEqual(node, node3)
        self.assertEqual(node4, node5)
        self.assertEqual(node6, node7)
        self.assertNotEqual(node9, node10, node11)
        self.assertNotEqual(node, node4, node6)
        self.assertNotEqual(node7, node8)


if __name__ == "__main__":
    unittest.main()
