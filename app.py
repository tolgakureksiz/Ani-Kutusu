from flask import Flask, render_template, request, redirect, url_for, flash
import os
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['SECRET_KEY'] = 'loppoc29min'
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['TEMPLATES_AUTO_RELOAD'] = True

DATA_FILE = "static/description.json"

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=["GET", "POST"])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("No file part!", "danger")
            return redirect(request.url)

        file = request.files['file']
        description = request.form.get("description", "").strip()

        if file.filename == '':
            flash("No selected file!", "warning")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Load descriptions safely
            if os.path.exists(DATA_FILE):
                try:
                    with open(DATA_FILE, "r") as f:
                        data = json.load(f)
                except json.JSONDecodeError:
                    data = {}  # If JSON is empty or invalid, use an empty dict
            else:
                data = {}

            # Store the filename and description
            data[filename] = description

            # Save back to JSON
            with open(DATA_FILE, "w") as f:
                json.dump(data, f, indent=4)

            flash("File uploaded successfully!", "success")
            return redirect(url_for('upload'))

        flash("Invalid file type!", "danger")

    # Load descriptions safely
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = {}  # If JSON is empty or invalid, use an empty dict
    else:
        data = {}

    images = [{"filename": os.path.join('images', image), "description": data.get(image, "")} for image in os.listdir(app.config['UPLOAD_FOLDER'])]

    return render_template("index.html", images=images)

if __name__ == "__main__":
    app.run(debug=True)
