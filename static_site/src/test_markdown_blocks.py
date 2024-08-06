import unittest
from markdown_blocks import (
    markdown_to_html_node,
    markdown_to_blocks,
    block_to_block_type,
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_olist,
    block_type_ulist,
    block_type_quote,
)



class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_block_to_blocktype_heading(self):
        text = "### This is a heading"
        self.assertEqual(block_to_block_type(text), "heading")

    def test_block_to_bt_invalid_heading(self):
        text = "####### This is a heading"
        self.assertEqual(block_to_block_type(text), "paragraph")

    def test_block_to_blocktype_quote(self):
        text = "> This is a quote"
        self.assertEqual(block_to_block_type(text), "quote")

    def test_block_to_blocktype_unordered_list(self):
        text = """* Item 1
* Item 2
* Item 3"""
        self.assertEqual(block_to_block_type(text), "unordered_list")

    def test_block_to_blocktype_ordered_list(self):
        text = """1. First item
2. Second item
3. Third item"""
        self.assertEqual(block_to_block_type(text), "ordered_list")

    def test_block_to_bt_invalid_paragraph(self):
        text = "? I couldn't decide on a > last test ```"
        self.assertEqual(block_to_block_type(text), "paragraph")

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )
        
if __name__ == "__main__":
    unittest.main()