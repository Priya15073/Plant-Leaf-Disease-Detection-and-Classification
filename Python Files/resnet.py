# -*- coding: utf-8 -*-
"""ResNet.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1S72leDqfEdr50P4LsAmBvNxTOzkCWMjh
"""

#Priya Rajpurohit 2015073
#Sakshi Saini 2017092

import keras,os
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPool2D , Flatten
from keras.preprocessing.image import ImageDataGenerator
import numpy as np

from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np

import tensorflow_datasets as tfds
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

import keras
from keras.layers.core import Layer
import keras.backend as K

from keras.models import Model
from keras.layers import Conv2D, MaxPool2D,  \
    Dropout, Dense, Input, concatenate,      \
    GlobalAveragePooling2D, AveragePooling2D,\
    Flatten

import cv2 
import numpy as np 
from keras.datasets import cifar10 
from keras import backend as K 
from keras.utils import np_utils

import math 
from keras.optimizers import SGD 
from keras.callbacks import LearningRateScheduler
from sklearn.model_selection import train_test_split

# ds = tfds.load("plant_village", split=tfds.Split.TRAIN, batch_size=-1)
# ds = tfds.as_numpy(ds)

# images, labels = ds["image"], ds["label"]

from google.colab import drive
drive.mount('/content/drive')

!unzip -uq "/content/drive/My Drive/SML_Project/Segmented.zip"

import os

path = '/content/Segmented/'
images=[]
labels=[]
# r=root, d=directories, f = files
lable = 1
labels = []
for r, d, f in os.walk(path):
    for folder in d:
        
        for r1, d1, f1 in os.walk(os.path.join(r, folder)):
          for file in f1:
            # print(file)
            images.append( cv2.imread(os.path.join(r1, file) ))
            labels.append(lable)

          lable = lable +1
images=np.array(images)
images.shape

x_train, x_test, y_train, y_test = train_test_split( images[:20000], labels[:20000], test_size=0.2, random_state=42, shuffle=True )
print(x_train.shape, x_test.shape)

from keras.models import Model

image_input = Input(shape=(224, 224, 3))

res = ResNet50(input_tensor=image_input, weights='imagenet', include_top=False)

for layer in res.layers:
  layer.trainable = False
x = GlobalAveragePooling2D()(res.output)
x=Dropout(0.3)(x)
x=Dense(1024,activation='relu')(x) #dense layer 2
x=Dense(512,activation='relu')(x)


prediction = Dense(38, activation='softmax')(x)

# create a model object
model = Model(inputs=res.input, outputs=prediction)
model.summary()

# # X_train = np.array([cv2.resize(img, (img_rows,img_cols)) for img in X_train[:,:,:,:]])
# # X_valid = np.array([cv2.resize(img, (img_rows,img_cols)) for img in X_valid[:,:,:,:]])

# resized = []
# n = 224
# m = 224

# for image in images:
#   image = cv2.resize( image, (n, m) )
#   resized.append(image)

#images, labels = ds["image"], ds["label"]
n1 = 224
m1 = 224

features = []
for image in x_train:

  image = cv2.resize(image , (n1,m1) )

  image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
  image = preprocess_input(image)

  feature = model.predict(image)
  
  features.append(feature)

featurestest = []
for image in x_test:

  image = cv2.resize(image , (n1,m1) )

  image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
  image = preprocess_input(image)

  feature = model.predict(image)
  
  featurestest.append(feature)

features = np.array(features)
featurestest=np.array(featurestest)

print(featurestest.shape)
print(features.shape)

from sklearn.ensemble import RandomForestClassifier

features = features.reshape(16000,38)

clf = RandomForestClassifier()
clf.fit(features,  y_train)
featurestest = featurestest.reshape(4000, 38)

accuracy = clf.score(featurestest,y_test)
accuracy *= 100
print(accuracy)
import h5py


h5_data    = 'segmented_resnet.h5'
h5_labels  = 'labels_resnet_seg.h5'

h5f_data = h5py.File(h5_data, 'w')
h5f_data.create_dataset('dataset_1', data=np.array(features))

h5f_label = h5py.File(h5_labels, 'w')
h5f_label.create_dataset('dataset_1', data=np.array(labels))

import pickle


filename = 'resnet_rf_model_color.sav'
pickle.dump(clf, open(filename, 'wb'))

from sklearn import svm

features = features.reshape(16000,38)

clf1 = svm.SVC()
clf1.fit(features,  y_train)
featurestest = featurestest.reshape(4000, 38)

accuracy = clf1.score(featurestest,y_test)
accuracy *= 100
print(accuracy)
import h5py





filename = 'resnet_svm_model_color.sav'
pickle.dump(clf1, open(filename, 'wb'))

!pip3 install elm
!pip3 install --upgrade numpy folium imgaug

import elm
elmk=elm.ELMKernel()
elmk.search_param(data, cv="kfold", of="accuracy", eval=10)

tr_result = elmk.train(features,y_train)
te_result = elmk.test(featurestest,y_test)

print(te_result.get_accuracy)