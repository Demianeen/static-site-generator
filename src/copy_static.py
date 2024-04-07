import os
import shutil


# Note: Yes, I know there is a shutil.copytree function that would eliminate the need for recursion entirely, but like, do you want to just download Hugo and skip this project? No! We go to the moon, not because it is easy, but because it is hard!
def copy_static_recursive(src: str, dest: str):
    if not os.path.exists(dest):
        os.mkdir(dest)
    dir_contents = os.listdir(src)
    for content in dir_contents:
        content_path = os.path.join(src, content)
        dest_path = os.path.join(dest, content)
        print(f" * {content_path} -> {dest_path}")
        if os.path.isfile(content_path):
            shutil.copy(content_path, dest_path)
            continue
        copy_static_recursive(content_path, dest_path)
