import os

from block_markdown import markdown_to_htmlnode


def extract_title(markdown: str):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:]
    raise Exception("Invalid md format: 1 level 1 header is required")


def get_file_content(path: str):
    with open(path) as target:
        return target.read()


def write_file(path: str, content: str = ""):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as file:
        file.write(content)


def generate_page(src_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {src_path} to {dest_path} using {template_path}")
    src_content = get_file_content(src_path)
    template_content = get_file_content(template_path)

    html_node = markdown_to_htmlnode(src_content)
    html = html_node.to_html()
    template_result = template_content.replace("{{ Content }}", html)

    title = extract_title(src_content)
    template_result = template_result.replace("{{ Title }}", title)

    write_file(dest_path, template_result)


def generate_page_recursive(src_dir: str, template_path: str, dest_dir: str):
    src_dir_contents = os.listdir(src_dir)
    for entry in src_dir_contents:
        src_path = os.path.join(src_dir, entry)
        dest_path = os.path.join(dest_dir, entry)
        if os.path.isfile(src_path):
            generate_page(
                src_path, template_path, f"{os.path.splitext(dest_path)[0]}.html"
            )
            continue
        generate_page_recursive(src_path, template_path, dest_path)
