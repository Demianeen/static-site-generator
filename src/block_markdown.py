from enum import Enum
from functools import reduce
import re
from typing import List

from htmlnode import LeafNode, ParentNode
from textnode import text_node_to_html_node

from inline_markdown import (
    text_to_textnodes,
)


class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6


def markdown_to_blocks(markdown: str) -> List[str]:
    blocks = re.split(r"\n\s*\n+", markdown)
    filtered_blocks = []
    for block in blocks:
        stripped_block = block.strip(" \n")

        is_code_block_start = stripped_block.startswith("```")
        is_code_block_end = stripped_block.endswith("```")
        if is_code_block_end:
            if not is_code_block_start and is_code_block_end:
                filtered_blocks[-1] += f"\n{stripped_block}"
                continue
        if stripped_block:
            filtered_blocks.append(stripped_block)

    return filtered_blocks


def get_block_type(block: str) -> BlockType:
    if re.match(r"#{1,6} ", block):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    block_lines = block.split("\n")
    if reduce(
        lambda value, line: (line.startswith("> ") if value is True else False),
        block_lines,
        True,
    ):
        return BlockType.QUOTE
    if reduce(
        lambda value, line: (
            (line.startswith("* ") or line.startswith("- ")) if value is True else False
        ),
        block_lines,
        True,
    ):
        return BlockType.UNORDERED_LIST
    if reduce(
        lambda value, line: (
            re.match(r"^\d. ", line) is not None if value is True else False
        ),
        block_lines,
        True,
    ):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_to_htmlnode(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    html_nodes = []

    for text_block in blocks:
        block_type = get_block_type(text_block)
        if block_type == BlockType.PARAGRAPH:
            lines = text_block.split("\n")
            paragraph_content = " ".join(lines)
            text_nodes = text_to_textnodes(paragraph_content)
            paragraph_node = ParentNode("p", [], {})
            paragraph_node.add_children(
                list(
                    map(lambda text_node: text_node_to_html_node(text_node), text_nodes)
                )
            )
            html_nodes.append(paragraph_node)
        if block_type == BlockType.QUOTE:
            block_text = " ".join(
                map(lambda line: line.lstrip("> "), text_block.split("\n"))
            )

            text_nodes = text_to_textnodes(block_text)
            paragraph_node = ParentNode("p", [], {})
            paragraph_node.add_children(
                list(
                    map(lambda text_node: text_node_to_html_node(text_node), text_nodes)
                )
            )
            html_nodes.append(ParentNode("blockquote", [paragraph_node]))
        if block_type == BlockType.CODE:
            html_nodes.append(
                ParentNode(
                    "pre", [LeafNode("code", "\n".join(text_block.splitlines()[1:-1]))]
                )
            )
        if block_type == BlockType.HEADING:
            block_text = text_block.lstrip("#")
            heading_level = len(text_block) - len(block_text)
            block_text = block_text.lstrip()
            html_nodes.append(LeafNode(f"h{heading_level}", block_text))
        if block_type == BlockType.UNORDERED_LIST:
            list_items_text_nodes = map(
                lambda text_segment: text_to_textnodes(text_segment[2:]),
                text_block.split("\n"),
            )

            list_items_html_nodes = []
            for list_item_text_nodes in list_items_text_nodes:
                list_item_html_nodes = []
                for text_node in list_item_text_nodes:
                    list_item_html_nodes.append(text_node_to_html_node(text_node))
                list_items_html_nodes.append(ParentNode("li", list_item_html_nodes))

            html_nodes.append(ParentNode("ul", list_items_html_nodes))
        if block_type == BlockType.ORDERED_LIST:
            list_items_text_nodes = map(
                lambda text_segment: text_to_textnodes(text_segment[3:]),
                text_block.split("\n"),
            )

            list_items_html_nodes = []
            for list_item_text_nodes in list_items_text_nodes:
                list_item_html_nodes = []
                for text_node in list_item_text_nodes:
                    list_item_html_nodes.append(text_node_to_html_node(text_node))
                list_items_html_nodes.append(ParentNode("li", list_item_html_nodes))

            html_nodes.append(ParentNode("ol", list_items_html_nodes))

    return ParentNode("div", html_nodes, {})
