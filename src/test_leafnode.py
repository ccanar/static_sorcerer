import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        ln1 = LeafNode(None, "There is no tag")
        ln2 = LeafNode("p", "There is a P!")

        self.assertEqual(ln1.to_html(), "There is no tag")
        self.assertEqual(ln2.to_html(), "<p>There is a P!</p>")


if __name__ == "__main__":
    unittest.main()

