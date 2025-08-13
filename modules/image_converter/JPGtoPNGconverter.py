import sys
from pathlib import Path
from PIL import Image

if len(sys.argv) < 3:
    print("Usage: python3 file.py param1 param2")
    sys.exit(1)

folder_path = Path("./" + sys.argv[1])
new_folder = Path(sys.argv[2]) 
new_folder.mkdir(exist_ok=True)

for file in folder_path.iterdir():
    if file.is_file():
        img = Image.open(folder_path.name + '/' + file.name)
        img.save(new_folder.name + '/' + file.stem + '.png', format="PNG")
