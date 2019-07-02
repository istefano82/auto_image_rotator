import requests
import json
import sys
from PIL import Image
import numpy as np
from keras.preprocessing import image
from keras.applications.mobilenet import preprocess_input
from skimage.transform import resize

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

labels =  {0: 'left', 1: 'right', 2: 'upright', 3: 'upsidedown'}
image_path = '/home/ivo/Downloads/airplane_0010.jpg'
# convert image to grayscale.
image = Image.open(image_path).convert('L')
# resize the image to 28 28 to make sure it is similar to our dataset
image.thumbnail((TARGET_IMAGE_SIZE, TARGET_IMAGE_SIZE))
image = preprocess_image(np.array(image))



# setup the request
full_url = "https://image-rotation-detector.herokuapp.com/v1/models/tf_serving_keras_mobilenet/versions/1:predict"

data = {"signature_name":"prediction",
        "instances":[{"images":image.tolist()}]}
data = json.dumps(data)

response = requests.post(full_url,data=data)
response = response.json()
highest_index = np.argmax(response['predictions'])
print(labels[highest_index])
