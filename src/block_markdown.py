from enum import Enum

from htmlnode import HTMLNode
from inline_markdown import text_to_textnodes
from leafnode import LeafNode
from parentnode import ParentNode
from test_textnode import test_text_node
from textnode import text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = ("paragraph",)
    HEADING = ("heading",)
    CODE = ("code",)
    QUOTE = ("quote",)
    UNORDERED_LIST = ("unordered_list",)
    ORDERED_LIST = ("ordered_list",)


def markdown_to_blocks(markdown_text: str) -> list[str]:
    output: list[str] = []
    split_text = markdown_text.split("\n\n")
    for element in split_text:
        if len(element) > 0:
            output.append(element.strip())
    return output


def block_to_block_type(markdown_text: str) -> BlockType:
    if markdown_text == "":
        raise Exception("block_to_block_type EMPTY STRING INPUT")
    if markdown_text[0] == " ":
        raise Exception("block_to_block_type STARTS WITH A SPACE")
    if markdown_text.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif markdown_text.startswith("```") and markdown_text.endswith("```"):
        return BlockType.CODE

    line_list = markdown_text.split("\n")
    if markdown_text.startswith(">"):
        all_lines_proper_start = True
        for line in line_list:
            if not line.startswith(">"):
                all_lines_proper_start = False
                break
        if all_lines_proper_start:
            return BlockType.QUOTE

    if markdown_text.startswith("- "):
        all_lines_proper_start = True
        for line in line_list:
            if not line.startswith("- "):
                all_lines_proper_start = False
                break
        if all_lines_proper_start:
            return BlockType.UNORDERED_LIST

    if markdown_text.startswith("1. "):
        number = 1
        all_lines_proper_start = True
        for line in line_list:
            if not line.startswith(f"{number}. "):
                all_lines_proper_start = False
                break
            number += 1
        if all_lines_proper_start:
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown_text: str) -> ParentNode:
    markdown_blocks = markdown_to_blocks(markdown_text)
    block_list = []
    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.CODE:
                block_list.append(LeafNode("code", block.strip("```")))

            case BlockType.QUOTE:
                lines = block.splitlines(True)
                stripped = ""
                for line in lines:
                    stripped += line.lstrip("> ")
                block_list.append(LeafNode("blockquote", stripped))

            case BlockType.ORDERED_LIST:
                omega_parent = ParentNode("ol", [])   
                block_in_lines = block.splitlines()
                for line in block_in_lines:
                    child = ParentNode("li", [])
                    child_text_nodes = text_to_textnodes(line[line.find(" ") + 1 :])
                    for text_node in child_text_nodes:
                        child.children.append(text_node_to_html_node(text_node))
                    omega_parent.children.append(child)
                block_list.append(omega_parent)

            case BlockType.UNORDERED_LIST:
                omega_parent = ParentNode("ul", [])   
                block_in_lines = block.splitlines()
                for line in block_in_lines:
                    child = ParentNode("li", [])
                    child_text_nodes = text_to_textnodes(line[line.find(" ") + 1:])
                    for text_node in child_text_nodes:
                        child.children.append(text_node_to_html_node(text_node))
                    omega_parent.children.append(child)
                block_list.append(omega_parent)

            case BlockType.HEADING:
                block_in_lines = block.splitlines()
                for line in block_in_lines:
                    number_of_symbols = line[:line.find(" ")].count('#')
                    child = ParentNode(f"h{number_of_symbols}", [])
                    child_text_nodes = text_to_textnodes(line[line.find(" ") + 1:])
                    for text_node in child_text_nodes:
                        child.children.append(text_node_to_html_node(text_node))
                    block_list.append(child)

            case BlockType.PARAGRAPH:
                block_list.append(
                    ParentNode(
                        "p",
                        [text_node_to_html_node(x) for x in text_to_textnodes(block)],
                    )
                )
    output = ParentNode("div", block_list, None)
    return output


def extract_title(markdown_text: str) -> str:
    lines = markdown_text.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.strip("# ").strip()
    raise Exception("No title found in markdown")
