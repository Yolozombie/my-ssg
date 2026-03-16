import os
import shutil
import sys
from copystatic import copy_files_recursive
from gencontent import generate_page, generate_pages_recursive

def main(): 
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    if os.path.exists("docs"):
        shutil.rmtree("docs")
    os.mkdir("docs")
    copy_files_recursive("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)

main()


# os.path.exists
# os.listdir
# os.path.join
# os.path.isfile
# os.mkdir
# shutil.copygenerate_page("content/index.md", "template.html", "public/index.html", "basepath")

# shutil.rmtree



#   Right now our site always assumes that / is the root path of the site (e.g. http://localhost:8888/. Make it configurable by:

#   In main.py use the sys.argv to grab the first CLI argument to the program. Save it as the basepath. If one isn't provided, default to /.
#   Pass the basepath to the generate_pages_recursive and generate_page functions.
#   In generate_page, after you replace the {{ Title }} and {{ Content }}, replace any instances of:
#   href="/ with href="{basepath}
#   src="/ with src="{basepath}
