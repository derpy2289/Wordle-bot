import pyautogui
import time

def findResult(x, y): # difference in y is 70, so is diff in x
    # y, w, w, g (177, 161,
    #

    # 76, 255) (58, 59, 60, 255) (58, 59, 60, 255) (97, 141, 85, 255)
    global count
    y = y + 5
    x = x + 35
    line = 0
    image = pyautogui.screenshot()
    image.save('another_screenshot2.png')
    pixels = []

    for num in range(5):
        pyautogui.moveTo((((x + num * 35) * 2), (y + count * 35) * 2))
        time.sleep(1)
        pixels.append(image.getpixel((((x + num * 35) * 2), (y + count * 35) * 2)))
    '''
    one = image.getpixel((x, y))
    two = image.getpixel((x + 160, y + count * 145))
    three = image.getpixel((x + 320, y + count * 145))
    four = image.getpixel((x + 480, y + count * 145))
    five = image.getpixel((x + 540, y + count * 145))
    '''
    result = ""
    for pixel in pixels:
        print(pixel)
        if pixel[0] < 150:
            result += "g"
        elif pixel[0] < 200:
            result += "w"
        else:
            result += "y"
    return result

def locateAnchorPoint():
    anchorPoint = pyautogui.locateOnScreen("C:/Users/Jacob/Desktop/wordle/Screenshot 2025-08-27 141001.png", confidence=.8)
    return anchorPoint
def typeResponse(word):
    pyautogui.write(word, interval = .01)
    pyautogui.press("enter")

    
loc = locateAnchorPoint()
x = (loc[0]) // 2 
y = (loc[1]) // 2
print(x, y)
while pyautogui.locateOnScreen("C:/Users/Jacob/Desktop/wordle/Screenshot 2025-08-27 141001.png", confidence=.8) == None:
    time.sleep(.1)

pyautogui.moveTo(x*2, y*2)

word = "raise"
typeResponse(word)
time.sleep(1)

count = 0
result = findResult(x,y)
print(result)
