from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self, tag: str | None, value: str | None, props: dict[str, str] | None = None
    ):
        super().__init__(tag, value, None, props)

    def __repr__(self):
        return f"LeafNode({self.tag=}, {self.value=}, {self.props=})"

    def to_html(self):
        if not self.value:
            raise ValueError("LeafNode: no value")

        if not self.tag:
            return self.value

        result = f"<{self.tag}{self.props_to_html()}"

        if self.tag == "img" or self.tag == "link":
            result += " />"
            return result

        result += f">{self.value}</{self.tag}>"
        return result
