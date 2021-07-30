import requests
import json
from keras.preprocessing.image import img_to_array
import numpy as np
import tensorflow as tf
import vendor.BetterLife as BetterLife

global graph
graph = tf.get_default_graph()

def preprocess_image(image, target_size):
    if image.mode != "RGB":
        image = image.convert("RGB")

    image = image.resize(target_size)
    image = img_to_array(image)
    image = np.expand_dims(image, axis = 0)

    return image



def predict(image, model):
    processed_image = preprocess_image(image, target_size=(224, 224))

    with graph.as_default():
        prediction = model.predict(processed_image).tolist()
    return prediction


def prediction(moleImage, moleId, moleDetailsId, model):
    predicted = predict(moleImage, model)
    url = 'https://betterlife.845.co.il/core/services/pythonServer.php'
    data = {'switch': "Predict", 'Token': BetterLife.API_TOKEN, 'pred': json.dumps(predicted), 'moleId' : moleId, 'moleDetailsId': moleDetailsId}
    x = requests.post(url, data = data)
    #print(x.text)