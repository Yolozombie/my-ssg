import os
import textwrap
from enum import Enum
from htmlnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block: str):
    lines = block.split("\n")
    first_line = lines[0]
    n = len(first_line) - len(first_line.lstrip("#")) 
    is_heading = 1 <= n <= 6 and len(first_line) > n and first_line[n] == " "
    is_code = block.startswith("```\n") and block.endswith("```")
    is_quote = all(line.startswith(">") for line in lines)
    is_ul = all(line.startswith("- ") for line in lines)
    is_ol = all(line.startswith(f"{i}. ") for i, line in enumerate(lines, start=1))

    if is_heading:
        return BlockType.HEADING
    if is_code:
        return BlockType.CODE
    if is_quote:
        return BlockType.QUOTE
    if is_ul:
        return BlockType.UNORDERED_LIST
    if is_ol:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
       

def markdown_to_blocks(markdown):
    blockstring = []
    parts = markdown.split("\n\n")
    for block in parts:
        clean = block.strip()
        if clean != "":
            blockstring.append(clean)
    return blockstring

def text_to_children(text):
    # 1. Maak text_nodes van de tekst
    text_nodes = text_to_textnodes(text)
    # 2. Maak een lijst om de html_nodes in op te slaan
    children = []
    # 3. Loop door de text_nodes en zet ze om naar html_nodes
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    # 4. Geef de lijst met kinderen terug
    return children



def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_block = []
    for block in blocks:
        type_block = block_to_block_type(block)
        if type_block == BlockType.QUOTE:
            lines = block.split("\n")
            new_lines = []
            for line in lines:
                new_lines.append(line.lstrip(">").strip())
            content = " ".join(new_lines)
            
            children = text_to_children(content)
            quote_node = ParentNode("blockquote", children)
            html_block.append(quote_node)         

        elif type_block == BlockType.HEADING:
            level = 0
            for char in block:
                if char == "#":
                    level += 1
                else:
                    break
            # De tekst begint ná de '#' en het daaropvolgende spatie.
            # Als level 3 is, dan begint de tekst bij index level + 1 (dus 4).
            text = block[level + 1 :].strip()
            
            # Nu we de tag 'h' + level weten en de tekst hebben...
            tag = f"h{level}"
            children = text_to_children(text)
            heading_node = ParentNode(tag, children)
            html_block.append(heading_node)
        
        elif type_block == BlockType.PARAGRAPH:
            lines = block.split("\n")
            # We strippen elke regel!
            stripped_lines = []
            for line in lines:
                stripped_lines.append(line.strip())
            
            paragraph_text = " ".join(stripped_lines)
            children = text_to_children(paragraph_text)
            paragraph_node = ParentNode("p", children)
            html_block.append(paragraph_node)

        elif type_block == BlockType.CODE:
            lines = block.split("\n")
            
            # verwijder eerste en laatste regel (de ``` regels)
            code_lines = lines[1:-1]
            
            # voeg weer samen met newline
            code_text = "\n".join(code_lines)
            
            # verwijder gemeenschappelijke inspringing
            code_text = textwrap.dedent(code_text) + "\n"

            raw_text_node = TextNode(code_text, TextType.TEXT)
            child = text_node_to_html_node(raw_text_node)
            
            code_node = ParentNode("code", [child])
            pre_node = ParentNode("pre", [code_node])
            html_block.append(pre_node)

        elif type_block == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            html_items = []
            for line in lines:
                text = line[2:]
                children = text_to_children(text)
                li_node = ParentNode("li", children)
                html_items.append(li_node)
            ul_node = ParentNode("ul", html_items)
            html_block.append(ul_node)
             
        elif type_block == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            html_items = []
            for line in lines:
                text = line[3:]
                children = text_to_children(text)
                li_node = ParentNode("li", children)
                html_items.append(li_node)
            ol_node = ParentNode("ol", html_items)
            html_block.append(ol_node)
    return ParentNode("div", html_block)



#
#open
#.read()
#.write()
#.close()
#.replace()
#os.path.dirname
#os.makedirs
#.startswith()
#.split()
