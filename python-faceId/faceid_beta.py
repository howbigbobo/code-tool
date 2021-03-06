# -*- coding: utf-8 -*-
"""faceid_beta.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OynWNoWF6POTcRGFG4V7KW_EGIkUmLYI

# FaceID implementation using face embeddings and RGBD images.
Made by [Norman Di Palo](https://medium.com/@normandipalo), March 2018.

# Let's start by downloading the dataset.
"""


# import os

# os.mkdir("faceid_train")
# os.mkdir("faceid_val")

# # https://keras.io/
# import keras

# link_list = ["http://vap.aau.dk/wp-content/uploads/VAPRBGD/(2012-05-16)(151751).zip", "http://vap.aau.dk/wp-content/uploads/VAPRBGD/(2012-05-16)(153054).zip", "http://vap.aau.dk/wp-content/uploads/VAPRBGD/(2012-05-16)(154211).zip", "http://vap.aau.dk/wp-content/uploads/VAPRBGD/(2012-05-16)(160440).zip", "http://vap.aau.dk/wp-content/uploads/VAPRBGD/(2012-05-16)(160931).zip", "http://vap.aau.dk/wp-content/uploads/VAPRBGD/(2012-05-16)(161342).zip", "http://vap.aau.dk/wp-content/uploads/VAPRBGD/(2012-05-16)(163349).zip", "http://vap.aau.dk/wp-content/uploads/VAPRBGD/(2012-05-16)(164248).zip", "http://vap.aau.dk/wp-content/uploads/VAPRBGD/(2012-05-17)(141550).zip",
#              "http://vap.aau.dk/wp-content/uploads/VAPRBGD/(2012-05-17)(142154).zip", "http://vap.aau.dk/wp-content/uploads/VAPRBGD/(2012-05-17)(142457).zip", "http://vap.aau.dk/wp-content/uploads/VAPRBGD/(2012-05-17)(143016).zip", "http://vap.aau.dk/wp-content/uploads/VAPRBGD/(2012-05-18)(132824).zip", "http://vap.aau.dk/wp-content/uploads/VAPRBGD/(2012-05-18)(133201).zip", "http://vap.aau.dk/wp-content/uploads/VAPRBGD/(2012-05-18)(133846).zip",
#              "http://vap.aau.dk/wp-content/uploads/VAPRBGD/(2012-05-18)(134239).zip", "http://vap.aau.dk/wp-content/uploads/VAPRBGD/(2012-05-18)(134757).zip", "http://vap.aau.dk/wp-content/uploads/VAPRBGD/(2012-05-18)(140516).zip", "http://vap.aau.dk/wp-content/uploads/VAPRBGD/(2012-05-18)(143345).zip", "http://vap.aau.dk/wp-content/uploads/VAPRBGD/(2012-05-18)(144316).zip", "http://vap.aau.dk/wp-content/uploads/VAPRBGD/(2012-05-18)(145150).zip", "http://vap.aau.dk/wp-content/uploads/VAPRBGD/(2012-05-18)(145623).zip", "http://vap.aau.dk/wp-content/uploads/VAPRBGD/(2012-05-18)(150303).zip",
#              "http://vap.aau.dk/wp-content/uploads/VAPRBGD/(2012-05-18)(150650).zip", "http://vap.aau.dk/wp-content/uploads/VAPRBGD/(2012-05-18)(151337).zip", "http://vap.aau.dk/wp-content/uploads/VAPRBGD/(2012-05-18)(151650).zip"]
# val_list = ["http://vap.aau.dk/wp-content/uploads/VAPRBGD/(2012-05-18)(152717).zip", "http://vap.aau.dk/wp-content/uploads/VAPRBGD/(2012-05-18)(153532).zip", "http://vap.aau.dk/wp-content/uploads/VAPRBGD/(2012-05-18)(154129).zip",
#             "http://vap.aau.dk/wp-content/uploads/VAPRBGD/(2012-05-18)(154728).zip", "http://vap.aau.dk/wp-content/uploads/VAPRBGD/(2012-05-18)(155357).zip"]

