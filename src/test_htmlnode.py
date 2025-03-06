import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode("p", "Text inside a paragraph")
        node2 = HTMLNode("p", "Text inside a paragraph", None)
        node3 = HTMLNode("p", "Text inside a paragraph", None, None)

        self.assertEqual(node1, node2)
        self.assertEqual(node1, node3)
        self.assertEqual(node2, node3)
        
if __name__ == "__main__":
    unittest.main() 