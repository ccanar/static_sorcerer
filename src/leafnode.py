from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        if not value:
            raise ValueError
        super().__init__(tag, value, None, props) 

    def to_html(self):
        if not self.tag:
            return self.value
        else:
            return self.full_tag[0] + self.value + self.full_tag[1]