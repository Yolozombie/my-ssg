import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link

class TestTextNode(unittest.TestCase):
        def test_eq(self):
            node = TextNode("This is a text node", TextType.BOLD)
            node2 = TextNode("This is a text node", TextType.BOLD)
            node3 = TextNode("This is a text node", TextType.ITALIC)
            self.assertEqual(node, node2)
            self.assertNotEqual(node, node3)

        
        def test_repr_with_url(self):
            node = TextNode("This is a link", TextType.LINK, "https://www.example.com")
            node2 = TextNode("This is a link", TextType.LINK, "https://www.example.com")
            node3 = TextNode("This is a link", TextType.TEXT, "https://www.different.com")
            self.assertEqual(node, node2)
            self.assertNotEqual(node, node3)
        
        def test_repr_without_url(self):
            node = TextNode("This is a normal text", TextType.TEXT)
            node2 = TextNode("This is a normal text", TextType.TEXT)
            node3 = TextNode("This is a different text", TextType.LINK, "https://www.example.com")
            self.assertEqual(node, node2)
            self.assertNotEqual(node, node3)    

        def test_text(self):
            node = TextNode("This is a text node", TextType.TEXT)
            html_node = text_node_to_html_node(node)
            self.assertEqual(html_node.tag, None)
            self.assertEqual(html_node.value, "This is a text node")

        def test_bold(self):
            node = TextNode("This is bold text", TextType.BOLD)
            html_node = text_node_to_html_node(node)
            self.assertEqual(html_node.tag, "b")
            self.assertEqual(html_node.value, "This is bold text")
        
        def test_italic(self):
            node = TextNode("This is italic text", TextType.ITALIC)
            html_node = text_node_to_html_node(node)
            self.assertEqual(html_node.tag, "i")
            self.assertEqual(html_node.value, "This is italic text")

        def test_code(self):
            node = TextNode("print('Hello, World!')", TextType.CODE)
            html_node = text_node_to_html_node(node)
            self.assertEqual(html_node.tag, "code")
            self.assertEqual(html_node.value, "print('Hello, World!')")

        def test_link(self):
            node = TextNode("Click here", TextType.LINK, "https://www.example.com")
            html_node = text_node_to_html_node(node)
            self.assertEqual(html_node.tag, "a")
            self.assertEqual(html_node.value, "Click here")
            self.assertEqual(html_node.props, {"href": "https://www.example.com"})
        
        def test_image(self):   
            node = TextNode("An image", TextType.IMAGE, "https://www.example.com/image.png")
            html_node = text_node_to_html_node(node)
            self.assertEqual(html_node.tag, "img")
            self.assertEqual(html_node.value, "")
            self.assertEqual(html_node.props, {"src": "https://www.example.com/image.png", "alt": "An image"})

import unittest
from inline_markdown import extract_markdown_images, extract_markdown_links, split_nodes_image

class TestInlineMarkdown(unittest.TestCase):
        def test_extract_markdown_images(self):
            matches = extract_markdown_images(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
            )
            self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

        def test_extract_markdown_links(self):
            matches = extract_markdown_links(
                "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
            )
            self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
            )    

        def test_split_images(self):
            node = TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
                TextType.TEXT,
            )
            new_nodes = split_nodes_image([node])
            self.assertListEqual(
                [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
            )
        
        def test_split_links(self):
            node = TextNode(
                "This is text with a [link](https://boot.dev) and another [second link](https://youtube.com)",
                TextType.TEXT,
            )
            new_nodes = split_nodes_link([node])
            self.assertListEqual(
                [
                    TextNode("This is text with a ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://boot.dev"),
                    TextNode(" and another ", TextType.TEXT),
                    TextNode("second link", TextType.LINK, "https://youtube.com"),
                ],
                new_nodes,
            )

if __name__ == "__main__":
    unittest.main()