from wordfreq import zipf_frequency
from spellchecker import SpellChecker
guess = ""
feedback = ""
guess_list = []

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
guess_list = sorted(all_words, key=score_word, reverse=True)

print("Good starter words are: slice, tried, crane")

for guesses in range(6):
    guess = input("\nword:").lower()
    print("g - green, y - yellow, w - wrong / grey")
    feedback = input("Feedback").lower()
    if feedback == "ggggg":
        print("Well Done! Guess",guesses+1)
        break

    temp_tuple = tuple(guess_list)
    for word in temp_tuple: # You can't iterate over a list you want to change, so using a tuple.
        for i in range(5):
            if feedback[i] == "w" and guess[i] in word and guess.count(guess[i]) == 1: #Thanks for this inprovement
                guess_list.remove(word)
                break
            elif feedback[i] == "g" and guess[i] != word[i]:
                guess_list.remove(word)
                break
            elif feedback[i] == "y" and guess[i] not in word:
                guess_list.remove(word)
                break
            elif feedback[i] == "y" and guess[i] == word[i]:
                guess_list.remove(word)
                break
    print(guess_list)
