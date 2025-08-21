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
    columns = request.form.getlist("columns[]")
    
    if not file or not columns:
        return jsonify({"error": "No file or columns selected"}), 400

    df = pd.read_csv(file)
    df = df[columns]

    table_html = df.to_html(classes="table table-striped table-blur", index=False, border=0)
    
    return jsonify({"table_html": table_html})

@bp.route("/generate_chart", methods=["POST"])
def generate_chart():
    file = request.files.get("file")
    chart_type = request.form.get("chart_type")
    columns = request.form.getlist("columns[]")
    
    if not file or not columns:
        return jsonify({"error": "No file or columns selected"}), 400

    df = pd.read_csv(file)
    
    img = io.BytesIO()
    
    try:
        if chart_type == "line":
            df[columns].plot(kind="line")
        elif chart_type == "bar":
            df[columns].plot(kind="bar")
        elif chart_type == "barh":
            df[columns].plot(kind="barh")
        elif chart_type == "hist":
            df[columns].plot(kind="hist", bins=20, alpha=0.7)
        elif chart_type == "box":
            df[columns].plot(kind="box")
        elif chart_type == "area":
            df[columns].plot(kind="area", alpha=0.4)
        elif chart_type == "pie" and len(columns) == 1:
            df[columns[0]].value_counts().plot(kind="pie", autopct='%1.1f%%')
        elif chart_type == "scatter" and len(columns) == 2:
            df.plot(kind="scatter", x=columns[0], y=columns[1])
        else:
            return jsonify({"error": "Invalid chart type or column selection"}), 400

        plt.tight_layout()
        plt.savefig(img, format="png")
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

        return jsonify({"chart": plot_url})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    bp.run(debug=True)
