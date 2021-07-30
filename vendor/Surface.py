import cv2
import numpy as np
import requests
import vendor.BetterLife as BetterLife
import base64

def imgToBase64(img):
	return base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()


def makeSurface(moleImg, moleName):

	img = cv2.imread(moleImg)
	img = cv2.resize(img, (600, 450))
	imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	d = []
	for row in imgGray:
		tempList = []
		for cell in row:
			pixel = cell
			if(pixel > 150):
				pixel = 255
			else:
				pixel = 100
			tempList.append(pixel)

		d.append(tempList)

	numpyD = np.array(d)

	for row in img:
		for pixel in row:
			pixel[0] += 50

	inxRow = 0
	for row in img:
		for i in range(len(row)):
			if numpyD[inxRow][i] < 160:
				row[i][1] = 255
		inxRow +=1

	numpyD = np.array(d)

	img_64 = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()

	url = 'https://betterlife.845.co.il/core/services/pythonServer.php'
	data = {'switch': "Surface", 'Token': BetterLife.API_TOKEN, 'image': img_64, 'name': moleName}
	x = requests.post(url, data=data)
	#print(x.text)
