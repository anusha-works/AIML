#importing required libraries

from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from sklearn import metrics 
import warnings
import pickle
warnings.filterwarnings('ignore')
from feature2 import FeatureExtraction

file = open("pickle/model.pkl","rb")
gbc = pickle.load(file)
file.close()


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        url = request.form["url"]
        obj = FeatureExtraction(url)
        x = np.array(obj.getFeaturesList()).reshape(1,30) 

        y_pred =gbc.predict(x)
        #1 is safe       
        #-1 is unsafe
        if(y_pred ==1 ):
            pred = "It is safe to go "
        else:
            pred = "It's not safe"
        return render_template('index.html',xx =pred,url=url)
    return render_template("index.html", xx =-1)


if __name__ == "__main__":
    app.run(debug=True, host='localhost',port=3000)