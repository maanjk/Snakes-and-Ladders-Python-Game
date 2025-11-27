# Snakes & Ladders – Python GUI Game

A desktop Snakes & Ladders game implemented in Python using Tkinter.  
Smooth animations, dice rolling, two-player mode, and a full 100-tile board.

## Table of Contents

- [Features](#features)  
- [Demo / Screenshots](#demo--screenshots)  
- [Requirements](#requirements)  
- [Getting Started / How to Run](#getting-started--how-to-run)  
- [Game Rules](#game-rules)  
  

---

## Features

- ✅ Graphical User Interface using **Tkinter**  
- 🎲 Dice roll functionality with drawn dice faces (1–6)  
- 🚶 Smooth token movement animation  
- 🐍🪜 Automatic snakes and ladders jumps  
- 👥 Two-player turn-based system  
- 🖼️ PNG-based token images + full-board background  
- 🏆 Win detection with popup message  
- 📦 Clean, modular, object-oriented code  

---

## Demo / Screenshots

> <img width="1345" height="1020" alt="image" src="https://github.com/user-attachments/assets/5dc894e5-8795-42bb-ae60-adc3aaf53bdd" />
----------------------------------------------------
## Requirements:

Python 3.8 or higher
Pillow (PIL)
 — used for image loading and resizing

Install dependencies:
   pip install pillow
---------------------------------------------------
## Getting Started / How to Run

Clone the repository:
    git clone https://github.com/maanjk/Snakes-and-Ladders-Python-Game.git
    cd Snakes-and-Ladders-Python-Game

----------------------------------------------------
## Game Rules

+ Each player starts at tile 1
+ Click "Roll Dice" to roll a value between 1 and 6
+ Token moves forward that many tiles (animated)
+ If you land on a ladder base — climb up automatically
+ If you land on a snake head — slide down automatically
+ Move only accepted if the dice roll doesn't exceed 100 (must land exactly on 100 to win)
+ Turns alternate between Player 1 and Player 2
+ First player to reach tile 100 exactly wins
  
```markdown
 
