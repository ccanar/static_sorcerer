import os
import shutil
import sys

from block_markdown import extract_title, markdown_to_html_node


# rm -rf public/*
# cp -r static/* public/
def copy_content(source, destination):
    list_dir_source = os.listdir(source)
    for item in list_dir_source:
        source_item_path = os.path.join(source, item)
        destination_item_path = os.path.join(destination, item)
        if os.path.isfile(source_item_path):
            print(f"Copy {source_item_path} to {destination_item_path}")
            shutil.copy(os.path.join(source, item), os.path.join(destination, item))
        elif os.path.isdir(source_item_path):
            print(f"mkdir {destination_item_path}")
            os.mkdir(destination_item_path)
            print(
                f"{destination_item_path} exists: {os.path.exists(destination_item_path)}"
            )
            copy_content(source_item_path, destination_item_path)


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as markdown_file:
        markdown_file_data = markdown_file.read()
    html_string = markdown_to_html_node(markdown_file_data).to_html()
    with open(template_path) as template_file:
        template = template_file.read()
    title = extract_title(markdown_file_data)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_string)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    if not os.path.exists(dest_path):
        os.mknod(dest_path)
    with open(dest_path, "w") as destination:
        destination.write(template)


def generate_pages_recursively(
    content_directory_path, template_path, destination_directory_path, basepath
):
    list_dir_content = os.listdir(content_directory_path)
    for item in list_dir_content:
        content_item_path = os.path.join(content_directory_path, item)
        destination_item_path = os.path.join(destination_directory_path, item)
        destination_item_path = destination_item_path.replace(".md", ".html")
        if os.path.isfile(content_item_path) and content_item_path.endswith(".md"):
            print(
                f"Generated {content_item_path} using {template_path} as {destination_item_path}"
            )
            generate_page(
                content_item_path, template_path, destination_item_path, basepath
            )
        elif os.path.isdir(content_item_path):
            print(f"mkdir {destination_item_path}")
            os.mkdir(destination_item_path)
            print(
                f"{destination_item_path} exists: {os.path.exists(destination_item_path)}"
            )
            generate_pages_recursively(
                content_item_path, template_path, destination_item_path, basepath
            )


def main():
    if len(sys.argv) <= 1:
        basepath = "/"
    else:
        basepath = sys.argv[1]

    static_path = "static/"
    source_path = "content/"
    template_path = "template.html"
    destination_path = "docs/"

    if os.path.exists(destination_path):
        print(f"{destination_path} exists\rmtree {destination_path}")
        shutil.rmtree(destination_path)
    if not os.path.exists(destination_path):
        print(f"{destination_path} directory does not exists, mkdir {destination_path}")
        os.mkdir(destination_path)
        if os.path.exists(destination_path):
            print(f"{destination_path} exists")
            copy_content(static_path, destination_path)
            if os.listdir(static_path) == os.listdir(destination_path):
                print(f"---Copy from static/ to {destination_path} successful---")
            print("ls static/", os.listdir(static_path))
            print(f"ls {destination_path}", os.listdir(destination_path))
    print("Hello, World!")

    generate_pages_recursively(source_path, template_path, destination_path, basepath)


if __name__ == "__main__":
    main()