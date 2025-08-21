from flask import Blueprint, render_template, request, jsonify
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import io, base64

project_path = Path(__file__).parent
project_name = project_path.name
TITLE = "Machine Learning Charts"

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "data.csv"

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

@bp.route("/get_columns", methods=["POST"])
def get_columns():
    file = request.files.get("file")
    
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    
    df = pd.read_csv(file)
    cols = sorted(df.columns.tolist())

    return jsonify({"columns": cols})

@bp.route("/filter_columns", methods=["POST"])
def filter_columns():
    file = request.files.get("file")
    selected_cols = request.form.getlist("columns[]")
    
    if not file or not selected_cols:
        return jsonify({"error": "No file or columns selected"}), 400

    df = pd.read_csv(file)
    df = df[selected_cols]

    table_html = df.to_html(classes="table table-striped table-blur", index=False, border=0)
    
    return jsonify({"table_html": table_html})

if __name__ == "__main__":
    bp.run(debug=True)
