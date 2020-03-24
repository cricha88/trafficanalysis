from flask import Flask, escape, request, render_template
import urllib.request
from PIL import Image
import numpy as np
from skimage import transform
from keras.utils import to_categorical
from keras.models import load_model
import tensorflow as tf
import os

app = Flask(__name__)
print(os.getcwd())
#model = load_model('genCNNc.h5')

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/camera" , methods=['GET', 'POST'])
def camera():
    #get which camera was selected
    select = request.form.get('whichcam')

    #append the selected camera to create the url with the image
    url = 'https://511on.ca/map/Cctv/loc' + str(select) + '--3'

    #get image from url
    imageurl = Image.open(urllib.request.urlopen(url))
    imageurl = np.array(imageurl).astype('float32') / 255
    imageurl = transform.resize(imageurl, (480, 704, 3))
    imageurl = np.expand_dims(imageurl, axis=0)

    #load TEMPORARY model file
    # predint = model.predict_classes(imageurl)
    # if predint == 0:
    #     predstr = 'Low Congestion'
    # if predint == 1:
    #     predstr = 'Medium Congestion'
    # if predint == 2:
    #     predstr = 'High Congestion'

    # return render_template('index.html', whichcam=str(url), prediction=str(predstr))
    return render_template('index.html', whichcam=str(url))

