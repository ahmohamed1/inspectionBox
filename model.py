from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.applications.vgg16 import decode_predictions
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# load the model
model = VGG16()


# Create function take the image path
# 1- load image with the required size
# 2- convert image to array
# 3- reshape the image into an array (1,224,224,3)
# 4- preprocess the image convert 0-255 to 0-1
# 5- predict the image
# 6- Separate the output into an arrays and return them

def predict_image(imagePath):
    name = []
    predictions = []
    img = load_img(imagePath, target_size=(224, 224))
    img = img_to_array(img)
    img = img.reshape((1, img.shape[0], img.shape[1], img.shape[2]))
    img = preprocess_input(img)
    yhat = model.predict(img)
    label = decode_predictions(yhat)
    for lab in label[0]:
        name.append(lab[1])
        predictions.append(lab[2] * 100)

    label = label[0][0]

    classification = '%s (%.2f%%)' % (label[1], label[2] * 100)

    return classification, name, predictions