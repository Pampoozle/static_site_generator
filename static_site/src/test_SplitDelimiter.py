import unittest, re

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)

from markdown_block import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_images, split_nodes_links, text_to_textnodes

class TestDelimiter(unittest.TestCase):
    def test_simple(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        correct_node = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text),
        ]
        self.assertEqual(new_nodes, correct_node)

    def test_bold(self):
        node = TextNode("This is text with a **bold block** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        correct_node = [
            TextNode("This is text with a ", text_type_text),
            TextNode("bold block", text_type_bold),
            TextNode(" word", text_type_text),
        ]
        self.assertEqual(new_nodes, correct_node)

    def test_firstword(self):
        node = TextNode("**This** is text with a bold block word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        correct_node = [
            TextNode("This", text_type_bold),
            TextNode(" is text with a bold block word", text_type_text),
        ]
        self.assertEqual(new_nodes, correct_node)

    def test_markdown_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        test_markdown = extract_markdown_images(text)
        correct_markdown = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(test_markdown, correct_markdown)

    def test_markdown_three_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) but mostly: ![crying](https://i.gifer.com/jU.gif)"
        test_markdown = extract_markdown_images(text)
        correct_markdown = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"), ("crying", "https://i.gifer.com/jU.gif")]
        self.assertEqual(test_markdown, correct_markdown)

    def test_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        test_link = extract_markdown_links(text)
        correct_markdown = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(test_link, correct_markdown)  

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            text_type_text,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", text_type_text),
                TextNode(
                    "second image", text_type_image, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_more_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and a third ![cat](https://media.istockphoto.com/id/1443562748/photo/cute-ginger-cat.jpg?s=612x612&w=0&k=20&c=vvM97wWz-hMj7DLzfpYRmY2VswTqcFEKkC437hxm3Cg=)",
            text_type_text,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", text_type_text),
                TextNode(
                    "second image", text_type_image, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and a third ", text_type_text),
                TextNode(
                    "cat", text_type_image, "https://media.istockphoto.com/id/1443562748/photo/cute-ginger-cat.jpg?s=612x612&w=0&k=20&c=vvM97wWz-hMj7DLzfpYRmY2VswTqcFEKkC437hxm3Cg="
                    ),
            ],
            new_nodes,
        )
    
    def test_split_link(self):
        node = TextNode(
            "This is text with a link [Google](https://www.google.ca) and another [Bootdev](https://www.boot.dev/tracks/backend) with text at the end.",
            text_type_text,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", text_type_text),
                TextNode("Google", text_type_link, "https://www.google.ca"),
                TextNode(" and another ", text_type_text),
                TextNode(
                    "Bootdev", text_type_link, "https://www.boot.dev/tracks/backend"
                ),
                TextNode(" with text at the end.", text_type_text),
            ],
            new_nodes,
        )
    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        test = text_to_textnodes(text)
        self.assertEqual(test,[
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
            ]
        )




if __name__ == "__main__":
    unittest.main()