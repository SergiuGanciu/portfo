# set FLASK_APP=./web_server/server.py
# set FLASK_DEBUG=1
# flask run
from flask import Flask, render_template, redirect, request, abort
from pathlib import Path
import importlib
import csv
app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

# Automatically discover and register all project Blueprints
projects_folder = Path("projects")
projects = []

for project_path in projects_folder.iterdir():
    views_file = project_path / "views.py"
    if project_path.is_dir() and views_file.exists():
        spec = importlib.util.spec_from_file_location(f"{project_path.name}.views", views_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        app.register_blueprint(module.bp, url_prefix=f'/{project_path.name}')
        projects.append({
            'name': project_path.name,
            'title': getattr(module, 'TITLE', project_path.name),
            'image': f'/static/assets/images/{project_path.name}-hover.jpg',
            'endpoint': f'{project_path.name}.index'
        })

@app.route('/works')
def works():
    return render_template('works.html', projects=projects)

@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)

def write_to_file(data):
    with open('database.txt', mode='a') as database:
        email = data['email']
        subject = data['subject']
        message = data['message']
        file = database.write(f'\n{email},{subject},{message}')

def write_to_csv(data):
    with open('database.csv', mode='w', newline='') as database_csv:
        email = data['email']
        subject = data['subject']
        message = data['message']
        csv_writer = csv.writer(database_csv)
        csv_writer.writerow([email,subject,message])

@app.route('/submit_form', methods=['GET', 'POST'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        write_to_csv(data)
        return redirect("/thankyou.html")
    else:
        return "SMTH went wrong!"

if __name__ == "__main__":
    app.run(debug=True)
