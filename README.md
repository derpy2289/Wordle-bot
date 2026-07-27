
## Wordle Bot :p

An automated **Wordle solver** built with **Python**, **OpenCV**, and **TensorFlow** that reads the Wordle board directly from the screen, identifies each letter and tile color, and intelligently determines the next best guess.

This project combines **computer vision**, **machine learning**, and **algorithmic problem solving** to automate the entire Wordle solving process.

---

## How It Works

1. Launch Wordle in your browser.
2. The bot captures a screenshot of the board.
3. OpenCV locates and crops the Wordle grid.
4. Each tile is segmented into individual letters.
5. A TensorFlow model classifies each tile's color.
6. The solver updates its knowledge of:

   * Correct letters
   * Misplaced letters
   * Eliminated letters
7. The algorithm selects the best next guess.
8. PyAutoGUI types the guess into Wordle.
9. The process repeats until the puzzle is solved.

---

## Installation

WIP

---

## Future Improvements

* Improve solver algorithm to reduce average guesses
* Increase letter recognition accuracy
* Better support for dark and light themes
* Automatic browser/window detection
* Faster image processing
* Cleaner code architecture and documentation
* Support for Wordle variants

---

## Demo

<img width="1280" height="720" alt="Video Project 3" src="https://github.com/user-attachments/assets/0f219468-5a34-4594-bc96-675f5a6be562" />

---

## What I Learned

This project taught me how to combine multiple areas of computer science into one application, including:

* Computer vision with OpenCV
* Image segmentation and contour detection
* Machine learning with TensorFlow
* Automation using PyAutoGUI
* Search and constraint-solving algorithms
* Debugging and optimizing Python applications

---

