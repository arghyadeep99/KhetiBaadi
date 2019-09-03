from flask import Flask, request, render_template
from PIL import Image
import os

TEST_FOLDER = os.path.join('static', 'test')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = TEST_FOLDER

from inference import get_plant_name

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        print(request.files)
        if 'file' not in request.files:
            print('file not uploaded')
            return
        image = request.files['file']
        prob, plant_name = get_plant_name(image_bytes=image)
        image = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        return render_template('result.html', disease=plant_name, category=prob, Image=image)

@app.route('/about')
def about_page():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)