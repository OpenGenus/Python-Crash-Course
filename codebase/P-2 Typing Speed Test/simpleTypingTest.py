import curses
import time 
import sys
import os



def speed(stdscr):

    text = "The quick brown fox jumps over the lazy dog, is a sentence containing all the letters of the alphabet."

    typed_text = []
    wpm=0
    start_time = time.time()
    
    
    while True:
        seconds_passed = max((time.time() - start_time), 1)
        cpm = int(len(typed_text) / (seconds_passed/60))
        wpm = round((cpm/5), 2)

        stdscr.clear()
        show_speed(stdscr, text, typed_text, cpm, wpm, seconds_passed)
        stdscr.refresh()

        if "".join(typed_text) == text:
            stdscr.nodelay(False)
            break
        
        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:
            break 
        
        if len(typed_text) == len(text):
            break

        if key in ("KEY_BACKSPACE", '\b', '\x7f'):
            if len(typed_text) > 0:
                typed_text.pop()
        elif len(typed_text) < len(text):
            typed_text.append(key)

def show_speed(stdscr, text, typed_text, cpm, wpm, seconds_passed):
    stdscr.addstr(text)
    stdscr.addstr(9, 0, f"Typing Speed in words per minute (wpm): {wpm}")
    stdscr.addstr(8, 0, f"Typing Speed in characters per minute : {cpm}")
    stdscr.addstr(7, 0, f"Seconds elapsed : {round(seconds_passed, 2)} seconds") 

    for i, letter in enumerate(typed_text):
        correct_char = text[i]
        if letter != correct_char:
                text_color = curses.color_pair(2)
        else:
            text_color = curses.color_pair(1)


        stdscr.addstr(0, i, letter, text_color)
    



def main(stdscr):
    curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    
    while True:
        speed(stdscr)
        stdscr.addstr(4, 0, "Finished! Press ESC key to Exit.\nPress any key to continue...")
        key = stdscr.getkey()
        if ord(key) == 27:
            break

curses.wrapper(main)