import pyautogui as pa
import time
import string
import itertools
import keyboard
from wordfreq import zipf_frequency
from spellchecker import SpellChecker

'''
spell = SpellChecker()
# comparator function to sort word bank by frequency
def compareFreq(elm):
    return zipf_frequency(elm, 'en')
# All known 5 letter words
#bank = sorted(list(spell.known([''.join(x) for x in itertools.product(string.ascii_lowercase, repeat=5)])), reverse=True, key=compareFreq)
'''
with open("nyt-answers.txt") as f:
    answers = [w.strip() for w in f if len(w.strip()) == 5]

with open("nyt-guesses.txt") as f:
    allowed = [w.strip() for w in f if len(w.strip()) == 5]

# Combine both into one set of guessable words
all_words = set(answers) | set(allowed)

# Rank function: prioritize answers more heavily
def score_word(word):
    freq = zipf_frequency(word, "en")
    if word in answers:
        return freq + 5   # bonus weight if it's a possible solution
    return freq

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
# grey incorrect
#grey = (58,58,60)
#grey = (164, 174, 196)
# yellow wrong place
#yellow = (177,161,69)
#yellow = (243, 194,  55)
# green correct
#green = (93, 139, 82)
#green = (121, 184,  81)
# map each colour to an int


#x = 505; y = 225; width = 55
grey = (120, 124, 126)
yellow = (201, 180,  88)
green = (106, 170, 100)
colmap = [grey, yellow, green]
#width = 65
width = 55
#795 183
#800 150

def locateAnchorPoint():
    #wordle infiite
    #anchorPoint = pa.locateOnScreen("C:/Users/Jacob/Desktop/wordle/Screenshot 2025-08-27 141001.png", confidence=.8)
    #wordle+
    #anchorPoint = pa.locateOnScreen("C:/Users/Jacob/Desktop/wordle/Screenshot 2025-08-28 180814.png", confidence=.8)
    #discord wordle
    anchorPoint = pa.locateOnScreen("C:/Users/Jacob/Desktop/wordle/discord_wordle.png", confidence=.8)
    image = pa.screenshot(region=(int(anchorPoint.left), int(anchorPoint.top), int(anchorPoint.width), int(anchorPoint.height)))
    image.save('boardmap.png')
    return anchorPoint

# get which letters in row are correct, in the wrong place, wrong
def getRowData(x, y):
    # take a screenshot of the board
    x = int(x+65)   
    y = int(y+5) 
    im = pa.screenshot(region=(x,y+(width*row),(width*5), width))
    im.save('another_screenshot.png')
    # array mapping what state the current letter is in 0=wrong 1=wrong place 2=correct
    pos = []
    pa.moveTo(x, y+(width*row))
    for i in range(5):
        pa.moveTo(int(x+(width*i)+20), y+(width*row+0))
        pixel = im.getpixel((int(width*i+20), 0))
        '''
        if pixel[0] < 150: #green
            pos.append(2)
        elif pixel[0] < 200:
            pos.append(0) #grey
        else:
            pos.append(1) #yellow
        '''
        if pixel[0] < 70: #grey
            pos.append(0)
        elif pixel[0] < 150:
            pos.append(2) #green
        else:
            pos.append(1) #yellow
        #pos.append(colmap.index(im.getpixel((int(width*i+20), 10))))
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

    '''
    for key, value in wrongOrder.items():
        if not(key in passed):
            return False
    for i in range(5):
        if passed[i] in wrongLetters:
            return False
        if correctOrder[i] != " ":
            if not(passed[i] == correctOrder[i]):
                return False
        for key, value in wrongOrder.items():
            if (passed[i] == key) and (i in value):
                return False
    return True
    '''


# refines the list of possible 5 letter words based on restrictions
def refineOptions():
    filtered = list(filter(checkCorrect, bank))
    return filtered

# gets the state of the previous row and updates requirments
def playRow(locX, locY):
    global bank, row
    # get the current row
    state = getRowData(locX, locY)
    
    # check if correct order is complete
    if all(s == 2 for s in state):  # all greens
        print("DONE!!")
        return "".join(correctOrder)

    # increment row
    row = row+1
    
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

def reset_game():
    ongOrder, wrongLetters, row, bank
    correctOrder = [" "] * 5
    wrongOrder = {}
    wrongLetters = set()
    row = 0
    bank = sorted(all_words, key=score_word, reverse=True)

loc = None
def play_game():
    global word, isSolved, start, loc
    
    print("Starting!")
    start = time.time()

    if loc is None:
        loc = locateAnchorPoint()
        
    x = int(loc[0])
    y = int(loc[1])
    pa.click(x, y)
    print(x, y)
    print(width)
    print("Press [SPACE] to continue")

    # Wait until user presses space or q
    while True:
        key = keyboard.read_key()

        if key == "space":
            break

    pa.click(x, y)
    # first word
    word = "salet"  # or pick from bank
    pa.write(word)
    pa.press('enter')
    time.sleep(3)
    isSolved = playRow(x, y)
    
    while not(isSolved) and row < 6:
        word = bank[0]
        pa.write(word)
        pa.press('enter')
        time.sleep(2)
        isSolved = playRow(x, y)
    
    print("Found that the word was",isSolved,"after",row,"guesses")
    print(correctOrder)
    print("That took ", (time.time()-start), " seconds")

    pa.moveTo(100,100)
    time.sleep(0.5)
    '''
    location = None
    #location = pa.locateOnScreen("C:/Users/Jacob/Desktop/wordle/Screenshot 2025-08-27 155226.png", confidence=.8)
    if location != None:
        pa.press('enter')
        time.sleep(0.1)
        reset_game()
        return True
    return False
    '''

while True:
    print("Press [SPACE] to start a new game, or [Q] to quit.")

    # Wait until user presses space or q
    key = keyboard.read_key()

    if key == "space":
        play_game()
    elif key == "q":
        print("Exiting...")
        break


