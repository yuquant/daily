# -*- coding:utf-8 -*-
"""
读取保存好的模型反复迭代
"""

from keras.preprocessing.image import ImageDataGenerator
from keras import backend
from keras.models import load_model
import pandas as pd
from matplotlib import pyplot as plt

train_data_dir = r'D:\360安全浏览器下载\data\train5'
validation_data_dir = r'D:\360安全浏览器下载\data\validation'
nb_train_samples = 2000
nb_validation_samples = 800
epochs = 50
batch_size = 20

# dimensions of our images.
img_width, img_height = 100, 100
if backend.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)

model = load_model('dog_cat_continue.h5')

# this is the augmentation configuration we will use for training
train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

# this is the augmentation configuration we will use for testing:
# only rescaling
test_datagen = ImageDataGenerator(rescale=1. / 255)

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary')

validation_generator = test_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary')

hist = model.fit_generator(
    train_generator,
    steps_per_epoch=nb_train_samples // batch_size,  # 取商
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=nb_validation_samples // batch_size)
model.save('dog_cat_continue.h5')
print(train_data_dir)
val_loss_acc = hist.history
df = pd.DataFrame(val_loss_acc)
df.plot()
plt.savefig("acc_loss.jpg")
plt.show()
