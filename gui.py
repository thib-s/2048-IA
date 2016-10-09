#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# imports ###################################################################

from tkinter import *
from collections import defaultdict
import time

import logic
import strategy


# constants #################################################################

# time in miliseconds between iterations
WAIT_DURATION = 6

# colors from http://gabrielecirulli.github.io/2048/style/main.css
COLORS = defaultdict(
  lambda: ("#3c3a32", "#f9f6f2"), {
       0: ("#ccc0b4", "#776e65"),
       2: ("#eee4da", "#776e65"),
       4: ("#ede0c8", "#776e65"),
       8: ("#f2b179", "#f9f6f2"),
      16: ("#f59563", "#f9f6f2"),
      32: ("#f67c5f", "#f9f6f2"),
      64: ("#f65e3b", "#f9f6f2"),
     128: ("#edcf72", "#f9f6f2"),
     256: ("#edcc61", "#f9f6f2"),
     512: ("#edc850", "#f9f6f2"),
    1024: ("#edc53f", "#f9f6f2"),
    2048: ("#edc22e", "#f9f6f2"),
})

FONT = "Helvetica 55 bold"

def get_font(v):
    if v < 100:
        return FONT
    elif v < 1000:
        return "Helvetica 44 bold"
    else:
        return "Helvetica 32 bold"


# graphical user interface ##################################################

# building the window

BACKGROUND_COLOR = "#bbada0"
window = tkinter.Tk()
window.configure(bg=BACKGROUND_COLOR, border=7)
window.wm_title("2048")
window.resizable(0, 0)
score = 0
scorestr =  StringVar()
scorestr.set("score:"+str(score))
score_label = tkinter.Label(window, textvariable = scorestr)
score_label.grid(row=logic.SIZE+1)


def frame(i, j):
    frame = tkinter.Frame(window, width=107, height=107)
    frame.grid(row=i, column=j, padx=7, pady=7)
    return frame

def label(i, j):
    label = tkinter.Label(frames[i][j], font=FONT)
    label.place(anchor="c", relx=.5, rely=.52)
    return label

frames = [[frame(i, j) for j in range(logic.SIZE)] for i in range(logic.SIZE)]
labels = [[label(i, j) for j in range(logic.SIZE)] for i in range(logic.SIZE)]


# updating the board

def update():
    for i in range(logic.SIZE):
        for j in range(logic.SIZE):
            v = logic.value(board, i, j)
            bg, fg = COLORS[v]
            labels[i][j].configure(bg=bg, fg=fg,
                                   text=str(v) if v else "",
                                   font=get_font(v))
            frames[i][j].configure(bg=bg)
            scorestr.set("score:"+str(score))

# handling events

state = 'new_tile'
resume_state = ''
board = logic.empty_board()

def key_press(event):
    global state, resume_state, score
    if event.keysym == 'q':
        window.destroy()
        return
    if event.keysym == 'r':
        if state == 'gameover':
            score = 0
            state = 'new_tile'
            for i in range(len(board)):
                board[i] = logic.zeros(logic.SIZE)
            window.configure(bg=BACKGROUND_COLOR)
    elif event.keysym == 'space' and state != 'gameover':
        update()
        if state == 'pause':
            window.configure(bg=BACKGROUND_COLOR)
            state = resume_state
        else:
            resume_state = state
            window.configure(bg="#FFFFFF")
            state = 'pause'
    next_state_loop(event.keysym)

def next_state_loop(key):
    if state == 'gameover' or state == 'pause':
        return
    next_state(key)
    update()
    wait_key = None
    if state == 'new_tile':
        wait_key = strategy.new_tile_requires_keyboard()
    elif state == 'direction':
        wait_key = strategy.direction_requires_keyboard()
    if wait_key:
        return
    window.after(WAIT_DURATION, next_state_loop, '')

# Return True if the game should continue without waiting
def next_state(key):
    global state
    if state == 'direction':
        if play_direction(key):
            state = 'new_tile'
    elif state == 'new_tile':
        if play_new_tile(key):
            state = 'direction'
        if logic.game_over(board):
            window.configure(bg="#880000")
            state = 'gameover'
    else:
        raise AssertionError('Invalid state ' + state)

def play_direction(key):
    global score
    direction = strategy.choose_direction(key, board, score)
    if direction is None:
        return False
    (moved, score_increment) = logic.slide(direction, board)
    score += score_increment
    if not moved:
        return False
    return True

def play_new_tile(key):
    new_tile_move = strategy.choose_new_tile(key, board)
    if new_tile_move is None:
        return False
    logic.computer_move(new_tile_move, board)
    return True

window.bind("<KeyPress>", key_press)
next_state_loop('')

tkinter.mainloop()
