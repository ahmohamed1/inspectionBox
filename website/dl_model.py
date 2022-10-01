from tensorflow.keras.layers import Flatten, Dense, Input
from tensorflow.keras.models import Model
from tensorflow.keras.applications.resnet import ResNet101
from tensorflow.keras.applications.resnet import ResNet152
from tensorflow.keras.applications.resnet import ResNet50
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.vgg19 import VGG19

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.data import AUTOTUNE
from imutils import paths
import os
import numpy as np
from glob import glob


class Create_model():
    def __init__(self):
        self.batch_size = None
        self.optimizer = None
        self.learning_rate = None
        self.loss_function = None
        self.model_selected = None
        self.image_size = (255, 255)
        self.epochs = 20

    def setup(self, model, optimizer, learning_rate, loss_function, batch_size, dataset_path):
        self.batch_size = batch_size
        self.optimizer = optimizer
        self.learning_rate = learning_rate
        self.loss_function = loss_function
        self.model_selected = model
        # self.image_paths = list(paths.list_images(dataset_path))
        # self.class_names = np.array(sorted(os.listdir(dataset_path)))
        image_path_list = glob(dataset_path)
        self.data = tf.data.Dataset.list_files(image_path_list)
        print(self.data)


    def build(self, output_size):
        input_shape = [255,255,3]
        if self.model_selected == 'ResNet101':
            self.model = ResNet101(input_shape=input_shape, weights='imagenet', include_top=False)
        elif self.model_selected == 'ResNet152':
            self.model = ResNet152(input_shape=input_shape, weights='imagenet', include_top=False)
        elif self.model_selected == 'ResNet50':
            self.model = ResNet50(input_shape=input_shape, weights='imagenet', include_top=False)
        elif self.model_selected == 'VGG16':
            self.model = VGG16(input_shape=input_shape, weights='imagenet', include_top=False)
        elif self.model_selected == 'VGG19':
            self.model = VGG19(input_shape=input_shape, weights='imagenet', include_top=False)
        else:
            print("[ERROR] No model selected")

        x = Flatten()(self.model.output)
        output_layer = Dense(output_size, activation='softmax')(x)
        self.model = Model(inputs=self.model.input, outputs=output_layer)
        self.model.summary()
        self.model.compile(optimizer=self.optimizer,
                           loss=self.loss_function,
                           metrics=[tf.keras.metrics.SparseCategoricalAccuracy()])

    def train(self):
        training_data = tf.data.Dataset.from_tensor_slices(self.data)
        training_data = (training_data
                   .shuffle(1024)
                   .map(self.load_images, num_parallel_calls=AUTOTUNE)
                   .cache()
                   .repeat()
                   .batch(self.batch_size)
                   .prefetch(AUTOTUNE)
                   )

        self.model.fit(x=training_data,
                        batch_size=self.batch_size,
                        epochs=self.epochs,
                        verbose='auto',
                        callbacks=None,
                        validation_split=0.0)
    def save_model(self, file_name):
        self.model_selected.save(file_name)

    def load_images(self, imagePath):
        # read the image from disk, decode it, resize it, and scale the
        # pixels intensities to the range [0, 1]
        image = tf.io.read_file(imagePath)
        image = tf.image.decode_png(image, channels=3)
        image = tf.image.resize(image, self.image_size) / 255.0
        # grab the label and encode it
        label = tf.strings.split(imagePath, os.path.sep)[-2]
        oneHot = label == self.class_mames
        encodedLabel = tf.argmax(oneHot)
        # return the image and the integer encoded label
        return (image, encodedLabel)

    @tf.function
    def augment(self, image, label):
        # perform random horizontal and vertical flips
        image = tf.image.random_flip_up_down(image)
        image = tf.image.random_flip_left_right(image)
        # return the image and the label
        return (image, label)