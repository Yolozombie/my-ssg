import unittest
import textwrap
from markdown_blocks import markdown_to_blocks, block_to_block_type, markdown_to_html_node, BlockType

class TestMarkdownBlocks(unittest.TestCase):
    def test_splitting(self):
        md = "a\n\nb"
        self.assertEqual(markdown_to_blocks(md), ["a", "b"])
    
    def test_whitespace_only(self):
        md = "   \n\n   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks(self):
        md = textwrap.dedent("""\
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
""")
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_block_to_block_type_heading(self):
        self.assertEqual(block_to_block_type("# Hallo"), BlockType.HEADING)

    def test_block_to_block_type_code(self):
        self.assertEqual(block_to_block_type("```\ncode\n```"), BlockType.CODE)

    def test_block_to_block_type_quote(self):
        self.assertEqual(block_to_block_type("> a\n> b"), BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        self.assertEqual(block_to_block_type("- a\n- b"), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        self.assertEqual(block_to_block_type("1. a\n2. b"), BlockType.ORDERED_LIST)

    def test_block_to_block_type_paragraph(self):
        self.assertEqual(block_to_block_type("gewoon tekst"), BlockType.PARAGRAPH)


    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
            ```
            This is text that _should_ remain
            the **same** even with inline stuff
            ```
            """

        node = markdown_to_html_node(md)
        html = node.to_html()
        
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
   

def test_extract_title(self):
    md = """
    # Hallo Wereld\nDit is tekst
           Hallo met spaties   
    Gewone tekst\nNog meer tekst  """

    
    pass






if __name__ == "__main__":
    unittest.main()