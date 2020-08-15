# -*- coding: utf-8 -*-
"""AlexNet_color.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-F_9OkTLj2aFeqbQl8JzDOZwnOs0oLdV
"""

#Priya Rajpurohit 2015073
#Sakshi Saini 2017092

# import tensorflow as tf
# print("Tensorflow version " + tf.__version__)

# try:
#   tpu = tf.distribute.cluster_resolver.TPUClusterResolver()  # TPU detection
#   print('Running on TPU ', tpu.cluster_spec().as_dict()['worker'])
# except ValueError:
#   raise BaseException('ERROR: Not connected to a TPU runtime; please see the previous cell in this notebook for instructions!')

# tf.config.experimental_connect_to_cluster(tpu)
# tf.tpu.experimental.initialize_tpu_system(tpu)
# tpu_strategy = tf.distribute.experimental.TPUStrategy(tpu)

# import os
# try:
#     device_name = os.environ['COLAB_TPU_ADDR']
#     TPU_ADDRESS = 'grpc://' + device_name
#     print('Found TPU at: {}'.format(TPU_ADDRESS))

# except KeyError:
#     print('TPU not found')

import numpy as np
import cv2
from os import listdir
import tensorflow as tf
import pickle
from keras import backend as K 
from sklearn.preprocessing import LabelBinarizer, MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers.normalization import BatchNormalization
from tensorflow.python.keras.layers.convolutional import Conv2D, MaxPooling2D
from tensorflow.python.keras.layers.core import Activation, Flatten, Dropout, Dense, Reshape
from tensorflow.python.keras.preprocessing.image import ImageDataGenerator
from tensorflow.python.keras.preprocessing.image import img_to_array
from tensorflow.python.keras.optimizers import Adam
from tensorflow.python.keras.preprocessing import image
from tensorflow.python.keras.callbacks import ModelCheckpoint, EarlyStopping
from tensorflow.python.keras import regularizers
import matplotlib.pyplot as plt
from tensorflow.python.keras.callbacks import LearningRateScheduler
import math
from tensorflow.python.keras.utils import np_utils
from sklearn.model_selection import train_test_split

#import tensorflow.compat.v2 as tf
import tensorflow_datasets as tfds

# tfds.disable_progress_bar()
#tf.enable_v2_behavior()

# Initialize hyperparameters.
# EPOCHS = 30
EPOCHS = 25
INIT_LR = 0.005
DECAY = 0.0005
BS = 100
default_image_size = tuple((256, 256))
resized_image_size = tuple((224,224))
image_size = 0

# ds, info = tfds.load("plant_village", split="train[:80%]",shuffle_files=True,
#     as_supervised=True, with_info=True)
# ds_test,info= tfds.load("plant_village", split="train[-20%:]",shuffle_files=True,
#     as_supervised=True, with_info=True)

x_train=[]
y_train=[]
x_test=[]
y_test=[]

num_classes = 38

ds = tfds.load("plant_village", split=tfds.Split.TRAIN, batch_size=-1)
ds = tfds.as_numpy(ds)

images, labels = ds["image"], ds["label"]

# ds = tfds.load("plant_village", split='train', batch_size=-1,as_supervised=True)
# ds = tfds.as_numpy(ds)
# images, labels = ds["image"], ds["label"]



# y_train = np_utils.to_categorical(y_train, num_classes)
# y_test = np_utils.to_categorical(y_test, num_classes)

x_train, x_test, y_train, y_test = train_test_split( images[:20000], labels[:20000], test_size=0.2, random_state=42 )
print(x_train.shape, x_test.shape)

np.unique(y_train).shape
n = 38

n1 = 224
m1 = 224

x_train = np.array([cv2.resize(img, (n1,m1)) for img in x_train[:,:,:,:]])
x_test = np.array([cv2.resize(img, (n1,m1)) for img in x_test[:,:,:,:]])

# y_train = np_utils.to_categorical( y_train, n)
# y_test = np_utils.to_categorical( y_test, n)

x_train = x_train.astype('float32')/255
x_test = x_test.astype('float32')/255

# def normalize_img(image, label):
#   """Normalizes images: `uint8` -> `float32`."""
#   print(image.shape)
#   image,label=tf.cast(image, tf.float32) / 255., label
#   print(image.shape)
#   image=tf.image.resize(image, (224,224,3))
#   return image,label

# ds = ds.map(normalize_img, num_parallel_calls=tf.data.experimental.AUTOTUNE)
# ds = ds.cache()
# ds = ds.shuffle(info.splits['train'].num_examples)
# ds = ds.batch(128)
# ds = ds.prefetch(tf.data.experimental.AUTOTUNE)

# ds_test = ds_test.map(normalize_img, num_parallel_calls=tf.data.experimental.AUTOTUNE)
# ds_test = ds_test.batch(128)
# ds_test = ds_test.cache()
# ds_test = ds_test.prefetch(tf.data.experimental.AUTOTUNE)

# Initialize the model.
# with tpu_strategy.scope(): # creating the model in the TPUStrategy scope means we will train the model on the TPU
 

model = Sequential()
          
