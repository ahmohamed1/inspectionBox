import tensorflow as tf
from tensorflow.keras.layers import Flatten, Dense, Input
from tensorflow.keras.models import Model
from tensorflow.keras.applications.resnet import ResNet101
from tensorflow.keras.applications.resnet import ResNet152
from tensorflow.keras.applications.resnet import ResNet50
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.vgg19 import VGG19

class Create_model():
    def __init__(self, model, optimizer, learning_rate, loss_function, batch_size):
        self.batch_size = batch_size
        self.optimizer = optimizer
        self.learning_rate = learning_rate
        self.loss_function = loss_function
        self.model_selected = model

    def build(self, output_size):
        input_shape = [255,255,3]
        if self.model_selected == 'ResNet101':
            model = ResNet101(input_shape=input_shape, weights='imagenet', include_top=False)
        elif self.model_selected == 'ResNet152':
            model = ResNet152(input_shape=input_shape, weights='imagenet', include_top=False)
        elif self.model_selected == 'ResNet50':
            model = ResNet50(input_shape=input_shape, weights='imagenet', include_top=False)
        elif self.model_selected == 'VGG16':
            model = VGG16(input_shape=input_shape, weights='imagenet', include_top=False)
        elif self.model_selected == 'VGG19':
            model = VGG19(input_shape=input_shape, weights='imagenet', include_top=False)
        else:
            print("[ERROR] No model selected")

        x = Flatten()(model.output)
        output_layer = Dense(output_size, activation='softmax')(x)
        model = Model(inputs=model.input, outputs=output_layer)
        model.summary()



