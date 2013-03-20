#!/usr/bin/env python
"""A Starter script for drawing a dragon curve fractal
Intially it just draws dots to the screen
pressing 'q' will quit the program
pressing 's' will slow the program to progress one step at a time
pressing ' ' will all the program to proceed as normal

logging is created for convinence
"""
import curses, logging, time
from random import randrange, choice
logging.basicConfig(
  filename='dragon_debug_{}.log'.format(
    time.strftime("%m-%d_%H:%M:%S", time.localtime())),
  level=logging.DEBUG
)


def main(window):
  # we know that the first argument from curses.wrapper() is stdscr.
  # Initialize it globally for convenience.
  curses.nl()
  curses.noecho()
  
  window.timeout(0)

  columns = curses.COLS - 4 # allow a border
  rows = curses.LINES - 4


  while True:
    
    x = randrange(columns) + 2
    y = randrange(rows) + 2
    window.addch(y, x, ord(choice(['o', 'O', '.'])))
    
    ch = window.getch()
    if ch == ord('q') or ch == ord('Q'):
      return
    elif ch == ord('s'): # for debugging allow us to step through program
      window.nodelay(0)
    elif ch == ord(' '):
      window.nodelay(1)

    curses.napms(50)
  

if __name__ == "__main__":
  curses.wrapper(main)

