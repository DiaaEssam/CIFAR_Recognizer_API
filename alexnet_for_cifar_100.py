# -*- coding: utf-8 -*-
"""alexnet-for-cifar-100.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17zXoOe2UL6w0QTnL7t0no71m90CoO6SG
"""

import numpy as np
from tensorflow.keras import regularizers
from PIL import Image
import math
from keras.preprocessing.image import ImageDataGenerator
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

def arch(input_shape):

    input_img = tf.keras.Input(shape=input_shape)

    layer=tfl.Conv2D(filters= 96 , kernel_size= 11,strides=(4, 4))(input_img)
    layer=tfl.ReLU()(layer)
    layer=tfl.MaxPool2D(pool_size=(3, 3), strides=(2, 2), padding='same')(layer)
    layer=tfl.BatchNormalization(axis=3)(layer,training=True)

    layer=tfl.Conv2D(filters= 256 , kernel_size= 5 ,strides=(1, 1), padding='same', kernel_regularizer=regularizers.L1(0.001),
                     activity_regularizer=regularizers.L2(0.001))(layer)
    layer=tfl.ReLU()(layer)
    layer=tfl.MaxPool2D(pool_size=(3, 3), strides=(2,2), padding='same')(layer)
    layer=tfl.BatchNormalization(axis=3)(layer,training=True)

    layer=tfl.Conv2D(filters= 384 , kernel_size= 3 ,strides=(1, 1), padding='same', kernel_regularizer=regularizers.L1(0.001),
                     activity_regularizer=regularizers.L2(0.001))(layer)
    layer=tfl.ReLU()(layer)
    layer=tfl.Conv2D(filters= 384 , kernel_size= 3 ,strides=(1, 1), padding='same', kernel_regularizer=regularizers.L1(0.001),
                     activity_regularizer=regularizers.L2(0.001))(layer)
    layer=tfl.ReLU()(layer)
    layer=tfl.Conv2D(filters= 256 , kernel_size= 3 ,strides=(1, 1), padding='same')(layer)
    layer=tfl.ReLU()(layer)
    layer=tfl.MaxPool2D(pool_size=(3, 3), strides=(2,2), padding='same')(layer)
    layer=tfl.BatchNormalization(axis=3)(layer,training=True)

    layer=tfl.Flatten()(layer)

    layer=tfl.Dense(units=4096, activation='relu')(layer)
    layer=tfl.Dropout(0.2)(layer)
    layer=tfl.BatchNormalization()(layer,training=True)

    layer=tfl.Dense(units=4096, activation='relu')(layer)
    layer=tfl.Dropout(0.2)(layer)
    layer=tfl.BatchNormalization()(layer,training=True)

    layer=tfl.Dense(units=1000, activation='relu')(layer)
    layer=tfl.Dropout(0.2)(layer)
    layer=tfl.BatchNormalization()(layer,training=True)

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
history = conv_model.fit(train_data,epochs=75,validation_data=val_data,batch_size = 64,shuffle=True)

class Sample:

    # function to test a single sample
    def predict(self,image):
        image = Image.open(image)
        image = np.array(image.resize((32, 32)))
        image = image.astype('float32')
        image = image / 255.
        image = image.reshape((1, 32, 32,3))

        return np.argmax(tf.nn.softmax(conv_model.predict(image)[0]))

    # function to predict a CSV file
    def predict_file(self,df_test):
        param_X_test=np.array(df_test)
        param_X_test = param_X_test.astype('float32')
        param_X_test=normalize(param_X_test)

        y_pred=conv_model.predict(X_test)
        return np.argmax(y_pred,axis=1)



test_sample=Sample()

# look in the note
import pickle 
pickle_out=open("C:/Users/Diaa Essam/OneDrive/Documents/Python/.vscode/CIFAR_Recognizer_API/Classifier.pkl","wb")
pickle.dump(test_sample, pickle_out)
pickle_out.close()