"""
Database: http://yann.lecun.com/exdb/mnist/
Keras 提供自度下載的 Function: https://keras.io/api/datasets/
Reference:
* http://speech.ee.ntu.edu.tw/~tlkagk/courses_ML20.html
* https://keras.io/zh/getting-started/sequential-model-guide/
"""
import os
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D
from keras.utils import np_utils, plot_model
from keras.datasets import mnist
import matplotlib.pyplot as plt
import pandas as pd


# Mnist Dataset
(X_train, Y_train), (X_test, Y_test) = mnist.load_data()
x_train = X_train.reshape(60000, 1, 28, 28)/255
x_test = X_test.reshape(10000, 1, 28, 28)/255
y_train = np_utils.to_categorical(Y_train)
y_test = np_utils.to_categorical(Y_test)

# Model Structure
"""
這裡是我們建立模型的部份，可以看到我們先是建立了 Convolution 層，
然後接 MaxPool 層簡化圖片像素，然後 Flattern 攤平維度，最後接 Dense 全連接層，
然後就輸出那 10 個類別了
"""
model = Sequential()
model.add(Conv2D(filters=32, kernel_size=3, input_shape=(1, 28, 28), activation='relu', padding='same'))
model.add(MaxPool2D(pool_size=2, data_format='channels_first'))
model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dense(10, activation='softmax'))
print(model.summary())

# Train
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(x_train, y_train, epochs=10, batch_size=64, verbose=1)

# Test
loss, accuracy = model.evaluate(x_test, y_test)
print('Test:')
print('Loss: %s\nAccuracy: %s' % (loss, accuracy))

# Save model
model.save('./CNN_Mnist.h5')

# Load Model
model = load_model('./CNN_Mnist.h5')

# Display
def plot_img(n):
    plt.imshow(X_test[n], cmap='gray')
    plt.show()


def all_img_predict(model):
    print(model.summary())
    loss, accuracy = model.evaluate(x_test, y_test)
    print('Loss:', loss)
    print('Accuracy:', accuracy)
    predict = model.predict_classes(x_test)
    print(pd.crosstab(Y_test.reshape(-1), predict, rownames=['Label'], colnames=['predict']))


def one_img_predict(model, n):
    predict = model.predict_classes(x_test)
    print('Prediction:', predict[n])
    print('Answer:', Y_test[n])
    plot_img(n)
