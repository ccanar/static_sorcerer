from enum import Enum


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

    line_list = markdown_text.splitlines()
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
