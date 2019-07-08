import json
import os
import random
import zipfile

import numpy as np
import requests
from PIL import Image
from app import app
from flask import render_template, jsonify, request, session, send_file
from skimage.transform import resize
from werkzeug import secure_filename

PREDICTION_LABELS = {0: 'left', 1: 'right', 2: 'upright', 3: 'upsidedown'}
TARGET_IMAGE_SIZE = 224


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


def _rotate_image(img_path, img_direction):
    '''Rotates image upright based on it current direction.'''
    img = Image.open(img_path)
    transform_map = {'right': 90, 'upright': 0, 'left': 270, 'upsidedown': 180}
    angle = transform_map[img_direction]
    out = img.rotate(angle, expand=True)
    out.save(img_path)


# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config[
        'ALLOWED_EXTENSIONS']


@app.route('/upload-files', methods=['POST'])
def upload_files():
    uploaded_files = request.files.getlist("file[]")
    filenames = []
    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            predict_rotate(path)
            filenames.append(filename)
    session['filenames'] = filenames
    return render_template('uploaded.html', images=filenames)


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
    _rotate_image(path, PREDICTION_LABELS[highest_index])


@app.route('/download_files/')
def download_files():
    archive_path = '/tmp/flipped_images.zip'
    converted_images = session['filenames']
    zipf = zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED)
    for file in converted_images:
        zipf.write(str(app.config['UPLOAD_FOLDER']) + '/' + file, file)
    zipf.close()
    return send_file(archive_path,
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
