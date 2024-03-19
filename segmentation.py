# -*- coding: utf-8 -*-
"""Segmentation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1D9XgfQzZ66u3-YBjmOV_FxtLvV-gdzkp
"""

# Commented out IPython magic to ensure Python compatibility.
# общие библиотеки
import pandas as pd
import numpy as np
import os
from PIL import Image
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
!pip install tensorflow

# %matplotlib inline

from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2DTranspose, concatenate, Activation
from tensorflow.keras.layers import MaxPooling2D, Conv2D, BatchNormalization

from tensorflow.keras import backend as K
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import utils
from tensorflow.keras.preprocessing import image

# пользовательская метрика
def dice_koef(y_true, y_pred):
  return(2 * K.sum(y_true * y_pred) + 1) / (K.sum(y_true) + K.sum(y_pred) + 1)

# подключаем GDrive
from google.colab import drive
drive.mount('/content/drive')

path_1 = '/content/drive/MyDrive/drive/annotations_prepped_train'
path_2 = '/content/drive/MyDrive/drive/annotations_prepped_test'
path_3 = '/content/drive/MyDrive/drive/images_prepped_train'
path_4 = '/content/drive/MyDrive/drive/images_prepped_test'

# загружаем данные
# создаем список для уменьшительных карт сегментации для train выборки
trainSeg = []

for filename in sorted(os.listdir(path_1)):
  trainSeg.append(image.load_img(os.path.join(path_1, filename),
                                 target_size = (88, 120)))

trainSeg = [11]

# Создаем список для уменьшенных картинок тестовой выборки
testSeg = []

for filename in sorted(os.listdir([path_2])):
  testSeg.append(image.load_img(os.path.join(path_2, filename),
                                 target_size = (88, 120)))

# Создаем список для уменьшенных картинок тестовой выборки
trainIm = []

for filename in sorted(os.listdir([path_3])):
  trainIm.append(image.load_img(os.path.join(path_3, filename),
                                 target_size = (88, 120)))

# Создаем список для уменьшенных картинок тестовой выборки
testIm = []

for filename in sorted(os.listdir([path_4])):
  testIm.append(image.load_img(os.path.join(path_4, filename),
                                 target_size = (88, 120)))

trainSeg[2]

testSeg[3]

trainIm[1]

testIm[22]

# обучающая и проверочная выборки
# преобразуем картинку в массив (длина, ширина, количество каналов)
xTrain = []
for img in trainIm:
  x = image.img_to_array(img)
  xTrain.append(x)
xTrain = np.array(xTrain)

# для карт сегментации

yTrain = []

for seg in trainSeg:
  x = image.img_to_array(seg)
  yTrain.append(x)
yTrain = np.array(yTrain)

# преобразуем картинку в массив (длина, ширина, количество каналов)
xTest = []
for img in testIm:
  x = image.img_to_array(img)
  xTest.append(x)
xTest = np.array(xTest)

# для карт сегментации

yTest = []

for seg in testSeg:
  x = image.img_to_array(seg)
  yTest.append(x)
yTest = np.array(yTest)

xTrain[2]

# функции раскраски
def index2Color(index):
# назначим каждому из классов некоторый цвет

  color = (255, 255, 255) # зеачения по умолчанию

  if (index == 0): color = (200, 0 , 0)
  if (index == 1): color = (0, 200 , 0)
  if (index == 2): color = (0, 0 , 200)
  if (index == 3): color = (200, 200 , 0)
  if (index == 4): color = (200, 0 , 200)
  if (index == 5): color = (0, 200 , 200)
  if (index == 6): color = (200, 200 , 200)
  if (index == 7): color = (100, 0 , 0)
  if (index == 8): color = (0, 100 , 0)
  if (index == 9): color = (0, 0 , 100)
  if (index == 10): color = (100, 100 , 0)
  if (index == 0): color = (0, 100 , 100)

  return color

# функция которая перекрашивает пиксель
def color(dSet): #dSet - разметка
  out = []
  for pr in dSet:
    currPr = pr.copy()
    currMatr = []
    for i in range(currPr.shape[0]):
      currStr = []
      for i in range(currStr.shape[1]):
        currStr.append(index2Color(currPr[i][j][0]))

      currMatr.append(currStr)
    out.append(currMatr)
  out = np.array(out)
  out = out.astype('uint8')

  return out