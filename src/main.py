import os
import shutil

from block_markdown import markdown_to_html_node, extract_title
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
            print(f"{destination_item_path} exists: {os.path.exists(destination_item_path)}")
            copy_content(source_item_path, destination_item_path)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as markdown_file:
        markdown_file_data = markdown_file.read()
    html_string = markdown_to_html_node(markdown_file_data).to_html()
    with open(template_path) as template_file:
        template = template_file.read()
    title = extract_title(markdown_file_data)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_string)
    if not os.path.exists(dest_path):
        os.mknod(dest_path)
    with open(dest_path, "w") as destination:
        destination.write(template)

def generate_pages_recursively(content_directory_path, template_path, destination_directory_path):
    list_dir_content = os.listdir(content_directory_path)
    for item in list_dir_content:
        content_item_path = os.path.join(content_directory_path, item)
        destination_item_path = os.path.join(destination_directory_path, item)
        destination_item_path = destination_item_path.replace(".md", ".html")
        if os.path.isfile(content_item_path) and content_item_path.endswith(".md"):
            print(f"Generated {content_item_path} using {template_path} as {destination_item_path}")
            generate_page(content_item_path, template_path, destination_item_path)
        elif os.path.isdir(content_item_path):
            print(f"mkdir {destination_item_path}")
            os.mkdir(destination_item_path)
            print(f"{destination_item_path} exists: {os.path.exists(destination_item_path)}")
            generate_pages_recursively(content_item_path, template_path, destination_item_path)

def main():
    source_path = "content/"
    template_path = "template.html"
    destination_path = "public/"

    if os.path.exists("public/"):
        print("public/ exists\rmtree public/")
        shutil.rmtree("public/")
    if not os.path.exists("public/"):
        print("public/ directory does not exists, mkdir public/")
        os.mkdir("public/")
        if os.path.exists("public/"):
            print("public/ exists")
            copy_content("static/", "public/")
            if os.listdir("static/") == os.listdir("public/"):
                print("---Copy from static/ to public/ successful---")
            print("ls static/", os.listdir("static/"))
            print("ls public/", os.listdir("public/"))
    print("Hello, World!")

    generate_pages_recursively(source_path, template_path, destination_path)


if __name__ == "__main__":
    main()

