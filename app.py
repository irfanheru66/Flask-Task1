import os
import shutil
from flask import Flask, render_template, request, redirect, url_for
from image import saves_image

sourceImg = "static/source.jpg"
app = Flask(__name__)
@app.route('/', methods=['GET','POST'])
def index ():
    if(request.method == 'GET'):
        return render_template("upload.html")

    elif(request.method == 'POST'):
        image = request.files['image']
        image.save(sourceImg)
        saves_image(sourceImg)
        return render_template('result.html')
        

if __name__ == '__main__':
    os.makedirs('static', exist_ok=True)
    app.run(host='0.0.0.0', port=5000)
    shutil.rmtree('static')