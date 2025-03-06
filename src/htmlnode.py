class HTMLNode():
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict[str, str] = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        output = ""
        for key, value in self.props.items():
            output += f"{key}={value} "
        return output

    def __repr__(self):
        return f"HTMLNode({self.tag=}, {self.value=}, {self.children=}, {self.props=})"

    def __eq__(self, other):
        if  self.tag == other.tag and \
            self.value == other.value and \
            self.children == other.children and \
            self.props == other.props:
            return True
        return False