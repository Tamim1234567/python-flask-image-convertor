import cv2
from flask import Flask, render_template, request, flash
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'webp', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def proccessImage(filename, operation):
    print(f"the oparetion is {operation} and filename is {filename}")
    img = cv2.imread(f"uploads/{filename}")
    match operation:
        case "cgray":
            imgProccessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            newFilename = f"static/{filename}"
            cv2.imwrite(newFilename, imgProccessed)
            return newFilename
        case "cwebp":
            newFilename = f"static/{filename.split('.')[0]}.webp"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cpng":
            newFilename = f"static/{filename.split('.')[0]}.cpng"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cjpg":
            newFilename = f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cjpeg":
            newFilename = f"static/{filename.split('.')[0]}.jpeg"
            cv2.imwrite(newFilename, img)
            return newFilename


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        operation = request.form.get("operation")
        if 'file' not in request.files:
            flash('No file part')
            return "error"
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return "error no selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = proccessImage(filename, operation)
            flash(
                f"Your image has been processed and is available <a href='/{new}' target='_blank'>here</a>")
        return render_template("index.html")


app.run(debug=True, port=8000)
