from inline_markdown import split_nodes_delimiter
from test_textnode import unittest
from textnode import TextNode
from textnode import TextType
from inline_markdown import extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("Dit is **dikke** tekst", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("Dit is ", TextType.TEXT),
                TextNode("dikke", TextType.BOLD),
                TextNode(" tekst", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("Dit is *schuine* tekst", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("Dit is ", TextType.TEXT),
                TextNode("schuine", TextType.ITALIC),
                TextNode(" tekst", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("Dit is `code` tekst", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("Dit is ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" tekst", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)

        self.assertListEqual(
            [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
    )


if __name__ == "__main__":
    unittest.main()