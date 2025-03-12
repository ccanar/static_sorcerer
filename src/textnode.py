from enum import Enum
from leafnode import LeafNode


class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        ):
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text=}, {self.text_type.value=}, {self.url=})"


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


def split_nodes_delimeter(
    old_nodes: list[TextNode], delimeter: str, text_type: TextType
) -> list[TextNode]:
    result = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            result.append(node)
            continue
        if node.text.count(delimeter) == 0:
            result.append(TextNode(node.text, TextType.NORMAL))
            continue
        if node.text.count(delimeter) % 2 != 0:
            raise Exception("No matching closing delimeter")
        split_at_delimeter = node.text.split(delimeter)
        for i in range(len(split_at_delimeter)):
            if split_at_delimeter[i] == "":
                continue
            if i == 0 or i % 2 == 0:
                result.append(TextNode(split_at_delimeter[i], TextType.NORMAL))
            # if i % 2 == 0:
            # result.append(TextNode(split_at_delimeter[i], TextType.NORMAL))
            else:
                result.append(TextNode(split_at_delimeter[i], text_type))
    return result
