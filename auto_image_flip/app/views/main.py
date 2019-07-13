import json
import os
import random
import zipfile
from collections import defaultdict
import uuid


import numpy as np
import requests
from PIL import Image
from app import app
from flask import render_template, jsonify, request, send_file, \
    Response, redirect, url_for, session
from skimage.transform import resize
from werkzeug import secure_filename

PREDICTION_LABELS = {0: 'left', 1: 'right', 2: 'upright', 3: 'upsidedown'}
CLOCKWISE_2_COUNTER_CLOCKWISE = {0: 0, 180: 180, 270: 90,
                                 90: 270}
TARGET_IMAGE_SIZE = 224

image_flips = defaultdict(int)

def preprocess_image(x):
    # @TODO Find a better way to preprocess images before sending to model
    #  for prediction
    x = resize(x, (TARGET_IMAGE_SIZE, TARGET_IMAGE_SIZE),
               mode='constant',
               anti_aliasing=False)

    # convert to 3 channel (RGB)
    x = np.stack((x,) * 3, axis=-1)

    # Make sure it is a float32, here is why
    # https://www.quora.com/When-should-I-use-tf-float32-vs-tf-float64-in-TensorFlow
    return x.astype(np.float32)

@app.route('/rotate_image', methods=['POST'])
def rotate_image_api():
    '''Rotates image by specified angle'''
    img_name, angle = json.loads(request.data).popitem()
    image_flips[img_name] = angle
    return Response(status=200)


def _rotate_image_from_label(img_path, img_direction):
    '''Rotates image upright based on it current direction.'''
    img = Image.open(img_path)
    transform_map = {'right': 90, 'upright': 0, 'left': 270, 'upsidedown': 180}
    angle = transform_map[img_direction]
    out = img.rotate(angle, expand=True)
    out.save(img_path)


def _rotate_image_from_angle(img_path, img_angle):
    '''Rotates image upright based on it current direction.'''
    img = Image.open(img_path)
    out = img.rotate(img_angle, expand=True)
    out.save(img_path)


# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config[
        'ALLOWED_EXTENSIONS']


@app.route('/upload-files', methods=['POST'])
def upload_files():
    uploaded_files = request.files.getlist("file[]")
    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            predict_rotate(path)
            image_flips[filename]
    return render_template('uploaded.html', images=image_flips.keys())


@app.route('/uploaded', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
        f.save(path)
        predict_rotate(path)
        img_name = os.path.split(path)[1]
        return render_template('uploaded.html', img_name=img_name)


def predict_rotate(path):
    """Preprocess image before sending to model for prediction and rotate it
    based on the model prediction label.

    :param path: Path to image file for prediction.
    :return: None
    """
    image = Image.open(path).convert('L')
    image.thumbnail((TARGET_IMAGE_SIZE, TARGET_IMAGE_SIZE))
    image = preprocess_image(np.array(image))
    url = app.config['HEROKU_MODEL_APP_URL']
    full_url = "{}/v1/models/tf_serving_keras_mobilenet/versions/1:predict".format(
        url)
    data = {"signature_name": "prediction",
            "instances": [{"images": image.tolist()}]}
    data = json.dumps(data)
    response = requests.post(full_url, data=data)
    response = response.json()
    highest_index = np.argmax(response['predictions'])
    _rotate_image_from_label(path, PREDICTION_LABELS[highest_index])


@app.route('/download_files/',  methods=['GET'])
def download_files():
    for image, angle in image_flips.items():
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], image)
        # Images are rotated clockwise by the angle in javascript
        # But pillow rotates the images counterclockwise
        # hence the need for angle conversion
        counter_clockwise_angle = CLOCKWISE_2_COUNTER_CLOCKWISE[angle]
        _rotate_image_from_angle(img_path, counter_clockwise_angle)
    archive_name = str(uuid.uuid4())
    archive_path = os.path.join('/tmp', archive_name)
    converted_images = image_flips.keys()
    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in converted_images:
            zipf.write(str(app.config['UPLOAD_FOLDER']) + '/' + file, file)
    image_flips.clear()
    return send_file(archive_path,
                     cache_timeout=1,
                     mimetype='zip',
                     attachment_filename='flipped_images.zip',
                     as_attachment=True)


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
