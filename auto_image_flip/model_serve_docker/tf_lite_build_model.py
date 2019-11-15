# Requires Tensorflow 2.0.0

'''
Article on exporting TF lite model

https://medium.com/towards-artificial-intelligence/testing-tensorflow-lite-image-classification-model-e9c0100d8de3
'''

import tensorflow as tf

from tensorflow.keras.layers import Dense,GlobalAveragePooling2D, Dropout
from tensorflow.keras.applications import MobileNet
from tensorflow.keras.models import Model
from tensorflow.keras.regularizers import l2

num_classes = 4

base_model = MobileNet(weights='imagenet',
                       include_top=False,
                       input_shape=[224,224,3])  # imports the mobilenet model and discards the last 1000 neuron layer.

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu', kernel_regularizer=l2(0.01),
          bias_regularizer=l2(0.01))(
    x)  # we add dense layers so that the model can learn more complex functions and classify for better results.
x = Dropout(0.25)(x)
x = Dense(1024, activation='relu', kernel_regularizer=l2(0.01),
          bias_regularizer=l2(0.01))(x)  # dense layer 2
x = Dropout(0.25)(x)
x = Dense(512, activation='relu', kernel_regularizer=l2(0.01),
          bias_regularizer=l2(0.01))(x)  # dense layer 3
x = Dropout(0.5)(x)
preds = Dense(num_classes, activation='softmax')(x)  # final layer with softmax activation
model = Model(inputs=base_model.input, outputs=preds)
for layer in model.layers[:20]:
    layer.trainable = False
for layer in model.layers[20:]:
    layer.trainable = True
model.load_weights('/home/ivo/Projects/auto_image_rotator/auto_image_flip/app/static/saved_model/image_rotate_weights.h5')
optimizer = tf.optimizers.Adam(1e-5)

model.build([None, 224, 224, 3])

model.summary()
model.compile(optimizer=optimizer, loss='categorical_crossentropy',
              metrics=['accuracy'])
model.summary()

# Convert model to TFLite

TFLITE_MODEL = "models/export/image_flip.tflite"
TFLITE_QUANT_MODEL = "models/export/image_flip_quant.tflite"

# Get the concrete function from the Keras model.
run_model = tf.function(lambda x : model(x))

# Save the concrete function.
concrete_func = run_model.get_concrete_function(
    tf.TensorSpec(model.inputs[0].shape, model.inputs[0].dtype)
)

# Convert the model to standard TensorFlow Lite model
converter = tf.lite.TFLiteConverter.from_concrete_functions([concrete_func])
converted_tflite_model = converter.convert()
with open(TFLITE_MODEL, "wb") as tf_lite_model:
    tf_lite_model.write(converted_tflite_model)

# Convert the model to quantized version with post-training quantization
converter = tf.lite.TFLiteConverter.from_concrete_functions([concrete_func])
converter.optimizations = [tf.lite.Optimize.OPTIMIZE_FOR_SIZE]
tflite_quant_model = converter.convert()
with open(TFLITE_QUANT_MODEL, "wb") as tf_lite_quant:
    tf_lite_quant.write(tflite_quant_model)

print("TFLite models and their sizes:")