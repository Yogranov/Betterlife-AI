import glob
from PIL import Image
import vendor.BetterLife as BetterLife
import vendor.Figure as Figure
import vendor.Surface as Surface
import vendor.Prediction as Prediction
import threading
import os



def predictImages(filePath, model):
    while BetterLife.door is False:
        pass

    try:
        BetterLife.door = False
        
        print("Loading images...\n")
        imageList = []
        for file in glob.glob(filePath + '*.jpg'):
            im = Image.open(file)
            imageList.append([im, file])


        print("Start working on images..\n")
        for image in imageList:
            fileFullName = image[1]
            filename = image[1].split('\\')[1]
            filename = filename[0:-4]

            moleId = filename.split('_')[0]
            moleDetailsId = filename.split('_')[1]

            t1 = threading.Thread(target=Prediction.prediction, args=(image[0], moleId, moleDetailsId, model))
            t2 = threading.Thread(target=Figure.makeFigure, args=(fileFullName, filename))
            t3 = threading.Thread(target=Surface.makeSurface, args=(fileFullName, filename))

            t1.start()
            t2.start()
            t3.start()

            t1.join()
            t2.join()
            t3.join()

            os.remove(fileFullName)

            print("All threads have been completed!")

    finally:
        BetterLife.door = True

    BetterLife.door = True



