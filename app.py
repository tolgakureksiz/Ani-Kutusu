from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['SECRET_KEY'] = 'loppoc29min'
app.config['UPLOAD_FOLDER'] = 'static/images'  # Fixed this

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=["GET", "POST"])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("No file part!", "danger")
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash("No selected file!", "warning")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash("File uploaded successfully!", "success")
            return redirect(url_for('upload'))

        flash("Invalid file type!", "danger")
    images = os.listdir(app.config['UPLOAD_FOLDER'])
    images = [os.path.join('images', image) for image in images]
    return render_template("testhi.html", images = images)

if __name__ == "__main__":
    app.run(debug=True)
