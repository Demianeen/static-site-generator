from typing import List
import re

from textnode import TextType, TextNode


def split_nodes_delimiter(
    old_nodes: List[TextNode], delimiter: str, text_type: TextType
):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i, text in enumerate(sections):
            if text == "":
                continue
            # all even indexes are normal text, all other are text_type node
            if i % 2 == 0:
                new_nodes.append(TextNode(text, TextType.TEXT))
                continue
            new_nodes.append(TextNode(text, text_type))
    return new_nodes


def extract_markdown_images(text: str):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes: List[TextNode]):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        extracted_images_attributes = extract_markdown_images(node.text)
        if len(extracted_images_attributes) == 0:
            new_nodes.append(node)
            continue

        text_after_image = node.text
        for alt, url in extracted_images_attributes:
            text_before_image, text_after_image = text_after_image.split(
                f"![{alt}]({url})", 1
            )
            if text_before_image != "":
                new_nodes.append(TextNode(text_before_image, TextType.TEXT))

            new_nodes.append(
                TextNode(alt, TextType.IMAGE, url),
            )
        if text_after_image != "":
            new_nodes.append(TextNode(text_after_image, TextType.TEXT))

    return new_nodes


def extract_markdown_links(text: str):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_link(old_nodes: List[TextNode]):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        extracted_images_attributes = extract_markdown_links(node.text)
        if len(extracted_images_attributes) == 0:
            new_nodes.append(node)
            continue

        text_after_image = node.text
        for alt, url in extracted_images_attributes:
            text_before_image, text_after_image = text_after_image.split(
                f"[{alt}]({url})", 1
            )
            if text_before_image != "":
                new_nodes.append(TextNode(text_before_image, TextType.TEXT))

            new_nodes.append(
                TextNode(alt, TextType.LINK, url),
            )
        if text_after_image != "":
            new_nodes.append(TextNode(text_after_image, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text: str) -> List[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes
