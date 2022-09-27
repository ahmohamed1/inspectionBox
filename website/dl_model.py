import tensorflow as tf
from tensorflow.keras.layers import Flatten, Dense, Input
from tensorflow.keras.models import Model
from tensorflow.keras.applications.resnet import ResNet101
from tensorflow.keras.applications.resnet import ResNet152
from tensorflow.keras.applications.resnet import ResNet50
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.vgg19 import VGG19

class Create_model():
    def __init__(self):
        self.batch_size = None
        self.optimizer = None
        self.learning_rate = None
        self.loss_function = None
        self.model_selected = None

    def setup(self, model, optimizer, learning_rate, loss_function, batch_size):
        self.batch_size = batch_size
        self.optimizer = optimizer
        self.learning_rate = learning_rate
        self.loss_function = loss_function
        self.model_selected = model

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
        pass
    def save_model(self, file_name):
        self.model_selected.save(file_name)


