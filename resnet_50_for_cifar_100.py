# -*- coding: utf-8 -*-
"""resnet-50-for-cifar-100.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1p3a6EZBcwOMBN8A89xjd1fhcRaZ8O3ro
"""

import numpy as np
from tensorflow.keras import regularizers
from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.regularizers import l2
import tensorflow as tf
import tensorflow.keras.layers as tfl
from keras import backend as K

from tensorflow.keras.datasets import cifar100

(X_train, y_train), (X_test, y_test) = cifar100.load_data(label_mode='coarse')

print(X_train.shape,y_train.shape)

from sklearn.preprocessing import OneHotEncoder

enc = OneHotEncoder()
y_train=enc.fit_transform(y_train).toarray().astype(int)
y_test=enc.transform(y_test).toarray().astype(int)


print(y_train.shape)
print(y_train[0])

X_train = X_train.astype('float32')
X_test = X_test.astype('float32')

def normalize(X):
    return X/255.0

X_train=normalize(X_train)
X_test=normalize(X_test)

train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)


test_datagen = ImageDataGenerator(rescale=1. / 255)

def identity_block(X, f, filters):
    X_shortcut=X

    X=tfl.Conv2D(filters=filters[0],kernel_size=1,strides=(1,1), padding='valid',kernel_regularizer=regularizers.L1(0.001),
                     activity_regularizer=regularizers.L2(0.001))(X)
    X=tfl.BatchNormalization(axis=3)(X, training=True)
    X=tfl.Activation('relu')(X)

    X=tfl.Conv2D(filters=filters[1],kernel_size=f,strides=(1,1), padding='same', kernel_regularizer=regularizers.L1(0.001),
                     activity_regularizer=regularizers.L2(0.001))(X)
    X=tfl.BatchNormalization(axis=3)(X, training=True)
    X=tfl.Activation('relu')(X)

    X=tfl.Conv2D(filters=filters[2],kernel_size=1,strides=(1,1), padding='valid',kernel_regularizer=regularizers.L1(0.001),
                     activity_regularizer=regularizers.L2(0.001))(X)
    X=tfl.BatchNormalization(axis=3)(X, training=True)

    X=tfl.Add()([X_shortcut,X])
    X=tfl.Activation('relu')(X)

    return X

def convolutional_block(X, f, filters, s=2):
    X_shortcut=X

    X=tfl.Conv2D(filters=filters[0],kernel_size=1,strides=(s,s), padding='valid',kernel_regularizer=regularizers.L1(0.001),
                     activity_regularizer=regularizers.L2(0.001))(X)
    X=tfl.BatchNormalization(axis=3)(X, training=True)
    X=tfl.Activation('relu')(X)

    X=tfl.Conv2D(filters=filters[1],kernel_size=f,strides=(1,1), padding='same')(X)
    X=tfl.BatchNormalization(axis=3)(X, training=True)
    X=tfl.Activation('relu')(X)

    X=tfl.Conv2D(filters=filters[2],kernel_size=1,strides=(1,1), padding='valid', kernel_regularizer=regularizers.L1(0.001),
                     activity_regularizer=regularizers.L2(0.001))(X)
    X=tfl.BatchNormalization(axis=3)(X, training=True)

    X_shortcut=tfl.Conv2D(filters=filters[2],kernel_size=1,strides=(s,s), padding='valid', kernel_regularizer=regularizers.L1(0.001),
                     activity_regularizer=regularizers.L2(0.001))(X_shortcut)
    X_shortcut=tfl.BatchNormalization(axis=3)(X_shortcut, training=True)

    X=tfl.Add()([X_shortcut,X])
    X=tfl.Activation('relu')(X)

    return X

def arch(input_shape):

    input_img = tf.keras.Input(shape=input_shape)

    layer =tfl.ZeroPadding2D((3, 3))(input_img)

    layer=tfl.Conv2D(filters=64,kernel_size=7,strides=(2,2))(layer)
    layer=tfl.BatchNormalization(axis=3)(layer, training=True)
    layer=tfl.Activation('relu')(layer)
    layer=tfl.MaxPooling2D((3, 3), strides=(2, 2))(layer)

    layer=convolutional_block(layer,3,[64,64,256],1)
    layer=identity_block(layer,3,[64,64,256])
    layer=identity_block(layer,3,[64,64,256])

    layer=convolutional_block(layer,3,[128,128,512],2)
    layer=identity_block(layer,3,[128,128,512])
    layer=identity_block(layer,3,[128,128,512])
    layer=identity_block(layer,3,[128,128,512])

    layer=convolutional_block(layer,3, [256, 256, 1024],2)
    layer=identity_block(layer,3, [256, 256, 1024])
    layer=identity_block(layer,3, [256, 256, 1024])
    layer=identity_block(layer,3, [256, 256, 1024])
    layer=identity_block(layer,3, [256, 256, 1024])
    layer=identity_block(layer,3, [256, 256, 1024])

    layer=convolutional_block(layer,3, [512, 512, 2048],2)
    layer=identity_block(layer,3, [512, 512, 2048])
    layer=identity_block(layer,3, [512, 512, 2048])

    layer=tfl.AveragePooling2D(pool_size=(2, 2),padding='same')(layer)
    layer=tfl.Flatten()(layer)

    outputs=tfl.Dense(units= 20 , activation='softmax')(layer)
    model = tf.keras.Model(inputs=input_img, outputs=outputs)
    return model

conv_model = arch((32, 32, 3))
conv_model.compile(optimizer='SGD',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
conv_model.summary()

train_data=train_datagen.flow(X_train,y_train,batch_size=64)
val_data=test_datagen.flow(X_test,y_test,batch_size=64)
history = conv_model.fit(train_data,epochs=70,validation_data=val_data,batch_size=64,shuffle=True)