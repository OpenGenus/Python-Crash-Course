import curses
import time 
from pygame import mixer

def speed(stdscr):
    mixer.init() 
    text = "The quick brown fox jumps over the lazy dog, is a sentence containing all the letters of the alphabet."

    typed_text = []
    wpm = 0
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
            keyPress = stdscr.getkey()
        except:
            continue


        if len(typed_text) == len(text):
            break

        if ord(keyPress) == 27:
            break 
        
        if keyPress in ("KEY_BACKSPACE", '\b', '\x7f'):
            if len(typed_text) > 0:
                typed_text.pop()

        elif len(typed_text) < len(text):
            typed_text.append(keyPress)
            
            mixer.music.load('C:\\Users\\sirin\\Desktop\\TypeTest\\sounds\\typeSec.mp3')
            mixer.music.play()

#display speed according to time passed and amount of text typed            
def show_speed(stdscr, text, typed_text, cpm, wpm, seconds_passed):
    stdscr.addstr(text)
    stdscr.addstr(5, 0, f"Typing Speed in words per minute (wpm): {wpm}")
    stdscr.addstr(4, 0, f"Typing Speed in characters per minute : {cpm}")
    stdscr.addstr(6, 0, f"Seconds elapsed : {round(seconds_passed, 2)} seconds") 


    for index, letter in enumerate(typed_text):
        correct_char = text[index]
        if letter != correct_char:
                text_color = curses.color_pair(2)
        else:
            text_color = curses.color_pair(1)


        stdscr.addstr(0, index, letter, text_color)
    



def main(stdscr):

    text = "The quick brown fox jumps over the lazy dog, is a sentence containing all the letters of the alphabet."

    curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    
    while True:
        speed(stdscr)

        #play music
        mixer.init() 
        mixer.music.load('C:\\Users\\sirin\\Desktop\\TypeTest\\sounds\\successMessage.mp3')
        mixer.music.play()

        #color blinking
        for i in range(0,2):
            stdscr.addstr(0, 0, text, curses.color_pair(2))
            stdscr.refresh()
            curses.napms(400)
            stdscr.addstr(0, 0, text, curses.color_pair(4))
            stdscr.refresh()
            curses.napms(400)
            stdscr.addstr(0, 0, text, curses.color_pair(1))
            stdscr.refresh()
            curses.napms(400)


        stdscr.addstr(8, 0, "Yay!! Press any key to continue. \nTo exit press the escape button.")

        
        keyPress = stdscr.getkey()
        
        #break if esc key is pressed
        if ord(keyPress) == 27:
            break

        

    
curses.wrapper(main)