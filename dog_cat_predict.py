# -*- coding:utf-8 -*-
"""
读取保存好的模型进行预测
"""
from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model
img_width, img_height = 100, 100
model = load_model('dog_cat_model.h5')
batch_size = 20
prediction_data_dir = r'D:\360安全浏览器下载\data\prediction'
prediction_data_gen = ImageDataGenerator(rescale=1. / 255)
prediction_generator = prediction_data_gen.flow_from_directory(
    prediction_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary')


prediction = model.predict_generator(
    generator=prediction_generator,
    workers=1, steps=None,
    max_queue_size=10,
    use_multiprocessing=False, verbose=0
    )

result = prediction > 0.5
print(result.sum()/len(result))

