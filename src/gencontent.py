import os
from markdown_blocks import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.splitlines()  # <-- geen file open hier, want input is string (content)
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith('# '):
            return stripped[2:].strip()
        elif stripped.startswith('#'):
            return stripped[1:].strip()
    raise Exception("No H1 header found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    file_from_path = open(from_path, "r")
    markdown_contents = file_from_path.read()
    file_from_path.close()
    
    file_template_path = open(template_path, "r")
    template = file_template_path.read()
    file_template_path.close()

    node = markdown_to_html_node(markdown_contents)
    html = node.to_html()
    title = extract_title(markdown_contents)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)
    to_file.close()


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    path_content = os.listdir(dir_path_content)
    for dir_path in path_content:
        full_path = os.path.join(dir_path_content, dir_path)
        if os.path.isfile(full_path) and dir_path == "index.md":
            generate_page(full_path, template_path, os.path.join(dest_dir_path, "index.html"))
        elif os.path.isdir(full_path):
            generate_pages_recursive(full_path, template_path, os.path.join(dest_dir_path, dir_path))