import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import pyautogui as pa
import time
import string
import itertools
import keyboard
from wordfreq import zipf_frequency
from spellchecker import SpellChecker
from letter_detection import get_board_data

# Rank function: prioritize answers more heavily
def score_word(word):
    freq = zipf_frequency(word, "en")
    if word in answers:
        return freq + 5   # bonus weight if it's a possible solution
    return freq

#Function to predict color
def predict_color(ROI):
    colors = {0: "grey", 1: "yellow", 2: "green"}
    RGB = (np.asarray(ROI)[0][0]) #get the RGB Numpy array from the square-containing letter image
    color_pred = co_model.predict(np.array([RGB])) #returns a list containing 3 probabilities for each color
    color_pred = list(list(color_pred.astype(int))[0]) #returns the same list of probabilities but converted to integer values basically 0 or 1
    color_index = color_pred.index(max(color_pred)) #returns the index in the list which has the highest probabiliy(value 1)
    return colors[color_index], RGB #returns the color associated with that color index.

#Fucntion to get data from row
def getRowData(row):
    pos = []
    for i in range(5):
        letter = row*5 + i
        
        #get the current letter
        print(row, i, letter)
        print(f"Wordle_data/Alphabets/ROI_{letter}.png")
        img = cv2.imread(f'Wordle_data/Alphabets/ROI_{letter}.png')
        final_color, RGB = predict_color(img)
        print(final_color, RGB)
        if final_color == "grey":
            pos.append(0)
        elif final_color == "yellow":
            pos.append(1)
        elif final_color == "green":
            pos.append(2)
    print(pos)
    return pos

# checks if the passed word matches parameters of correctWords and wrongOrder
def checkCorrect(passed):
    #passed = bank/guess_list
    #return false is to remove a word from bank

    for key in wrongOrder:
        if key not in passed:
            return False
    
    for i in range(5):
        if passed[i] in wrongLetters and passed[i] not in correctOrder:
            return False
        elif correctOrder[i] != " " and passed[i] != correctOrder[i]:
            return False

        for key, value in wrongOrder.items():
            if passed[i] == key and i in value:
                return False
    return True

# refines the list of possible 5 letter words based on restrictions
def refineOptions():
    filtered = list(filter(checkCorrect, bank))
    return filtered

# gets the state of the previous row and updates requirments
def playRow():
    global bank, row

    get_board_data()
    time.sleep(1)

    # get the current row
    state = getRowData(row)
    
    # check if correct order is complete
    if all(s == 2 for s in state):  # all greens
        print("DONE!!")
        return "".join(correctOrder)

    # increment row
    row += 1
    
    # add correct letters to letter array
    for x in range(len(state)):
        if state[x] == 1:
            if word[x] in wrongOrder:
                wrongOrder[word[x]].append(x)
            else:
                wrongOrder[word[x]] = [x]
        elif state[x] == 2:
            correctOrder[x] = word[x]
        elif state[x] == 0 and word[x] not in correctOrder:
            wrongLetters.add(word[x])
    '''
    for letter in wrongLetters:
        if letter in correctOrder:
            wrongLetters.remove(letter)
    '''

    print(wrongLetters)
    print(wrongOrder)
    print(correctOrder)
    time.sleep(0.1)
    
    # refine the search 
    print("Bank length before refining: ",len(bank))
    bank = refineOptions()
    if len(bank) < 200:
        print(bank)
    print("Bank length after refining: ",len(bank))
    return False

def play_game():
    global word, isSolved
    
    print("Starting!")
    start = time.time()

    # Take the screenshot
    screenshot = pa.screenshot()
    screenshot.save('Wordle_data/screenshot.png')

    # Load the image and convert to grayscale
    image = cv2.imread('Wordle_data/screenshot.png')
    height, width = image.shape[:2]

    # Displaying the height and width
    print("Height = {}, Width = {}".format(height, width))

    pa.click(width/2, height/2)
    print("Press [SPACE] to continue")

    # Wait until user presses space or q
    while True:
        key = keyboard.read_key()

        if key == "space":
            break

    pa.click(width/2, height/2)
    # first word
    word = "sport"  # or pick from bank
    pa.write(word)
    pa.press('enter')
    time.sleep(3)
    print("test")
    isSolved = playRow()
    
    while not(isSolved) and row < 6:
        word = bank[0]
        print("trying word", word)
        pa.write(word)
        pa.press('enter')
        time.sleep(2)
        isSolved = playRow()
    
    print("Found that the word was",isSolved,"after",row,"guesses")
    print(correctOrder)
    print("That took ", (time.time()-start), " seconds")

    pa.moveTo(100,100)
    time.sleep(0.5)

#Load color classifier model
co_model = load_model('Models/color.keras')

with open("Wordle_data/nyt-answers.txt") as f:
    answers = [w.strip() for w in f if len(w.strip()) == 5]

with open("Wordle_data/nyt-guesses.txt") as f:
    allowed = [w.strip() for w in f if len(w.strip()) == 5]

# Combine both into one set of guessable words
all_words = set(answers) | set(allowed)

# Sort the combined list
bank = sorted(all_words, key=score_word, reverse=True)

# known letters in their position
correctOrder = [" "," "," "," "," "]
# know letters in incorrect positions e.g:
# wrongOrder = {"h":[0,1],"l":[4,2],"m":[3]}
# h was correct but in the wrong order at positions 0 and 1
# l was correct but in the wrong order at positions 4 and 2
# m was correct but in the wrong order at position 3
wrongOrder = {}
# incorrect letters
wrongLetters = set()
row = 0

while True:
    print("Press [SPACE] to start a new game, or [Q] to quit.")

    # Wait until user presses space or q
    key = keyboard.read_key()

    if key == "space":
        play_game()
        print("done")
        break
    elif key == "q":
        print("Exiting...")
        break