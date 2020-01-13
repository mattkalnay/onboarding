from flask import Flask, render_template, request, redirect, session, send_file
from mysqlconnection import connectToMySQL

import os

from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["IMAGE_UPLOADS"] = "/Users/matthewkalnay/Desktop/Onboarding Files/Hitachi Chemical Onboarding/static/img/uploads"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG", "JPG", "JPEG", "GIF", "PDF"]

@app.route('/')
def index():
    mysql= connectToMySQL('hitachi_docs')

    return render_template('index.html')

@app.route('/benefits')
def benefits():
    names = []

    for filename in os.listdir(app.config["IMAGE_UPLOADS"]):
        names.append(filename)
    return render_template('benefits.html', names = names)

@app.route('/return-files/<filename>')
def return_files(filename):
    print(filename)
    return send_file("/Users/matthewkalnay/Desktop/Onboarding Files/Hitachi Chemical Onboarding/static/img/uploads/" + filename)



@app.route('/expats')
def expats():
    return render_template('expats.html')

@app.route('/recruiting')
def recruiting():
    return render_template('recruiting.html')

@app.route('/training')
def training():
    return render_template('training.html')

@app.route('/programs')
def programs():
    return render_template('programs.html')

@app.route('/policies')
def policies():
    return render_template('policies.html')

@app.route('/information')
def information():
    return render_template('information.html')

def allowed_image(filename):

    if not "." in filename:
        return False
    
    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config['ALLOWED_IMAGE_EXTENSIONS']:
        return True
    else:
        return False

@app.route('/add-doc', methods=['GET', 'POST'])
def add_doc():
    if request.method == "POST":

        if request.files:

            image = request.files["image"]

            if image.filename == "":
                print("Image must have a filename")
                return redirect(request.url)

            if not allowed_image(image.filename):
                print("That image extension is not allowed")
                return redirect(request.url)

            else: 
                filename = secure_filename(image.filename)

                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))

            print("Image saved")

            return redirect('/benefits')

    return render_template("upload.html")

@app.route('/delete-files/<filename>')
def remove_doc(filename):
    # print(app.config["IMAGE_UPLOADS"] + '/' + filename)
    os.remove(app.config["IMAGE_UPLOADS"] + '/' + filename) 
    return redirect('/benefits')


if __name__ == '__main__':
    app.run(debug=True)