import os
import shutil

from copy_static import copy_static_recursive
from html_generation import generate_page_recursive

static_dir_path = "./static"
public_dir_path = "./public"


def main():
    if os.path.exists(public_dir_path):
        print("Deleting public directory...")
        shutil.rmtree(public_dir_path)

    print("Copying static files to public directory...")
    copy_static_recursive("./static", "./public")

    generate_page_recursive("./content", "template.html", "./public")


main()
