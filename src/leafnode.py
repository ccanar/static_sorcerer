from textnode import TextNode, TextType
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


def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.NORMAL:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            if text_node.url:
                return LeafNode(
                    "a",
                    text_node.text,
                    {
                        "href": text_node.url,
                    },
                )
            else:
                raise Exception("url is None")
        case TextType.IMAGE:
            if text_node.url:
                return LeafNode(
                    "img", "", {"src": text_node.url, "alt": text_node.text}
                )
            else:
                raise Exception("url is None")
