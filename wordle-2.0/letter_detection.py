# Importing the OpenCV library
import cv2
import pyautogui as pa
import numpy as np

def get_board_data():

    # Take the screenshot
    screenshot = pa.screenshot()
    screenshot.save('Wordle_data/screenshot.png')

    # Load the image and convert to grayscale
    image = cv2.imread('Wordle_data/screenshot.png')

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # cv2.imshow("Image", gray)
    # cv2.waitKey(0)

    #Sharpen the edges of the image for better contour detection
    sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharpen = cv2.filter2D(gray, -1, sharpen_kernel)

    # cv2.imshow("Image", sharpen)
    # cv2.waitKey(0)

    #Calculate the average brightness of the pixels
    avg_brightness = cv2.mean(gray)[0]

    #Classify based on the threshold
    #Thresholding the image
    if avg_brightness < 50:
        thresh = cv2.threshold(sharpen,80,255, cv2.THRESH_BINARY)[1]
        print("Dark Mode", avg_brightness)
    else:
        thresh = cv2.threshold(sharpen,225,255, cv2.THRESH_BINARY_INV)[1]
        print("Light Mode", avg_brightness)


    # cv2.imshow("Threshold Image", thresh)
    # cv2.waitKey(0)

    cv2.imwrite("Wordle_data/Grayscale.png", gray)
    cv2.imwrite("Wordle_data/Sharpen.png", sharpen)
    cv2.imwrite("Wordle_data/Threshold.png", thresh)

    #Find contours in the image
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    #Variable cnts includes all the contours found in the image

    #The below for loop goes through every contour found and basically crops the image
    #to every letter in a square and saves it
    cnts = cnts[::-1] #reverses the list containing contours
    image_number = 0
    for c in cnts:
        area = cv2.contourArea(c)#finds out area of each contour
        if  2000 < area < 10000: #filters out contours that are too small or too large
            x,y,w,h = cv2.boundingRect(c)#produces coordinated (x, y) and height(h) and width(w) of each square-containing alphabet
            ratio = w/h
            if 0.9 < ratio < 1.1: #filters out contours that are not square-shaped
                ROI = image[y:y+h, x:x+w] #crops the image to the square-containing alphabet
                #print(image_number, cv2.contourArea(c))#finds out area of each contour
                ROI = cv2.resize(ROI, (68, 68))#Resizes the square-containing alphabet to 68x68 pixels
                cv2.imwrite('Alphabets/ROI_{}.png'.format(image_number), ROI) #saves the square-containing alphabet
                cv2.rectangle(image, (x, y), (x + w, y + h), (255,0,0), 2) #produces blue-coloured rectangles on each contour found
                image_number += 1 #counts number of contours and adds by 1 in the for loop
    #print(image_number)
    cv2.imwrite("Wordle_data/Contours.png", image) #saves the blue rectangle-bounded image to display all contours

