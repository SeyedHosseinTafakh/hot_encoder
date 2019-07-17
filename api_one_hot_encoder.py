# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 02:01:16 2019

@author: Hossein
"""

import os
import werkzeug
from flask import Flask, jsonify , send_from_directory,send_file
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)
import mysql.connector
import json
import pandas as pd

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns; sns.set(style="ticks", color_codes=True)
from joblib import dump, load
from sklearn.preprocessing import OneHotEncoder
import numpy as np


global global_model
global column_names

class elbow(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('column_names',required=True)
        parser.add_argument('file', type=werkzeug.datastructures.FileStorage,location='files')
        args = parser.parse_args()
        file = args['file']
        file.save("file.csv")
        dataset = pd.read_csv('file.csv')
        global column_names
        column_names = args['column_names'].split(',')
        
        hot_encoder = OneHotEncoder()
        hot_encoder.fit_transform(dataset[column_names])
        global global_model
        global_model = hot_encoder
        s = hot_encoder.get_feature_names(column_names)
        return (s.tolist())
    
class transforms(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        global column_names
        for coloumn in column_names:
            parser.add_argument(name = coloumn , required=True)
        args = parser.parse_args()
        columns_dataframe=[]
        values_dataframe =[]
        for arg in args:
            columns_dataframe.append(arg)
            if args[arg].isdigit():
                value = float(args[arg])
            else:
                value = args[arg]
            values_dataframe.append(value)
        df = pd.DataFrame([values_dataframe] , columns=columns_dataframe)
        global global_model
        try :
            values = global_model.transform(df)
        except ValueError:
                return "Found unknown categories"
        values = values.todense().tolist()
        values = values[0]
        i = 0
        ret ={}
        s = global_model.get_feature_names(column_names).tolist()
        while i <= (len(s) -1):
            ret[s[i]] = values[i]
            i = i +1
        return ret
    
    
@app.route('/download', methods=['GET', 'POST'])
def download():
    parser = reqparse.RequestParser()
    parser.add_argument('file_name',required=True)
    args = parser.parse_args()
    path = 'files/'+ args['file_name']
    return send_file(path,as_attachment=True)




api.add_resource(elbow, '/')
api.add_resource(transforms, '/transform')
# app.run(host='192.168.43.7',debug=True)
app.run(debug=True)
        
        
        