# import requests
# import zipfile
# import io
# for link in link_list:
#     r = requests.get(link, stream=True)
#     z = zipfile.ZipFile(io.BytesIO(r.content))
#     z.extractall("faceid_train")
# for link in val_list:
#     r = requests.get(link, stream=True)
#     z = zipfile.ZipFile(io.BytesIO(r.content))
#     z.extractall("faceid_val")

"""# Input preprocessing.
Here we create some functions that will create the input couple for our model, both correct and wrong couples. I created functions to have both depth-only input and RGBD inputs.
"""

import numpy as np
import glob
# import matplotlib.pyplot as plt
from PIL import Image

def create_couple(file_path):
    # arbitraty choose a folder
    folder = np.random.choice(glob.glob(file_path + "*"))
    while folder == "datalab":
        folder = np.random.choice(glob.glob(file_path + "*"))
    #  print(folder)
    mat = np.zeros((480, 640), dtype='float32')
    i = 0
    j = 0
    depth_file = np.random.choice(glob.glob(folder + "/*.dat"))
    with open(depth_file) as file:
        for line in file:
            vals = line.split('\t')
            for val in vals:
                if val == "\n":
                    continue
                if int(val) > 1200 or int(val) == -1:
                    val = 1200
                mat[i][j] = float(int(val))
                j += 1
                j = j % 640

            i += 1
        mat = np.asarray(mat)
    mat_small = mat[140:340, 220:420]
    mat_small = (mat_small - np.mean(mat_small)) / np.max(mat_small)
#    plt.imshow(mat_small)
#    plt.show()

    mat2 = np.zeros((480, 640), dtype='float32')
    i = 0
    j = 0
    depth_file = np.random.choice(glob.glob(folder + "/*.dat"))
    with open(depth_file) as file:
        for line in file:
            vals = line.split('\t')
            for val in vals:
                if val == "\n":
                    continue
                if int(val) > 1200 or int(val) == -1:
                    val = 1200
                mat2[i][j] = float(int(val))
                j += 1
                j = j % 640

            i += 1
        mat2 = np.asarray(mat2)
    mat2_small = mat2[140:340, 220:420]
    mat2_small = (mat2_small - np.mean(mat2_small)) / np.max(mat2_small)
#    plt.imshow(mat2_small)
#    plt.show()
    return np.array([mat_small, mat2_small])


# print(create_couple("faceid_train/"))


def create_couple_rgbd(file_path):
    folder = np.random.choice(glob.glob(file_path + "*"))
    while folder == "datalab":
        folder = np.random.choice(glob.glob(file_path + "*"))
    #  print(folder)
    mat = np.zeros((480, 640), dtype='float32')
    i = 0
    j = 0
    depth_file = np.random.choice(glob.glob(folder + "/*.dat"))
    with open(depth_file) as file:
        for line in file:
            vals = line.split('\t')
            for val in vals:
                if val == "\n":
                    continue
                if int(val) > 1200 or int(val) == -1:
                    val = 1200
                mat[i][j] = float(int(val))
                j += 1
                j = j % 640

            i += 1
        mat = np.asarray(mat)
    mat_small = mat[140:340, 220:420]
    img = Image.open(depth_file[:-5] + "c.bmp")
    img.thumbnail((640, 480))
    img = np.asarray(img)
    img = img[140:340, 220:420]
    mat_small = (mat_small - np.mean(mat_small)) / np.max(mat_small)
#    plt.imshow(mat_small)
#    plt.show()
#    plt.imshow(img)
#    plt.show()

    mat2 = np.zeros((480, 640), dtype='float32')
    i = 0
    j = 0
    depth_file = np.random.choice(glob.glob(folder + "/*.dat"))
    with open(depth_file) as file:
        for line in file:
            vals = line.split('\t')
            for val in vals:
                if val == "\n":
                    continue
                if int(val) > 1200 or int(val) == -1:
                    val = 1200
                mat2[i][j] = float(int(val))
                j += 1
                j = j % 640

            i += 1
        mat2 = np.asarray(mat2)
    mat2_small = mat2[140:340, 220:420]
    img2 = Image.open(depth_file[:-5] + "c.bmp")
    img2.thumbnail((640, 480))
    img2 = np.asarray(img2)
    img2 = img2[160:360, 240:440]

 #   plt.imshow(img2)
 #   plt.show()
    mat2_small = (mat2_small - np.mean(mat2_small)) / np.max(mat2_small)
 #   plt.imshow(mat2_small)
 #   plt.show()

    full1 = np.zeros((200, 200, 4))
    full1[:, :, :3] = img[:, :, :3]
    full1[:, :, 3] = mat_small

    full2 = np.zeros((200, 200, 4))
    full2[:, :, :3] = img2[:, :, :3]
    full2[:, :, 3] = mat2_small
    return np.array([full1, full2])


