import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

from util import get_limits

#Function to predict color
def predict_color(ROI):
    colors = {0: "grey", 1: "yellow", 2: "green"}
    RGB = (np.asarray(ROI)[0][0]) #get the RGB Numpy array from the square-containing letter image
    color_pred = co_model.predict(np.array([RGB])) #returns a list containing 3 probabilities for each color
    color_pred = list(list(color_pred.astype(int))[0]) #returns the same list of probabilities but converted to integer values basically 0 or 1
    color_index = color_pred.index(max(color_pred)) #returns the index in the list which has the highest probabiliy(value 1)
    return colors[color_index] #returns the color associated with that color index.

#Load color classifier model
co_model = load_model('Models/color.h5')



for i in range(5):
    img = cv2.imread(f'Alphabets/ROI_{i}.png')

    cv2.imshow("img", img)
    cv2.waitKey(0)
    final_color, RGB = predict_color(ROI)
    print(final_color, RGB) #print color predicted and the RGB value associated