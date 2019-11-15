'''
Article on testing TF llite model with

https://github.com/tensorflow/tensorflow/blob/master/tensorflow/lite/examples/python/label_image.py
'''

import numpy as np
import tensorflow as tf
from PIL import Image

TARGET_IMAGE_SIZE = 224



labels =  {0: 'left', 1: 'right', 2: 'upright', 3: 'upsidedown'}
image_path = '/home/ivo/Downloads/airplane_0010.jpg'

TFLITE_MODEL = "models/export/image_flip.tflite"

interpreter = tf.lite.Interpreter(model_path=TFLITE_MODEL)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print(input_details)
print(output_details)

# check the type of the input tensor
floating_model = input_details[0]['dtype'] == np.float32

# NxHxWxC, H:1, W:2
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]
img = Image.open(image_path).resize((width, height))

# add N dim
input_data = np.expand_dims(img, axis=0)
input_mean = 127.5
input_std = 127.5

if floating_model:
    input_data = (np.float32(input_data) - input_mean) / input_std

interpreter.set_tensor(input_details[0]['index'], input_data)

interpreter.invoke()

output_data = interpreter.get_tensor(output_details[0]['index'])
results = np.squeeze(output_data)

top_k = results.argsort()[-5:][::-1]
for i in top_k:
    if floating_model:
        print('{:08.6f}: {}'.format(float(results[i]), labels[i]))
    else:
        print('{:08.6f}: {}'.format(float(results[i] / 255.0), labels[i]))