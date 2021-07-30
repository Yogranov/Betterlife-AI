import base64
import io
from PIL import Image
import threading
from keras.models import load_model
import requests
from flask import request
from flask import Flask
from flask_cors import CORS
import vendor.Daemon as Daemon
import vendor.BetterLife as BetterLife
import time
app = Flask(__name__)
CORS(app)



def get_model():
    global model
    # model = load_model('models/vgg16_Comp_Test.h5')
    model = load_model('models/vgg19_Comp_Test.h5')
    model._make_predict_function()

    print(" * Model Loaded!")


print(" * Loading keras model...")
get_model()


@app.route("/home", methods=["POST"])
def home():
    return "Hello World"


@app.route("/test", methods=["POST"])
def test():
    print("start test")
    url = 'https://betterlife.845.co.il/core/services/pythonServer.php'
    data = {'switch': "Test", 'Token': BetterLife.API_TOKEN}
    x = requests.post(url, data=data)
    print(x.text)
    print("End test")
    return "200"


@app.route("/saveToDir", methods=["POST"])
def saveToDir():
    print("Saving Image \n")
    t1 = threading.Thread(target=Daemon.predictImages, args=(BetterLife.IMAGE_DIR, model))

    encoded = request.values.get("moleImage")
    imgName = request.values.get("name")
    decoded = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(decoded))
    image.save(BetterLife.IMAGE_DIR + imgName + ".jpg")
    print("Image saved, Daemon start with new thread \n")
    t1.start()

    return "200"

@app.route("/saveDataImg", methods=["POST"])
def saveDataImg():
    print("Saving Data Image \n")

    type = request.values.get("moleType")

    encoded = request.values.get("moleImage")
    encoded = encoded[23:]
    decoded = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(decoded))

    image.save(BetterLife.DATA_IMG + type + '/' + str(int(time.time())) + ".jpg")

    return "200"

