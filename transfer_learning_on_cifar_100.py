# -*- coding: utf-8 -*-
"""transfer-learning-on-cifar-100.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yuzYJGxtUIp4baW_r3FPDaUKkhGtOpgE
"""

import numpy as np
import os
import tensorflow as tf
import tensorflow.keras.layers as tfl

AUTO = tf.data.experimental.AUTOTUNE

# Detect TPU, return appropriate distribution strategy
try:
    tpu = tf.distribute.cluster_resolver.TPUClusterResolver()
    print('Running on TPU ', tpu.master())
except ValueError:
    tpu = None

if tpu:
    tf.config.experimental_connect_to_cluster(tpu)
    tf.tpu.experimental.initialize_tpu_system(tpu)
    strategy = tf.distribute.TPUStrategy(tpu)
else:
    strategy = tf.distribute.get_strategy()

print("REPLICAS: ", strategy.num_replicas_in_sync)

from tensorflow.keras.datasets import cifar100

(X_train, y_train), (X_test, y_test) = cifar100.load_data(label_mode='coarse')

print(X_train.shape,y_train.shape)
print(X_test.shape,y_test.shape)

import cv2
X_train = np.array([cv2.resize(img, (224, 224)) for img in X_train])

X_test = np.array([cv2.resize(img, (224, 224)) for img in X_test])

from sklearn.preprocessing import OneHotEncoder

enc = OneHotEncoder()
y_train=enc.fit_transform(y_train).toarray().astype(int)
y_test=enc.transform(y_test).toarray().astype(int)


print(y_train.shape)
print(y_train[0])

preprocess_input = tf.keras.applications.mobilenet_v2.preprocess_input

IMG_SIZE = (224, 224)
IMG_SHAPE = IMG_SIZE + (3,)
MobileNet = tf.keras.applications.MobileNetV2(input_shape=IMG_SHAPE,
                                               include_top=False,
                                               weights='imagenet')

def transfer_from_MN(image_shape=IMG_SIZE):

    input_shape = image_shape + (3,)

    base_model = tf.keras.applications.MobileNetV2(input_shape=input_shape,
                                                   include_top=False,
                                                   weights='imagenet')

    # freeze the base model by making it non trainable
    base_model.trainable = False

    # create the input layer (Same as the imageNetv2 input size)
    inputs = tf.keras.Input(shape=input_shape)

    # data preprocessing using the same weights the model was trained on
    x = preprocess_input(inputs)

    # set training to False to avoid keeping track of statistics in the batch norm layer
    x = base_model(x, training=False)

    # use global avg pooling to summarize the info in each channel
    x = tfl.GlobalAveragePooling2D()(x)
    # include dropout with probability of 0.2 to avoid overfitting
    x = tfl.Dropout(0.2)(x)

    # use a prediction layer with one neuron (as a binary classifier only needs one)
    outputs = tfl.Dense(units=20, activation='softmax')(x)

    ### END CODE HERE

    model = tf.keras.Model(inputs, outputs)

    return model

# instantiating the model in the strategy scope creates the model on the TPU
with strategy.scope():
    CIFAR_Recognizer = transfer_from_MN(IMG_SIZE)
    CIFAR_Recognizer.compile(optimizer=tf.keras.optimizers.Adam(),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

train_dataset = tf.data.Dataset.from_tensor_slices((X_train, y_train)).batch(16 * strategy.num_replicas_in_sync)
test_dataset = tf.data.Dataset.from_tensor_slices((X_test, y_test)).batch(16 * strategy.num_replicas_in_sync)
initial_epochs = 5
history = CIFAR_Recognizer.fit(train_dataset, validation_data=test_dataset, batch_size=16 * strategy.num_replicas_in_sync,epochs=initial_epochs,shuffle=True)

current_directory = os.path.abspath(os.path.dirname(__file__))
model_path = os.path.join(current_directory, "model")
CIFAR_Recognizer.save(model_path)