# create_couple_rgbd("faceid_val/")


def create_wrong(file_path):
    folder = np.random.choice(glob.glob(file_path + "*"))
    while folder == "datalab":
        folder = np.random.choice(glob.glob(file_path + "*"))
    mat = np.zeros((480, 640), dtype='float32')
    i = 0
    j = 0
    depth_file = np.random.choice(glob.glob(folder + "/*.dat"))
    with open(depth_file) as file:
        for line in file:
            vals = line.split('\t')
            for val in vals:
                if val == "\n":
                    continue
                if int(val) > 1200 or int(val) == -1:
                    val = 1200
                mat[i][j] = float(int(val))
                j += 1
                j = j % 640

            i += 1
        mat = np.asarray(mat)
    mat_small = mat[140:340, 220:420]
    mat_small = (mat_small - np.mean(mat_small)) / np.max(mat_small)
 #   plt.imshow(mat_small)
 #   plt.show()

    folder2 = np.random.choice(glob.glob(file_path + "*"))
    while folder == folder2 or folder2 == "datalab":  # it activates if it chose the same folder
        folder2 = np.random.choice(glob.glob(file_path + "*"))
    mat2 = np.zeros((480, 640), dtype='float32')
    i = 0
    j = 0
    depth_file = np.random.choice(glob.glob(folder2 + "/*.dat"))
    with open(depth_file) as file:
        for line in file:
            vals = line.split('\t')
            for val in vals:
                if val == "\n":
                    continue
                if int(val) > 1200 or int(val) == -1:
                    val = 1200
                mat2[i][j] = float(int(val))
                j += 1
                j = j % 640

            i += 1
        mat2 = np.asarray(mat2)
    mat2_small = mat2[140:340, 220:420]
    mat2_small = (mat2_small - np.mean(mat2_small)) / np.max(mat2_small)
 #   plt.imshow(mat2_small)
 #   plt.show()

    return np.array([mat_small, mat2_small])


create_wrong("faceid_train/")


def create_wrong_rgbd(file_path):
    folder = np.random.choice(glob.glob(file_path + "*"))
    while folder == "datalab":
        folder = np.random.choice(glob.glob(file_path + "*"))
    mat = np.zeros((480, 640), dtype='float32')
    i = 0
    j = 0
    depth_file = np.random.choice(glob.glob(folder + "/*.dat"))
    with open(depth_file) as file:
        for line in file:
            vals = line.split('\t')
            for val in vals:
                if val == "\n":
                    continue
                if int(val) > 1200 or int(val) == -1:
                    val = 1200
                mat[i][j] = float(int(val))
                j += 1
                j = j % 640

            i += 1
        mat = np.asarray(mat)
    mat_small = mat[140:340, 220:420]
    img = Image.open(depth_file[:-5] + "c.bmp")
    img.thumbnail((640, 480))
    img = np.asarray(img)
    img = img[140:340, 220:420]
    mat_small = (mat_small - np.mean(mat_small)) / np.max(mat_small)
    #  plt.imshow(img)
    #  plt.show()
    #  plt.imshow(mat_small)
    #  plt.show()
    folder2 = np.random.choice(glob.glob(file_path + "*"))
    while folder == folder2 or folder2 == "datalab":  # it activates if it chose the same folder
        folder2 = np.random.choice(glob.glob(file_path + "*"))
    mat2 = np.zeros((480, 640), dtype='float32')
    i = 0
    j = 0
    depth_file = np.random.choice(glob.glob(folder2 + "/*.dat"))
    with open(depth_file) as file:
        for line in file:
            vals = line.split('\t')
            for val in vals:
                if val == "\n":
                    continue
                if int(val) > 1200 or int(val) == -1:
                    val = 1200
                mat2[i][j] = float(int(val))
                j += 1
                j = j % 640

            i += 1
        mat2 = np.asarray(mat2)
    mat2_small = mat2[140:340, 220:420]
    img2 = Image.open(depth_file[:-5] + "c.bmp")
    img2.thumbnail((640, 480))
    img2 = np.asarray(img2)
    img2 = img2[140:340, 220:420]
    mat2_small = (mat2_small - np.mean(mat2_small)) / np.max(mat2_small)
 #   plt.imshow(img2)
 #   plt.show()
 #   plt.imshow(mat2_small)
 #   plt.show()
    full1 = np.zeros((200, 200, 4))
    full1[:, :, :3] = img[:, :, :3]
    full1[:, :, 3] = mat_small

    full2 = np.zeros((200, 200, 4))
    full2[:, :, :3] = img2[:, :, :3]
    full2[:, :, 3] = mat2_small
    return np.array([full1, full2])


