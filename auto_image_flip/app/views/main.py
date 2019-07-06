import json
import os
import random

import numpy as np
import requests
from PIL import Image
from app import app
from flask import render_template, jsonify, request
from skimage.transform import resize

PREDICTION_LABELS = {0: 'left', 1: 'right', 2: 'upright', 3: 'upsidedown'}
TARGET_IMAGE_SIZE = 224


def preprocess_image(x):
    x = resize(x, (TARGET_IMAGE_SIZE, TARGET_IMAGE_SIZE),
               mode='constant',
               anti_aliasing=False)

    # convert to 3 channel (RGB)
    x = np.stack((x,) * 3, axis=-1)

    # Make sure it is a float32, here is why
    # https://www.quora.com/When-should-I-use-tf-float32-vs-tf-float64-in-TensorFlow
    return x.astype(np.float32)


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
        f = request.files['file']
        path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
        f.save(path)
        image = Image.open(path).convert('L')
        image.thumbnail((TARGET_IMAGE_SIZE, TARGET_IMAGE_SIZE))
        image = preprocess_image(np.array(image))
        # setup the request
        url = app.config['HEROKU_MODEL_APP_URL']
        full_url = "{}/v1/models/tf_serving_keras_mobilenet/versions/1:predict".format(url)

        data = {"signature_name": "prediction",
                "instances": [{"images": image.tolist()}]}
        data = json.dumps(data)

        response = requests.post(full_url, data=data)
        response = response.json()
        highest_index = np.argmax(response['predictions'])
        print(PREDICTION_LABELS[highest_index])
        _rotate_image(path, PREDICTION_LABELS[highest_index])
        img_name = os.path.split(path)[1]
        return render_template('uploaded.html', img_name=img_name)


@app.route('/')
@app.route('/index')
def index():
    # return render_template('user/charge.html', title='Home')
    return render_template('index.html')


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
