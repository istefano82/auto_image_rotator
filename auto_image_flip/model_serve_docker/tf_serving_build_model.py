import tensorflow as tf

from keras.layers import Dense,GlobalAveragePooling2D, Dropout
from keras.applications import MobileNet
from keras.models import Model
from keras.regularizers import l2

num_classes = 4

base_model = MobileNet(weights='imagenet',
                       include_top=False)  # imports the mobilenet model and discards the last 1000 neuron layer.

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
optimizer = tf.train.AdamOptimizer(1e-5)
model.compile(optimizer=optimizer, loss='categorical_crossentropy',
              metrics=['accuracy'])
model.summary()
# Save the graph to the app framework.
graph = tf.get_default_graph()

import os
import tensorflow as tf
import keras

# Import the libraries needed for saving models
# Note that in some other tutorials these are framed as coming from tensorflow_serving_api which is no longer correct
from tensorflow.python.saved_model import builder as saved_model_builder
from tensorflow.python.saved_model import tag_constants, signature_constants, signature_def_utils_impl

# images will be the input key name
# scores will be the out key name
prediction_signature = tf.saved_model.signature_def_utils.predict_signature_def(
    {
    "images": model.input
    }, {
    "scores": model.output
    })
model_name = 'tf_serving_keras_mobilenet'
# export_path is a directory in which the model will be created
export_path = os.path.join(
    tf.compat.as_bytes('models/export/{}'.format(model_name)),
    tf.compat.as_bytes('1'))

# SavedModelBuilder will create the directory if it does not exist
builder = saved_model_builder.SavedModelBuilder(export_path)

sess = keras.backend.get_session()

# Add the meta_graph and the variables to the builder
builder.add_meta_graph_and_variables(
    sess, [tag_constants.SERVING],
    signature_def_map={
        'prediction': prediction_signature,
    })
# save the graph
builder.save()