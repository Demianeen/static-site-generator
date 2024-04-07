import unittest

from htmlnode import HtmlNode, LeafNode, ParentNode


class TestHtmlNode(unittest.TestCase):
    # HtmlNode
    def test_props_to_html(self):
        link_node = HtmlNode(
            "a",
            "click me",
            None,
            {"href": "http://luminous-fig.biz", "target": "_blank"},
        )
        self.assertEqual(
            ' href="http://luminous-fig.biz" target="_blank"', link_node.props_to_html()
        )

    def test_props_to_html_with_bool(self):
        link_node = HtmlNode(
            "a",
            "click me",
            None,
            {"target": False, "disabled": True},
        )
        self.assertEqual(' target="False" disabled', link_node.props_to_html())

    def test_props_to_html_empty(self):
        paragraph_node = HtmlNode("p", None, None, None)
        self.assertEqual("", paragraph_node.props_to_html())

    def test_repr(self):
        link_node = HtmlNode(
            "a",
            "click me",
            None,
            {"href": "http://luminous-fig.biz", "target": "_blank"},
        )
        paragraph_node = HtmlNode("p", None, [link_node], None)
        self.assertEqual(
            "HtmlNode(a, click me, None, {'href': 'http://luminous-fig.biz', 'target': '_blank'})",
            repr(link_node),
        )
        self.assertEqual(
            "HtmlNode(p, None, [HtmlNode(a, click me, None, {'href': 'http://luminous-fig.biz', 'target': '_blank'})], None)",
            repr(paragraph_node),
        )

    # ParentNode
    def test_parentnode_to_html(self):
        paragraph_node = ParentNode(
            "p",
            [
                LeafNode(
                    "a",
                    "click me",
                    {"href": "http://luminous-fig.biz", "target": "_blank"},
                ),
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            {"class": "p"},
        )
        self.assertEqual(
            '<p class="p"><a href="http://luminous-fig.biz" target="_blank">click me</a><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>',
            paragraph_node.to_html(),
        )

    def test_parentnode_to_html_value_none(self):
        link_node = ParentNode(
            "a",
            None,
            {"href": "http://luminous-fig.biz", "target": "_blank"},
        )
        with self.assertRaises(ValueError):
            _ = link_node.to_html()

    def test_parentnode_to_html_tag_none(self):
        node = ParentNode(None, [], None)
        with self.assertRaises(ValueError):
            _ = node.to_html()

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    # LeafNode
    def test_leafnode_to_html(self):
        link_node = LeafNode(
            "a",
            "click me",
            {"href": "http://luminous-fig.biz", "target": "_blank"},
        )
        self.assertEqual(
            '<a href="http://luminous-fig.biz" target="_blank">click me</a>',
            link_node.to_html(),
        )

    def test_leafnode_to_html_value_none(self):
        link_node = LeafNode(
            "a",
            None,
            {"href": "http://luminous-fig.biz", "target": "_blank"},
        )
        with self.assertRaises(ValueError):
            _ = link_node.to_html()

    def test_leafnode_to_html_tag_none(self):
        node = LeafNode(
            None,
            "click me",
            {"href": "http://luminous-fig.biz", "target": "_blank"},
        )
        self.assertEqual(
            "click me",
            node.to_html(),
        )


if __name__ == "__main__":
    unittest.main()
