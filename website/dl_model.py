import tensorflow as tf

class Model():
    def __init__(self, model, optimizer, learning_rate, loss_function, batch_size):
        self.batch_size = batch_size
        self.optimizer = optimizer
        self.learning_rate = learning_rate
        self.loss_function = loss_function

        if model == 'ResNet10':
            from tf.keras.applications.resnet10 import ResNet10 as model
        elif model == 'ResNet18':
            from tf.keras.applications.resnet18 import ResNet18 as model
        elif model == 'ResNet50':
            from tf.keras.applications.resnet50 import ResNet50 as model
        elif model == 'VGG16':
            from tf.keras.applications.vgg16 import VGG16 as model
        elif model == 'VGG19':
            from tf.keras.applications.vgg19 import VGG19 as model

    def build(self):
        pass

