from flask import Blueprint, render_template, request, jsonify
from pathlib import Path
import requests
import hashlib

project_path = Path(__file__).parent
project_name = project_path.name
TITLE = "Password Checker"

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


def request_api_data(query_check):
    url = 'https://api.pwnedpasswords.com/range/' + str(query_check)
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error code: {res.status_code}. check api work!')
    
    return res

def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


@bp.route("/pwned_api_check", methods=["POST"])
def pwned_api_check():
    data = request.get_json()
    password = data.get("password")
    sha1pass = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1pass[:5], sha1pass[5:]
    response = request_api_data(first5_char) 
    count = get_password_leaks_count(response, tail)
    
    if count:
        result = f"⚠️ Password found {count} time(s)!"
    else:
        result = "✅ Not found."

    return jsonify({"result": result})


if __name__ == "__main__":
    bp.run(debug=True)
