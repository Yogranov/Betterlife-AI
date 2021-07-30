from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import pandas as pd
import cv2
import requests
import vendor.BetterLife as BetterLife
import base64
from io import BytesIO


def im_2_b64(image):
    buff = BytesIO()
    image.savefig(buff, format="JPEG")
    img_str = base64.b64encode(buff.getvalue())
    return img_str


def makeFigure(moleImg, moleName):
    img = cv2.imread(moleImg, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (100, 100))
    img = cv2.GaussianBlur(img, (9, 9), 0)

    x=0
    d = {}
    for row in img:
        x += 1
        tempList = []
        for cell in row:
            pixel = 255-cell
            #if(pixel < 100):
            #    pixel = 0
            tempList.append(pixel)

        d['V' + str(x)] = tempList

    data2 = pd.DataFrame(data=d)


    # Transform it to a long format
    df = data2.unstack().reset_index()

    df.columns = ["X", "Y", "Z"]
    # And transform the old column name in something numeric
    df['X'] = pd.Categorical(df['X'])
    df['X'] = df['X'].cat.codes


    # Make the plot
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.view_init(65, 290)
    ax.plot_trisurf(df['Y'], df['X'], df['Z'], cmap=plt.cm.viridis, linewidth=0.2)
    #plt.show()

    img_64 = im_2_b64(plt)


    url = 'https://betterlife.845.co.il/core/services/pythonServer.php'
    data = {'switch': "Figure", 'Token': BetterLife.API_TOKEN, 'image': img_64, 'name': moleName}
    x = requests.post(url, data=data)
    #print(x.text)
