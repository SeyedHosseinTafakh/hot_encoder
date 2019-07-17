# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 01:04:29 2019

@author: Hossein
"""


# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

train_X = pd.DataFrame({'Sex':['male', 'female']*3, 'AgeGroup':[0,15,30,45,60,75]})


from sklearn.preprocessing import OneHotEncoder



encoder = OneHotEncoder()


train_X_encoded = encoder.fit_transform(train_X[['Sex', 'AgeGroup']])

testing = train_X.iloc[[0],:]
encoder_test = encoder.transform(testing)
column_name = encoder.get_feature_names(['Sex', 'AgeGroup'])
one_hot_encoded_frame =  pd.DataFrame(train_X_encoded.todense(), columns= column_name)


print(encoder_test.todense())

encoder.get_feature_names(['Sex', 'AgeGroup'])

    