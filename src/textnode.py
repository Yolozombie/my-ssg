from enum import Enum
from htmlnode import LeafNode 

class TextType(Enum):
    BOLD = "bold"
    ITALIC = "italic"
    TEXT = "text"
    LINK = "link"
    CODE = "code"
    IMAGE = "image"
    

class TextNode:
    def __init__(self, text: str, text_type: TextType, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    
    def __eq__(self, value):
        return True if isinstance(value, TextNode) and self.text == value.text and self.text_type == value.text_type and self.url == value.url else False
    
    def __repr__(self):
        return f"TextNode({self.text},{self.text_type.value},{self.url})"
    
def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, props={"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", props={"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"Unsupported text type: {text_node.text_type}")