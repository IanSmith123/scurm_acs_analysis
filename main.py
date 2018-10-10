import os
from flask import Flask, request, Response, flash, redirect, url_for, send_from_directory, send_file, render_template
from werkzeug.utils import secure_filename

from analysis import get_times

ALLOWED_EXTENSIONS = ['csv']

app = Flask(__name__)

app.secret_key = "fjalkfjJKLFJKJAFu98"
app.config['UPLAOD_FOLDER'] = "upload"
app.config['DOWNLOAD_FOLDER'] = "download"


def check_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash("no selected file")
            return redirect(request.url)

        if file and check_extension(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLAOD_FOLDER'], filename)
            file.save(filepath)

            out_director = app.config['DOWNLOAD_FOLDER']
            out_file = get_times(filepath, app.config['DOWNLOAD_FOLDER'])

            # return send_file(out_path)
            return send_from_directory(directory=out_director, filename=out_file, as_attachment=True)

    with open("index.html", encoding='utf8') as f:
        con = f.read()
    return Response(con)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=80)
    # app.run(debug=True)
