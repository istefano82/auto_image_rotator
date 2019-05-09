import os
import random
from PIL import Image

import numpy as np
from app import app
from flask import render_template, jsonify, request
from keras.applications.resnet50 import preprocess_input
from keras.preprocessing import image

def _rotate_image(img_path, img_direction):
    '''Rotates image upright based on it current direction.'''
    img = Image.open(img_path)
    transform_map = {'right': 90, 'upright': 0, 'left': 270, 'upsidedown': 180}
    angle = transform_map[img_direction]
    out = img.rotate(angle, expand=True)
    out.save(img_path)

@app.route('/upload')
def upload_file2():
    return render_template('index.html')


@app.route('/uploaded', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        model = app.model
        graph = app.graph
        f = request.files['file']
        path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
        f.save(path)
        img = image.load_img(path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        with graph.as_default():
            preds_class = model.predict_classes(x)[0]
        print(preds_class)
        pred_classes = ['right', 'upright', 'left', 'upsidedown']
        _rotate_image(path, pred_classes[preds_class])
        img_name = os.path.split(path)[1]
        return render_template('uploaded.html', img_name=img_name)

@app.route('/')
@app.route('/index')
def index():
    return render_template('user/charge.html', title='Home')


@app.route('/map')
def map():
    return render_template('map.html', title='Map')


@app.route('/map/refresh', methods=['POST'])
def map_refresh():
    points = [(random.uniform(48.8434100, 48.8634100),
               random.uniform(2.3388000, 2.3588000))
              for _ in range(random.randint(2, 9))]
    return jsonify({'points': points})


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')
