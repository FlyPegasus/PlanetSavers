from flask import Flask, render_template, request, url_for, flash, redirect
import os
from inference_sdk import InferenceHTTPClient
import cv2
import plastic_detector


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['PROCESSED_FOLDER'] = 'processed/'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg'}

# allowed file extension checker method
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route("/")
@app.route("/home")
def home_view():
    return render_template("home.html", title="home")

@app.route("/plastic", methods=['GET', 'POST'])
def plastic_view():
    if request.method == 'POST':
        # Check if the POST request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']

        # If the user does not select a file, browser may submit an empty file part
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = file.filename
            #print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image = plastic_detector.transform(file_path)
            cv2.imwrite(os.path.join(app.config['PROCESSED_FOLDER'] , 'detected_' + filename), image)
            img_path = os.path.join(app.config['PROCESSED_FOLDER'] , 'detected_' + filename)
            return render_template("plastic_detected.html", image_path = img_path)
        else:
            flash('File not supported!')
    return render_template("plastic.html", title="plastic")


#testing
@app.route("/test", methods=['GET', 'POST'])
def test_view():
    if request.method == 'POST':
        # Check if the POST request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']

        # If the user does not select a file, browser may submit an empty file part
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            CLIENT = InferenceHTTPClient(
                api_url="https://detect.roboflow.com",
                api_key="jfbwoJ5zSnkPddWB4rRA"
            )

            result = CLIENT.infer(file_path, model_id="tree-counting-qiw3h/1")
            cv2.imwrite(os.path.join(app.config['PROCESSED_FOLDER'] , 'waka.jpg'), result)
            #cv2.waitKey(0)
        else:
            flash('File not supported!')
    
    return render_template("modeltest.html")


if __name__=="__main__":
    app.run(debug=True)