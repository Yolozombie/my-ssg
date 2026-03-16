from textnode import TextNode, TextType 
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception("delimiter not closed!")
            
       
        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(parts[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(parts[i], text_type))
    return new_nodes
        

def extract_markdown_images(text):
    patern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    result = re.findall(patern, text)
    return result

def extract_markdown_links(text):
    patern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    result = re.findall(patern, text)
    return result


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        images = extract_markdown_images(old_node.text)
        if len(images) == 0:
            new_nodes.append(old_node)  
        else:
            remaining_text = old_node.text
            for image_alt, image_link in images:
                sections = remaining_text.split(f"![{image_alt}]({image_link})", 1)
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
                remaining_text = sections[1]
            if remaining_text:
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        links = extract_markdown_links(old_node.text)
        if len(links) == 0:
            new_nodes.append(old_node)
        else:
            remaining_text = old_node.text
            for image_alt, image_link in links:
                sections = remaining_text.split(f"[{image_alt}]({image_link})", 1)
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(image_alt, TextType.LINK, image_link))
                remaining_text = sections[1]
            if remaining_text:
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes
            
def text_to_textnodes(text):    
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
