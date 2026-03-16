import os
import shutil
from copystatic import copy_files_recursive
from gencontent import generate_page, generate_pages_recursive

def main(): 
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")
    copy_files_recursive("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive("content", "template.html", "public")

main()


# os.path.exists
# os.listdir
# os.path.join
# os.path.isfile
# os.mkdir
# shutil.copy
# shutil.rmtree