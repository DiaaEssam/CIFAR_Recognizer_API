from flask import Flask,request
import pandas as pd
import numpy as np
from flasgger import Swagger
import tensorflow as tf
from PIL import Image
import os

app=Flask(__name__) # it's a common step to start with this
Swagger(app) # pass the App to Swagger

current_directory = os.path.abspath(os.path.dirname(__file__))
model_path = os.path.join(current_directory, "model.h5")

classifier=tf.keras.models.load_model(model_path)

classes = {
    0:'aquatic mammals',
    1:'fish',
    2:'flowers',
    3:'food containers',
    4:'fruit and vegetables',
    5:'household electrical devices',
    6:'household furniture',
    7:'insects',
    8:'large carnivores',
    9:'large man-made outdoor things',
    10:'large natural outdoor scenes',
    11:'large omnivores and herbivores',
    12:'medium-sized mammals',
    13:'non-insect invertebrates',
    14:'people',
    15:'reptiles',
    16:'small mammals',
    17:'trees',
    18:'vehicles 1',
    19:'vehicles 2',
}
@app.route('/') # must be written to define the root page or main page to display
# this will display a web page having welcome all in it
def welcome():
    return "Welcome All"

# a page for predicting one sample, can be used through Postman
@app.route('/predict',methods=["POST"]) # by default it's GET method because we will pass our features as parameters
def predict_A_sample():
    """
    Let's see what is the coarse
    ---
    parameters:
        
        - name: image
          in: formData
          type: file
          required: true

    responses:
        200:
            description: The output value

    """
    image=request.files.get("image")

    image = Image.open(image)
    image = np.array(image.resize((224, 224)))
    image = image.reshape((1, 224, 224,3))
    print(image.shape)

    prediction=np.argmax(tf.nn.softmax(classifier.predict(image)[0]))
    return "The digit is: " + classes[prediction]

# a page for predicting csv file, can be used through Postman
@app.route('/predict_file',methods=["POST"])
def predict_A_File():

    """
    Let's see what is the coarse
    ---
    parameters:
        - name: file
          in: formData
          type: file
          required: true
    
    responses:
        200:
            description: The output values
    """
    df_test=pd.read_csv(request.files.get("file")) 
    test_data=np.array(df_test)
    test_data=test_data.reshape(test_data.shape[0],224,224,3)
    prediction=classifier.predict(test_data)
    return "The digits are: " + str(list(prediction))



if __name__=='__main__':
    app.run()