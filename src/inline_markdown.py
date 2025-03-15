import re
from textnode import TextNode, TextType


def extract_markdown_images(raw_text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", raw_text)


def extract_markdown_links(raw_text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", raw_text)


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
            else:
                result.append(TextNode(split_at_delimeter[i], text_type))
    return result


def split_nodes_images(old_nodes: list[TextNode]):
    result: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            result.append(node)
            continue

        found_images = extract_markdown_images(node.text)

        if len(found_images) == 0:
            result.append(node)
            continue

        text = node.text

        for i in range(len(found_images)):
            split_text = text.split(f"![{found_images[i][0]}]({found_images[i][1]})", 1)
            if split_text[0] != "":
                result.append(TextNode(split_text[0], TextType.NORMAL))
            result.append(
                TextNode(found_images[i][0], TextType.IMAGE, found_images[i][1])
            )
            if i == len(found_images) - 1:
                if split_text[1] != "":
                    result.append(TextNode(split_text[1], TextType.NORMAL))
            else:
                if split_text[1] != "":
                    text = split_text[1]
    return result


def split_nodes_links(old_nodes: list[TextNode]):
    result: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            result.append(node)
            continue

        found_links = extract_markdown_links(node.text)

        if len(found_links) == 0:
            result.append(node)
            continue

        text = node.text

        for i in range(len(found_links)):
            split_text = text.split(f"[{found_links[i][0]}]({found_links[i][1]})", 1)
            if split_text[0] != "":
                result.append(TextNode(split_text[0], TextType.NORMAL))
            result.append(TextNode(found_links[i][0], TextType.LINK, found_links[i][1]))
            text = split_text[1]
            if i == len(found_links) - 1:
                if split_text[1] != "":
                    result.append(TextNode(split_text[1], TextType.NORMAL))
            else:
                if split_text[1] != "":
                    text = split_text[1]
    return result


def text_to_textnodes(text) -> list[TextNode]:
    text_nodes: list[TextNode] = []
    text_nodes = split_nodes_images([TextNode(text, TextType.NORMAL)])
    text_nodes = split_nodes_links(text_nodes)
    delimeters_and_text_types = [
        ("**", TextType.BOLD),
        ("_", TextType.ITALIC),
        ("`", TextType.CODE),
    ]
    for delimeter, text_type in delimeters_and_text_types:
        text_nodes = split_nodes_delimeter(text_nodes, delimeter, text_type)
    return text_nodes
