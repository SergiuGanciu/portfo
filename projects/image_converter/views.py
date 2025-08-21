from flask import Blueprint, render_template, request, send_file
from io import BytesIO
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
    url_prefix=f"/{project_name}"
)

@bp.route("/")
def index():
    return render_template(f"{project_name}/index.html", project_name=project_name)

@bp.route("/process", methods=["POST"])
def process():
    uploaded_file = request.files.get("image")
    if not uploaded_file:
        return "No file uploaded", 400

    # Get format
    output_format = request.form.get("format", "PNG").upper()
    
    # Pillow works with JPEG. Users mostly use JPG
    if output_format == "JPG":
        save_format = "JPEG"
        download_ext = "jpg"
    else:
        save_format = output_format
        download_ext = output_format.lower()

    # Open and convert
    img = Image.open(uploaded_file)
    
    # If save format is JPEG convert it to RGB
    if save_format == "JPEG":
        if img.mode in ("RGBA", "LA"):
            # RGBA → RGB
            background = Image.new("RGB", img.size, (255, 255, 255))
            alpha_channel = img.split()[3] if img.mode == "RGBA" else None
            background.paste(img, mask=alpha_channel)
            img = background
        elif img.mode == "P":  
            # Palette → RGB
            img = img.convert("RGB")
    
    output_io = BytesIO()
    img.save(output_io, format=save_format)
    output_io.seek(0)

    return send_file(
        output_io,
        mimetype=f"image/{download_ext}",
        as_attachment=True,
        download_name=f"converted.{download_ext}"
    )

if __name__ == "__main__":
    bp.run(debug=True)
