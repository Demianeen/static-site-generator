from typing import Dict, List, Optional


class HtmlNode:
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children: Optional[List["HtmlNode"]] = None,
        props: Optional[Dict[str, str | int | bool]] = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self) -> str:
        if self.props is None:
            return ""

        html_props = ""
        for key, value in self.props.items():
            if value is True:
                html_props += f" {key}"
            else:
                html_props += f' {key}="{value}"'

        return html_props

    def __repr__(self):
        return f"HtmlNode({self.tag}, {self.value}, {self.children}, {self.props})"


class ParentNode(HtmlNode):
    def __init__(
        self,
        tag: Optional[str] = None,
        children: Optional[List["HtmlNode"]] = None,
        props: Optional[Dict[str, str | int | bool]] = None,
    ):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.children is None:
            raise ValueError("The children property is required for ParentNode")

        if self.tag is None:
            raise ValueError("The tag property is required for ParentNode")

        content_string = "".join(map(lambda tag: tag.to_html(), self.children))
        return f"<{self.tag}{self.props_to_html()}>{content_string}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"

    def add_children(self, children: List[HtmlNode]):
        if self.children is None:
            raise ValueError("Children can't be none for LeafNode")
        self.children += children


class LeafNode(HtmlNode):
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        props: Optional[Dict[str, str | int | bool]] = None,
    ):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("The value property is required for LeafNode")

        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
