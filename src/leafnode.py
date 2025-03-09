from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self, tag: str | None, value: str, props: dict[str, str] | None = None
    ):
        if not value:
            raise ValueError
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.tag:
            return self.value
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"
