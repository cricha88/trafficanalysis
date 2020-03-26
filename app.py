from flask import Flask, escape, request, render_template
import urllib.request
from PIL import Image
import numpy as np
from skimage import transform, io
from keras.utils import to_categorical
import keras.models
import cv2
import tensorflow as tf
import os
from matplotlib import pyplot
import math


app = Flask(__name__)
print(os.getcwd())
#load temporary model files
model_con = keras.models.load_model('genCNNc.h5')
model_lt = keras.models.load_model('initCNNl.h5')

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/camera" , methods=['GET', 'POST'])
def camera():
    #get which camera was selected
    select = request.form.get('whichcam')

    #append the selected camera to create the url with the image
    url = 'https://511on.ca/map/Cctv/loc' + str(select) + '--3'

    urllib.request.urlretrieve(url, "downloaded.jpg")
    img = cv2.imread('downloaded.jpg')
    image = np.array(img)
    if image.shape != (480, 704, 3):
        predstr_con = 'Current image is invalid'
        predstr_lt = 'Current image is invalid'
    else:
        image = image / 255.0
        image = image.reshape(-1, 480, 704, 3)

        predint_con = model_con.predict_classes(image)
        if predint_con == 0:
            predstr_con = 'Low Congestion'
        elif predint_con == 1:
            predstr_con = 'Medium Congestion'
        elif predint_con == 2:
            predstr_con= 'High Congestion'

        predint_lt = model_lt.predict_classes(image)
        if predint_lt == 0:
            predstr_lt = 'Dark'
        elif predint_lt == 1:
            predstr_lt = 'Bright'

    return render_template('index.html', whichcam=str(url), pred_con=predstr_con, pred_lt=predstr_lt)

@app.route("/map.html" , methods=['POST'])
def map():
    pred = []

    for i in range(15,25):
        url = 'https://511on.ca/map/Cctv/loc' + str(i) +'--3'
        urllib.request.urlretrieve(url, "downloaded.jpg")
        img = cv2.imread('downloaded.jpg')
        image = np.array(img)

        if image.shape != (480, 704, 3):
            pred.append('Current image is invalid')
        else:
            image = image / 255.0
            image = image.reshape(-1, 480, 704, 3)

            predint = model_con.predict_classes(image)
            if predint == 0:
                predstr = 'Low Congestion'
            elif predint == 1:
                predstr = 'Medium Congestion'
            elif predint == 2:
                predstr= 'High Congestion'

            pred.append(predstr)

    return render_template('map.html', pred=pred)

