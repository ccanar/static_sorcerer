from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props=None):
        super().__init__(tag, None, children, props)

    def __repr__(self):
        return f"ParentNode({self.tag=}, {self.children=}, {self.props=})"

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode: no tag")

        if not self.children:
            raise ValueError("ParentNode: no children")

        result = f"<{self.tag}{self.props_to_html()}>"

        for child in self.children:
            result += child.to_html()

        result += f"</{self.tag}>"
        return result
