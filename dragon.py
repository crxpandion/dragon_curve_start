#!/usr/bin/env python
"""A Starter script for drawing a dragon curve fractal
pressing 'q' will quit the program
pressing 's' will enter debug mode, press s to execute a single step in this mode
pressing ' ' will all the program to proceed as normal

For more info see http://mathworld.wolfram.com/DragonCurve.html

For our purposes we will approach the dragon curve in two steps:
1) creating the encoding of a dragon curve
2) translating the encoding into characters to draw to the screen
Most of part 2 is already done for you.

To correctly draw a dragon curve you will need to implement
  create_pattern
  get_new_direction
  Point.next_point
"""
import curses, logging, time, sys
from collections import namedtuple
from random import randrange, choice

#
# if you need to do further debugging uncomment these lines
#   then you can log by calling logging.debug("message")
#   see http://docs.python.org/2/library/logging.html
#
#logging.basicConfig(
#  filename='dragon_debug_{}.log'.format(
#    time.strftime("%m-%d_%H:%M:%S", time.localtime())),
#  level=logging.DEBUG
#)

def enum(**enums):
  return type('Enum', (), enums)

class OutOfBoundsError(ValueError):
  pass

Directions = enum(EAST=0, NORTH=1, WEST=2, SOUTH=3)
Turns = enum(LEFT="0", RIGHT="1")

class Point(namedtuple("Point", "row column char")):
  """Simple namedtuple class to make points more explicit"""
  __slots__ = ()
  
  def next_point(self, direction, current_direction):
    """Produces a new point based off of the current direction
    and new direction. This determines how the encoding of the curve will be rendered. 
    
    TODO Implement logic to dictate how the characters "_" and "|" will be drawn to the screen.
    There should be four cases as the curve always makes a 90 degree turn.
    
    Optimize for chars \in ("|", "_")
    """
    if current_direction in (Directions.EAST, Directions.WEST):
      return Point(self.row, self.column - (current_direction - 1), "_")
    elif current_direction in (Directions.NORTH, Directions.SOUTH):
      return Point(self.row - (current_direction - 2), self.column, "|")
    raise ValueError("current direction must be an instance of Direction")
      
  def draw_to_window(self, window):
    """Draws this Point to the curses window"""
    if self.row < 1 or self.row > curses.LINES - 1:
      raise OutOfBoundsError("Went Out of Bounds!")
    if self.column < 1 or self.column > curses.COLS - 1:
      raise OutOfBoundsError("Went Out of Bounds!")
    window.addch(self.row, self.column, self.char)

  def __str__(self):
    return "Point {} at {}, {}".format(self.char, self.row, self.column)

def create_pattern():
  """TODO extend to generate the pattern dynamically
  """
  return "1101100111001001110110001100100"

def get_new_direction(old_direction, turn):
  """TODO Fix to correctly determine direction
  Currently this just rotates around-and-around
  """
  return old_direction

def draw_line(window, point, direction, current_direction):
  new_point = point.next_point(direction, current_direction)
  new_point.draw_to_window(window)
  return new_point 

def reset_window(window):
  columns = curses.COLS - 4 # allow a border
  rows = curses.LINES - 4
  window.clear()
  curses.flash()
  current_direction = choice((Directions.SOUTH, Directions.WEST, Directions.NORTH, Directions.EAST))
  starting_char = "|" if current_direction in (Directions.NORTH, Directions.SOUTH) else "_"
  cur_point = Point(randrange(1, rows), randrange(1, columns), starting_char)
  cur_point.draw_to_window(window)
  return current_direction, cur_point

def main(window, pattern):
  curses.nl()
  curses.noecho()
  
  window.timeout(0)

  current_direction, cur_point = reset_window(window) 
 
  index = 0

  while True:
    if index == len(pattern):
      index = 0
    direction = get_new_direction(current_direction, pattern[index])
    try:
      cur_point = draw_line(window, cur_point, direction, current_direction) 
      current_direction = direction
      index += 1
    except OutOfBoundsError:
      current_direction, cur_point = reset_window(window)

    ch = window.getch()
    if ch == ord('q') or ch == ord('Q'):
      return
    elif ch == ord('s'): # for debugging allow us to step through program
      window.nodelay(0)
    elif ch == ord(' '):
      window.nodelay(1)
    
    curses.napms(100)

if __name__ == "__main__":
  # Create a pattern of at least 4095 chars.  
  pattern = create_pattern()  

  # pass pattern to main
  curses.wrapper(main, pattern)