# create_wrong_rgbd("faceid_val/")[0].shape

"""# Network crafting.
Now we create the network. We first manually create the *constrative loss*, then we define the network architecture starting from the SqueezeNet architecture, and then using it as a siamese-network for embedding faces into a manifold. (the network for now is very big and could be heavily optimized, but I just wanted to show a proof-of-concept)
"""

from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Flatten, Dropout, Lambda, ELU, concatenate, GlobalAveragePooling2D, Input, BatchNormalization, SeparableConv2D, Subtract, concatenate
from keras.activations import relu, softmax
from keras.layers.convolutional import Convolution2D
from keras.layers.pooling import MaxPooling2D, AveragePooling2D
from keras.optimizers import Adam, RMSprop, SGD
from keras.regularizers import l2
from keras import backend as K


def euclidean_distance(inputs):
    assert len(inputs) == 2, \
        'Euclidean distance needs 2 inputs, %d given' % len(inputs)
    u, v = inputs
    return K.sqrt(K.sum((K.square(u - v)), axis=1, keepdims=True))


def contrastive_loss(y_true, y_pred):
    margin = 1.
    return K.mean((1. - y_true) * K.square(y_pred) + y_true * K.square(K.maximum(margin - y_pred, 0.)))
   # return K.mean( K.square(y_pred) )

#
def fire(x, squeeze=16, expand=64):
    x = Convolution2D(squeeze, (1, 1), padding='valid')(x)
    x = Activation('relu')(x)

    left = Convolution2D(expand, (1, 1), padding='valid')(x)
    left = Activation('relu')(left)

    right = Convolution2D(expand, (3, 3), padding='same')(x)
    right = Activation('relu')(right)

    x = concatenate([left, right], axis=3)
    return x

#建立神经网络
print("Network crafting====================")
#输入数据为 200 × 200 × 4 的矩阵
img_input = Input(shape=(200, 200, 4))

# 卷积输出为64维，卷积核的小矩阵为5*5, 卷积步伐是2*2像素， 启用填充？
x = Convolution2D(64, (5, 5), strides=(2, 2), padding='valid')(img_input)

# 卷积反向传播梯度下降采用Batch Normalization （另一个是mini-batch size）
x = BatchNormalization()(x)

# 激活函数ReLU
x = Activation('relu')(x)

# 池化区域大小为3*3, 池化步伐是2*2
x = MaxPooling2D(pool_size=(3, 3), strides=(2, 2))(x)

# 卷积
x = fire(x, squeeze=16, expand=16)

# 卷积
x = fire(x, squeeze=16, expand=16)

# 池化
x = MaxPooling2D(pool_size=(3, 3), strides=(2, 2))(x)

# 卷积
x = fire(x, squeeze=32, expand=32)
# 卷积
x = fire(x, squeeze=32, expand=32)
# 池化
x = MaxPooling2D(pool_size=(3, 3), strides=(2, 2))(x)


x = fire(x, squeeze=48, expand=48)

x = fire(x, squeeze=48, expand=48)

x = fire(x, squeeze=64, expand=64)

x = fire(x, squeeze=64, expand=64)

