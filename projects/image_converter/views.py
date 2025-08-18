import sys
from flask import Blueprint, render_template
from pathlib import Path
from PIL import Image

project_path = Path(__file__).parent
project_name = project_path.name
TITLE = "Image Converter"

bp = Blueprint(
    project_name,
    __name__,
    template_folder=str(project_path / "templates"),
    static_folder=str(project_path / "static"),
    url_prefix=f"/works/{project_name}"
)

@bp.route("/")
def index():
    return render_template(f"{project_name}/index.html")

# Project code
# if len(sys.argv) < 3:
#     print("Usage: python3 file.py param1 param2")
#     sys.exit(1)

# folder_path = Path("./" + sys.argv[1])
# new_folder = Path(sys.argv[2]) 
# new_folder.mkdir(exist_ok=True)

# for file in folder_path.iterdir():
#     if file.is_file():
#         img = Image.open(folder_path.name + '/' + file.name)
#         img.save(new_folder.name + '/' + file.stem + '.png', format="PNG")
