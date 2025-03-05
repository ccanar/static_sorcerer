from textnode import *

def main():
    t1 = TextNode("Text one", TextType.BOLD)
    t2 = TextNode("Text two", TextType.LINK, "www.wp.pl/image")
    t3 = TextNode("Text two", TextType.LINK, "www.wp.pl/image")

    print(f"{t1 == t2 = }")
    print(f"{t1 == t3 = }")
    print(f"{t2 == t3 = }")

    return 

main()