# 正则化，dropout是让某些神经元以一定的概率不工作， 防止训练的时候过拟合（过拟合是指为了得到一致假设而使假设变得过度严格。）
# 随机的让一些节点不工作了，因此可以避免某些特征只在固定组合下才生效，有意识地让网络去学习一些普遍的共性
# 随机扔掉20%？
x = Dropout(0.2)(x)

#输出层？
x = Convolution2D(512, (1, 1), padding='same')(x)
out = Activation('relu')(x)

#建立模型，模型的输入，输出
modelsqueeze = Model(img_input, out)

#Prints a string summary of the network
modelsqueeze.summary()

im_in = Input(shape=(200, 200, 4))
#wrong = Input(shape=(200,200,3))

x1 = modelsqueeze(im_in)
#x = Convolution2D(64, (5, 5), padding='valid', strides =(2,2))(x)

#x1 = MaxPooling2D(pool_size=(3, 3), strides=(2, 2))(x1)

"""
x1 = Convolution2D(256, (3,3), padding='valid', activation="relu")(x1)
x1 = Dropout(0.4)(x1)

x1 = MaxPooling2D(pool_size=(3, 3), strides=(1, 1))(x1)

x1 = Convolution2D(256, (3,3), padding='valid', activation="relu")(x1)
x1 = BatchNormalization()(x1)
x1 = Dropout(0.4)(x1)

x1 = Convolution2D(64, (1,1), padding='same', activation="relu")(x1)
x1 = BatchNormalization()(x1)
x1 = Dropout(0.4)(x1)
"""

# Flatten层用来将输入“压平”，即把多维的输入一维化，常用在从卷积层到(Convolution)全连接层(Dense)的过渡。
x1 = Flatten()(x1)

#Dense全连接层
x1 = Dense(512, activation="relu")(x1)
x1 = Dropout(0.2)(x1)
#x1 = BatchNormalization()(x1)
feat_x = Dense(128, activation="linear")(x1)

#经过lambda计算，如果该layer是input layer,则lambda的input是当前layer 的input，否则是previous layer的input
feat_x = Lambda(lambda x: K.l2_normalize(x, axis=1))(feat_x)


model_top = Model(inputs=[im_in], outputs=feat_x)

model_top.summary()

im_in1 = Input(shape=(200, 200, 4))
im_in2 = Input(shape=(200, 200, 4))

feat_x1 = model_top(im_in1)
feat_x2 = model_top(im_in2)

#计算距离？
lambda_merge = Lambda(euclidean_distance)([feat_x1, feat_x2])

#？？
model_final = Model(inputs=[im_in1, im_in2], outputs=lambda_merge)

model_final.summary()

# Adam optimizer: 在实际应用中，Adam方法效果良好。与其他自适应学习率算法相比，其收敛速度更快，
# 学习效果更为有效，而且可以纠正其他优化技术中存在的问题，如学习率消失、收敛过慢或是高方差的参数更新导致损失函数波动较大等问题。
# lr=Learning rate = 学习率
# 学习率决定了参数移动到最优值的速度快慢。
# 如果学习率过大，很可能会越过最优值；
# 而如果学习率过小，优化的效率可能过低，长时间算法无法收敛。
# 所以学习率对于算法性能的表现至关重要。
adam = Adam(lr=0.001)

#Stochastic gradient descent optimizer 随机梯度下降
#学习率
#momentum 动量，冲量，如果只有学习率，
# 可能进入了一个平坦地区，下降好多步，也走不到头
# 进入了一个泥石流区域，向左1步，向右1步，走半天也走不出去
# 动量就是每一步的梯度下降的量和方向，也参考一下上面的步骤，要是方向一致，就大步走；要是忽走忽右，就中和一下，往前走
# momentum越大表示不同向时下降梯度按0.9?。
sgd = SGD(lr=0.001, momentum=0.9)

#初始化学习阶段的配置Configures the model for training，
model_final.compile(optimizer=adam, loss=contrastive_loss)

"""# Learning phase.
We write the generators that will give our model batches of data to train on, then we run the training.
"""
print("Learning phase====================")

