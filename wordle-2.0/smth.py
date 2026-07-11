# Importing the OpenCV library
import cv2
import pyautogui as py
import numpy as np

# Take the screenshot
screenshot = py.screenshot()

screenshot.save('screenshot.png')

# Load the image and convert to grayscale
image = cv2.imread('screenshot.png')
h, w = image.shape[:2]
# Displaying the height and width
print("Height = {}, Width = {}".format(h, w))

image = image[100 : 600, 700 : 1200]
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

cv2.imshow("Grayscale Image", gray)
cv2.waitKey(0)

#Sharpen the edges of the image for better contour detection
sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
sharpen = cv2.filter2D(gray, -1, sharpen_kernel)

#Thresholding the image
thresh = cv2.threshold(sharpen,225,255, cv2.THRESH_BINARY_INV)[1]

cv2.imshow("Threshold Image", thresh)
cv2.waitKey(0)

#FInd contours in the image
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
#Variable cnts includes all the contours found in the image

#The below for loop goes through every contour found and basically crops the image
#to every letter in a square and saves it
cnts = cnts[::-1] #reverses the list containing contours
image_number = 0
for c in cnts:
    area = cv2.contourArea(c)#finds out area of each contour
    if area > 800:
        x,y,w,h = cv2.boundingRect(c)#produces coordinated (x, y) and height(h) and width(w) of each square-containing alphabet
        ROI = image[y:y+h, x:x+w] #crops the image to the square-containing alphabet
        ROI = cv2.resize(ROI, (68, 68))#Resizes the square-containing alphabet to 68x68 pixels
        cv2.imwrite('Alphabets/ROI_{}.png'.format(image_number), ROI) #saves the square-containing alphabet
        cv2.rectangle(image, (x, y), (x + w, y + h), (255,0,0), 2) #produces blue-coloured rectangles on each contour found
        image_number += 1 #counts number of contours and adds by 1 in the for loop
print(image_number)
cv2.imwrite("Contours detected in Image", image) #displays the blue rectangle-bounded image to display all contours


# # Reading the image using imread() function
# image = cv2.imread(r'C:\Users\Jacob\Documents\GITHUB-projects\Wordle-bot\wordle-2.0\geeks14.png')
# image = cv2.imread(r'C:\Users\Jacob\Documents\GITHUB-projects\Wordle-bot\wordle-2.0\road.jpg')
# # Extracting the height and width of an image
# h, w = image.shape[:2]
# # Displaying the height and width
# print("Height = {}, Width = {}".format(h, w))

# # Extracting RGB values.
# # Here we have randomly chosen a pixel
# # by passing in 100, 100 for height and width.
# (B, G, R) = image[100, 100]

# # Displaying the pixel values
# print("R = {}, G = {}, B = {}".format(R, G, B))

# # We can also pass the channel to extract
# # the value for a specific channel
# B = image[100, 100, 0]
# print("B = {}".format(B))

# # Filename
# filename = 'savedImage.jpg'

# # Using cv2.imwrite() method
# # Saving the image
# cv2.imwrite(filename, image)

# # Reading and showing the saved image
# image = cv2.imread(filename)
# cv2.imshow("GeeksforGeeks", image)

# cv2.waitKey(0)
# cv2.destroyAllWindows()

# # We will calculate the region of interest
# # by slicing the pixels of the image
# roi = image[100 : 500, 200 : 700]
# cv2.imshow("ROI", roi)
# cv2.waitKey(0)

# # resize() function takes 2 parameters,
# # the image and the dimensions
# resize = cv2.resize(image, (500, 500))
# cv2.imshow("Resized Image", resize)
# cv2.waitKey(0)

# # Calculating the ratio
# ratio = 800 / w

# # Creating a tuple containing width and height
# dim = (800, int(h * ratio))

# # Resizing the image
# resize_aspect = cv2.resize(image, dim)
# cv2.imshow("Resized Image", resize_aspect)
# cv2.waitKey(0)

# # We are copying the original image,
# # as it is an in-place operation.
# output = image.copy()

# # Using the rectangle() function to create a rectangle.
# rectangle = cv2.rectangle(output, (1500, 900),
#                         (600, 400), (255, 0, 0), 2)

# cv2.imshow("Rectangle", rectangle)
# cv2.waitKey(0)

# # Copying the original image
# output = image.copy()

# # Adding the text using putText() function
# text = cv2.putText(output, 'OpenCV Demo', (500, 550),
#                 cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 0, 0), 2)

# cv2.imshow("Text", text)
# cv2.waitKey(0)