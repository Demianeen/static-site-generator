import unittest

from block_markdown import (
    markdown_to_htmlnode,
    markdown_to_blocks,
    get_block_type,
    BlockType,
)


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md_content = """This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items

```
This is some code block

With a bit of
text
```
"""
        blocks = markdown_to_blocks(md_content)
        self.assertEqual(
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
                """```
This is some code block
With a bit of
text
```""",
            ],
            blocks,
        )

    def test_markdown_to_blocks_with_trailing_spaces(self):
        md_content = """

This is **bolded** paragraph


This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line



* This is a list
* with items



"""
        blocks = markdown_to_blocks(md_content)
        self.assertEqual(
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
            blocks,
        )

    def test_get_block_types(self):
        block = "# heading"
        self.assertEqual(get_block_type(block), BlockType.HEADING)
        block = """```
This is some code block

With a bit of
text
```"""
        self.assertEqual(get_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(get_block_type(block), BlockType.QUOTE)
        block = "* list\n* items"
        self.assertEqual(get_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(get_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(get_block_type(block), BlockType.PARAGRAPH)

    def test_markdown_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_htmlnode(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_htmlnode(md)
        html = node.to_html()
        self.maxDiff = None
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_htmlnode(md)
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

        node = markdown_to_htmlnode(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote><p>This is a blockquote block</p></blockquote><p>this is paragraph text</p></div>",
        )


if __name__ == "__main__":
    unittest.main()