def generator(batch_size):
    while 1:
        X = []
        y = []
        switch = True
        for _ in range(batch_size):
           #   switch += 1
            if switch:
               #   print("correct")
                X.append(create_couple_rgbd(
                    "faceid_train/").reshape((2, 200, 200, 4)))
                y.append(np.array([0.]))
            else:
               #   print("wrong")
                X.append(create_wrong_rgbd(
                    "faceid_train/").reshape((2, 200, 200, 4)))
                y.append(np.array([1.]))
            switch = not switch
        X = np.asarray(X)
        y = np.asarray(y)
        XX1 = X[0, :]
        XX2 = X[1, :]
        yield [X[:, 0], X[:, 1]], y


def val_generator(batch_size):

    while 1:
        X = []
        y = []
        switch = True
        for _ in range(batch_size):
            if switch:
                X.append(create_couple_rgbd(
                    "faceid_val/").reshape((2, 200, 200, 4)))
                y.append(np.array([0.]))
            else:
                X.append(create_wrong_rgbd(
                    "faceid_val/").reshape((2, 200, 200, 4)))
                y.append(np.array([1.]))
            switch = not switch
        X = np.asarray(X)
        y = np.asarray(y)
        XX1 = X[0, :]
        XX2 = X[1, :]
        yield [X[:, 0], X[:, 1]], y


gen = generator(16)
val_gen = val_generator(4)

# fit 装载数据进行训练
#  fit_generator 通过generator的方式达到分批出来，节省内存的目的
# outputs = model_final.fit_generator(
#     gen, steps_per_epoch=30, epochs=50, validation_data=val_gen, validation_steps=20)
outputs = model_final.fit_generator(
    gen, steps_per_epoch=30, epochs=1, validation_data=val_gen, validation_steps=20)


"""# Some model tests."""
print("Some model tests====================")

cop = create_couple("faceid_val/")
#Returns the loss value & metrics values for the model in test mode
#用测试数据评估训练结果
model_final.evaluate([cop[0].reshape((1, 200, 200, 4)),
                      cop[1].reshape((1, 200, 200, 4))], np.array([0.]))

cop = create_wrong_rgbd("faceid_val/")
#预测
model_final.predict([cop[0].reshape((1, 200, 200, 4)),
                     cop[1].reshape((1, 200, 200, 4))])

"""# Saving and loading the model.
The next cells show both how to save the model weights and upload them into your Drive, and then how to retrieve those weights from the Drive to load a pre-trained model.
"""

#把训练结果保存到本地HDF5文件
model_final.save("faceid_big_rgbd_2.h5")
print("model_final.save(faceid_big_rgbd_2.h5)====================")

#Dumps all layer weights to a HDF5 file
model_final.save_weights('pesi_weights.h5')

#自己加的，把model保存成json文件，观察下结构
import json
with open('faceid_big_rgbd_2_json.json', 'w') as file:
    file.write(json.dumps(model_final.to_json(), indent=4, sort_keys=False))

# from google.colab import files

# # Install the PyDrive wrapper & import libraries.
# # This only needs to be done once in a notebook.
# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive
# from google.colab import auth
# from oauth2client.client import GoogleCredentials

# # Authenticate and create the PyDrive client.
# # This only needs to be done once in a notebook.
# auth.authenticate_user()
# gauth = GoogleAuth()
# gauth.credentials = GoogleCredentials.get_application_default()
# drive = GoogleDrive(gauth)

# # Create & upload a file.
# uploaded = drive.CreateFile({'title': 'faceid_big_rgbd.h5'})
# uploaded.SetContentFile('faceid_big_rgbd.h5')
# uploaded.Upload()
# print('Uploaded file with ID {}'.format(uploaded.get('id')))

# # Install the PyDrive wrapper & import libraries.
# # This only needs to be done once per notebook.
# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive
# from google.colab import auth
# from oauth2client.client import GoogleCredentials

# # Authenticate and create the PyDrive client.
# # This only needs to be done once per notebook.
# auth.authenticate_user()
# gauth = GoogleAuth()
# gauth.credentials = GoogleCredentials.get_application_default()
# drive = GoogleDrive(gauth)

# # Download a file based on its file ID.
# #
# # A file ID looks like: laggVyWshwcyP6kEI-y_W3P8D26sz
# file_id = '17Lo_ZxYcKO751iYs4XRyIvVXME8Lyc75'
# downloaded = drive.CreateFile({'id': file_id})
# #print('Downloaded content "{}"'.format(downloaded.GetContentString()))

