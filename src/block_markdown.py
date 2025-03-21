def markdown_to_blocks(markdown_text: str) -> list[str]:
    output: list[str] = []
    split_text = markdown_text.split("\n\n")
    for element in split_text:
        if len(element) > 0:
            output.append(element.strip())
    return output