# 1st Convolutional Layer
model.add(Conv2D(filters = 96, input_shape = (224,224,3), kernel_size = (11,11), strides = (4,4), padding = 'valid'))
model.add(Activation('relu'))
# Batch Normalisation before passing it to the next layer
model.add(BatchNormalization())
# Pooling Layer
model.add(MaxPooling2D(pool_size = (3,3), strides = (2,2), padding = 'valid'))

# 2nd Convolutional Layer
model.add(Conv2D(filters = 256, kernel_size = (5,5), strides = (1,1), padding = 'same'))
model.add(Activation('relu'))
# Batch Normalisation
model.add(BatchNormalization())
# Pooling Layer
model.add(MaxPooling2D(pool_size = (3,3), strides = (2,2), padding = 'valid'))

# 3rd Convolutional Layer
model.add(Conv2D(filters = 384, kernel_size = (3,3), strides = (1,1), padding = 'same'))
model.add(Activation('relu'))
# Batch Normalisation
model.add(BatchNormalization())
# Dropout
model.add(Dropout(0.5))

# 4th Convolutional Layer
model.add(Conv2D(filters = 384, kernel_size = (3,3), strides = (1,1), padding = 'same'))
model.add(Activation('relu'))
# Batch Normalisation
model.add(BatchNormalization())
# Dropout
model.add(Dropout(0.5))

# 5th Convolutional Layer
model.add(Conv2D(filters = 256, kernel_size = (3,3), strides = (1,1), padding = 'same'))
model.add(Activation('relu'))
# Batch Normalisation
model.add(BatchNormalization())
# Pooling Layer
model.add(MaxPooling2D(pool_size = (3,3), strides = (2,2), padding = 'valid'))
# Dropout
model.add(Dropout(0.5))

# Passing it to a dense layer
model.add(Flatten())

# 1st Dense Layer
model.add(Dense(4096, input_shape = (224*224*3,)))
model.add(Activation('relu'))
# Add Dropout to prevent overfitting
model.add(Dropout(0.25))
# Batch Normalisation
model.add(BatchNormalization())

# 2nd Dense Layer
model.add(Dense(4096))
model.add(Activation('relu'))
# Add Dropout
model.add(Dropout(0.5))
# Batch Normalisation
model.add(BatchNormalization())

# 3rd Dense Layer
model.add(Dense(1000))
model.add(Activation('relu'))
# Add Dropout
model.add(Dropout(0.5))
# Batch Normalisation
model.add(BatchNormalization())

# Output Layer
model.add(Dense(38))
model.add(Activation('softmax'))

# Get the model summary.
model.summary()

# Initialize hyperparameters.
EPOCHS = 30
INIT_LR = 0.005
DECAY = 0.0005
BS = 100
default_image_size = tuple((256, 256))
resized_image_size = tuple((224,224))

# aug = ImageDataGenerator(
#     rotation_range = 20,
#     width_shift_range = 0.2,
#     height_shift_range = 0.2,
#     shear_range = 0.2, 
#     zoom_range = 0.2,
#     horizontal_flip = True, 
#     fill_mode = "nearest")

# aug.fit(x_train)

def decay(epoch, steps=100):
    initial_lrate = 0.005
    drop = 0.96
    epochs_drop = 8
    lrate = initial_lrate * math.pow(drop, math.floor((1+epoch)/epochs_drop))
    return lrate
lr_sc = LearningRateScheduler(decay)
opt = tf.keras.optimizers.SGD(lr=INIT_LR, momentum=0.9, nesterov=False)
model.compile(loss="categorical_crossentropy", optimizer = opt,metrics = ["accuracy"])

print(y_train.shape)
y_train = np_utils.to_categorical(y_train, num_classes)
y_test = np_utils.to_categorical(y_test, num_classes)
print(y_train.shape)
y_test.shape#

history = model.fit(
   x_train, y_train,
    validation_data = (x_test,y_test),
    batch_size=BS,
    callbacks = [lr_sc],
    epochs = EPOCHS )

# tpu_model = tf.contrib.tpu.keras_to_tpu_model(
#     model,
#     strategy=tf.contrib.tpu.TPUDistributionStrategy(
#         tf.contrib.cluster_resolver.TPUClusterResolver(TPU_ADDRESS)))
# tpu_model.fit(
#     train_input_fn,
#     steps_per_epoch = 60,
#     epochs=10,
# )

!mkdir -p saved_model
#tpu_model.save('saved_model/AlexNet') 
model.save('saved_model/AlexNet_color')

!zip -r AlexNet_color.zip saved_model/AlexNet_color/
#Download files
from google.colab import files
files.download('AlexNet_color.zip')

files.download('AlexNet_color.zip')

final_accuracy = history.history["val_accuracy"][-5:]
print("FINAL ACCURACY MEAN-5: ", np.mean(final_accuracy))

def display_training_curves(training, validation, title, subplot):
  ax = plt.subplot(subplot)
  ax.plot(training)
  ax.plot(validation)
  ax.set_title('model '+ title)
  ax.set_ylabel(title)
  ax.set_xlabel('epoch')
  ax.legend(['training', 'validation'])

plt.subplots(figsize=(10,10))
plt.tight_layout()
display_training_curves(history.history['accuracy'], history.history['val_accuracy'], 'accuracy', 211)
display_training_curves(history.history['loss'], history.history['val_loss'], 'loss', 212)