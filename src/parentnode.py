from htmlnode import HTMLNode
from leafnode import LeafNode
class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("No TAG")
        if not self.children:
            raise ValueError("No CHILDREN")
        result = ""
        result += f"<{self.tag}>"
        for child in self.children:
            result += child.to_html()
        result += f"</{self.tag}>"
        return result

node = ParentNode(
    "p",
    [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
    ],
)

print(node.to_html())