# downloaded.GetContentFile('pesi.h5')

from keras.models import load_model

# model_final.load_weights('pesi_weights.h5')

"""# Raw output.
Here we create a model that outputs the embedding of an input face instead of the distance between two embeddings, so we can map those outputs.
"""

im_in1 = Input(shape=(200, 200, 4))
#im_in2 = Input(shape=(200,200,4))

feat_x1 = model_top(im_in1)
#feat_x2 = model_top(im_in2)


model_output = Model(inputs=im_in1, outputs=feat_x1)

model_output.summary()

adam = Adam(lr=0.001)

sgd = SGD(lr=0.001, momentum=0.9)

model_output.compile(optimizer=adam, loss=contrastive_loss)

cop = create_couple_rgbd("faceid_val/")
model_output.predict(cop[0].reshape((1, 200, 200, 4)))


def create_input_rgbd(file_path):
    #  print(folder)
    mat = np.zeros((480, 640), dtype='float32')
    i = 0
    j = 0
    depth_file = file_path
    with open(depth_file) as file:
        for line in file:
            vals = line.split('\t')
            for val in vals:
                if val == "\n":
                    continue
                if int(val) > 1200 or int(val) == -1:
                    val = 1200
                mat[i][j] = float(int(val))
                j += 1
                j = j % 640

            i += 1
        mat = np.asarray(mat)
    mat_small = mat[140:340, 220:420]
    img = Image.open(depth_file[:-5] + "c.bmp")
    img.thumbnail((640, 480))
    img = np.asarray(img)
    img = img[140:340, 220:420]
    mat_small = (mat_small - np.mean(mat_small)) / np.max(mat_small)
    # plt.figure(figsize=(8, 8))
    # plt.grid(True)
    # plt.xticks([])
    # plt.yticks([])
    # plt.imshow(mat_small)
    # plt.show()
    # plt.figure(figsize=(8, 8))
    # plt.grid(True)
    # plt.xticks([])
    # plt.yticks([])
    # plt.imshow(img)
    # plt.show()

    full1 = np.zeros((200, 200, 4))
    full1[:, :, :3] = img[:, :, :3]
    full1[:, :, 3] = mat_small

    return np.array([full1])


"""# Data visualization.
Here we store the embeddings for all the faces in the dataset. Then, using both **t-SNE** and **PCA**, we visualize the embeddings going from 128 to 2 dimensions.
"""

outputs = []
n = 0
for folder in glob.glob('faceid_train/*'):
    i = 0
    for file in glob.glob(folder + '/*.dat'):
        i += 1
        outputs.append(model_output.predict(
            create_input_rgbd(file).reshape((1, 200, 200, 4))))
    print(i)
    n += 1
    print("Folder ", n, " of ", len(glob.glob('faceid_train/*')))
print(len(outputs))

outputs = np.asarray(outputs)
outputs = outputs.reshape((-1, 128))
outputs.shape

#**t-SNE** and **PCA** 降维
#降维可以用于可视化，提高计算距离的速度

import sklearn
from sklearn.manifold import TSNE

X_embedded = TSNE(2).fit_transform(outputs)
X_embedded.shape

import numpy as np
from sklearn.decomposition import PCA

X_PCA = PCA(3).fit_transform(outputs)
print(X_PCA.shape)

#X_embedded = TSNE(2).fit_transform(X_PCA)
# print(X_embedded.shape)

print("Distance between two arbitrary RGBD pictures.======")

# import matplotlib.pyplot as plt

color = 0
for i in range(len((X_embedded))):
    el = X_embedded[i]
    if i % 51 == 0 and not i == 0:
        color += 1
        color = color % 10
    # plt.scatter(el[0], el[1], color="C" + str(color))

"""# Distance between two arbitrary RGBD pictures."""

file1 = ('faceid_train/(2012-05-16)(154211)/015_1_d.dat')
inp1 = create_input_rgbd(file1)
file1 = ('faceid_train/(2012-05-16)(154211)/011_1_d.dat')
inp2 = create_input_rgbd(file1)

model_final.predict([inp1, inp2])
