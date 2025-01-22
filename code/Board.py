# -*- coding: utf-8 -*-
# ref: https://stackoverflow.com/questions/24563513

import matplotlib.pyplot as plt
import string

from collections import defaultdict
from itertools import cycle

#################################

RATIO = 1

def set_ratio(n):
  """ reduces the final diagram: use with care!
      better to use ratio=1 and then resize at the browser """
  global RATIO # HACK: don't like global vars :-/
  RATIO = n

###  

def draw_board(n_rows, n_cols, stones, 
               labels=None, 
               markers=None, 
               coordinates=None, 
               background='ivory', 
               filename='board.svg'):
  """
  Draws a rectangle-shaped board
  
  * n_rows : number of rows
  * n_cols : number of columns
  * stones : dictionary, each color with a list of coordinates
      eg: {'white':[(1,1), (2,1)], 'black':[(4,4)]}
      Uses matplotlib/CSS colors
      cf. matplotlib.org/stable/gallery/color/named_colors.html
  * labels : list of triples where the labels must be shown
      eg: [(3,2,'a'), (3,1,'88'), (3,3,'b')]
  * markers : extra marker symbols from matplotlib
      a marker is (row, column, color, size, type)
      eg: [(4,5,'blue',8,'o')]
      cf. https://matplotlib.org/stable/api/markers_api.html
  * coordinates : 1 for intersections (like Go), 
                  2 for squares (like Chess)
  * backgroud : background color, can be a matplotlib color or a 
                rgb triple, eg (1, 1, .95)
      cf. https://matplotlib.org/stable/gallery/color/named_colors.html        
  * filename : 
      Filename with board in SVG format, default is 'board.svg'
  """
  PIECE_SIZE, LABEL_SIZE, COORD_SIZE = 42/RATIO, 24/RATIO, 12/RATIO
  size = max(n_rows, n_cols)/RATIO
  figsize = (ratio*size, size) if (ratio:=n_cols/n_rows)<1 else (size, size/ratio)
  fig = plt.figure(figsize=figsize)
  fig.patch.set_facecolor(background)

  ax = fig.add_subplot(111)
  ax.set_position([0,0,1,1]) # scale the axis area to fill the whole figure
  ax.set_aspect('equal')     # make both axis the same scale
  ax.set_axis_off()          # get rid of axes and everything
  ax.set_xlim(-.5, n_cols-.5) # scale the plot area 
  ax.set_ylim(-.5, n_rows-.5)
  
  # draw the grid
  for x in range(n_cols):
    ax.plot([x, x], [0, n_rows-1], 'k', linewidth=1/RATIO)
  for y in range(n_rows):
    ax.plot([0, n_cols-1], [y, y], 'k', linewidth=1/RATIO)
  
  # draw stones
  edge_color = {'white':'black', 'black':(.3,.3,.3)}  
  for stone_type in stones:
    for x,y in stones[stone_type]:
      ax.plot(x, y, 'o', markersize=PIECE_SIZE, 
                         markeredgecolor=edge_color.get(stone_type, 'black'), 
                         markerfacecolor=stone_type, 
                         markeredgewidth=2/RATIO)
  
  all_stones = [st for _,stones in stones.items() for st in stones]
 
  # draw labels
  if labels:
    for x,y,s in labels:
      # if label not on a stone, make transparent circle before showing it
      if (x,y) not in all_stones:
        ax.plot(x, y, 'o', markersize=PIECE_SIZE, 
                           markeredgecolor=background, 
                           markerfacecolor=background, 
                           markeredgewidth=2/RATIO)
  
      color = 'white' if (x,y) in stones['black'] else 'black'
      ax.text(x, y, s, size=LABEL_SIZE, color=color, ha='center', va='center')
    
  # draw markers  
  if markers:
    for x,y,color,dot_sz,mk in markers:
      if (x,y) not in all_stones:
        ax.plot(x, y, mk, markersize=dot_sz/RATIO, 
                          markerfacecolor=color, 
                          markeredgecolor=color)
        
  # draw coordinates
  alphabet = string.ascii_uppercase
  if coordinates:
    if coordinates == 1: # stones are in intersections
      for i, x in enumerate(range(n_cols)):
        ax.text(x-.05, -0.5, alphabet[i%26], size=COORD_SIZE)
      for i, y in enumerate(range(n_rows)) :
        ax.text( -0.5, y-0.05, str(i+1), size=COORD_SIZE)

    if coordinates == 2: # stones are inside squares
      for i, x in enumerate(range(n_cols-1)):
        ax.text(x+.45, -.25, alphabet[i%26], size=COORD_SIZE)
      for i, y in enumerate(range(n_rows-1)) :
        ax.text( -0.25, y+0.45, str(i+1), size=COORD_SIZE)
  
  plt.savefig(filename) # save board as svg

#### 

def intersections(grid):
  """ grid is a multi-string with the board information, like

  .  x1 .  o2  .  .
  .  3  .  4  .  .
  .  .  .  .  .  .
  Q  O  #  .  X  .
  
  and returns all information in a format useful to draw_board()
  
  Accepts white pieces (oOQ), black pieces (xX#), and labels
  Other colors must be added by hand   

  Eg:
    n_rows, n_cols, stones, labels, markers, coord = intersections(grid)
    stones['red'].append( (1,4) )
    labels.append( (2,3,'♔') )
    draw_board(n_rows, n_cols, stones, labels, markers, coord)                                       
  """
  lines = [line for line in grid.split('\n') if len(line)>0] # remove empty lines
  n_rows, n_cols = len(lines), len(lines[0].split())
  
  stones, labels, markers = defaultdict(list), [], []
  for r, line in enumerate(lines):
    for c, stone in enumerate(line.split()):
      
      if stone[0] in 'xX#':
        stones['black'].append( (c, n_rows-r-1) )
        if stone[0] == 'X':
          # +0.001 because a marker at a stone's coordinate is not shown
          markers.append( (c+0.001, n_rows-r-1, 'gray', 28/RATIO, 'o') )
        if stone[0] == '#':
          markers.append( (c+0.001, n_rows-r-1, 'white', 12/RATIO, 's') )
        if len(stone) > 1: # this is a labeled stone
          labels.append( (c, n_rows-r-1, stone[1:]) )
          
      elif stone[0] in 'oOQ':
        stones['white'].append( (c, n_rows-r-1) )
        if stone[0] == 'O':
          markers.append( (c+0.001, n_rows-r-1, 'lightgray', 28/RATIO, 'o') )
        if stone[0] == 'Q':
          markers.append( (c+0.001, n_rows-r-1, 'black', 14/RATIO, 's') )
        if len(stone) > 1: # this is a labeled stone
          labels.append( (c, n_rows-r-1, stone[1:]) )
          
      elif stone[0] != '.':
        labels.append( (c, n_rows-r-1, stone) )
        
      elif len(stone)>1:
          labels.append( (c, n_rows-r-1, stone[1:]) )
        
  return n_rows, n_cols, stones, labels, markers, 1


def squares(grid):
  """ receives the same information as intersections(), but returns
      the data to be drawn inside the squares """
  n_rows, n_cols, stones, labels, markers, _ = intersections(grid)
  # shift graphic elements from the intersections to the middle of the squares
  for stone_type in stones:
    stones[stone_type] = [(x+.5, y+.5) for x,y in stones[stone_type]]
  labels  = [(x+.5, y+.5, label)      for x,y,label    in labels]
  markers = [(x+.5, y+.5, cl, sz, mk) for x,y,cl,sz,mk in markers]
  return n_rows+1, n_cols+1, stones, labels, markers, 2


####

def read_game(n_rows, n_cols, moves, labels=True, players='xo'):
  """
     n_rows, 
     n_cols  : size of the board
     moves   : multi-line string with the moves
        moves must be separared with spaces, multi-moves by commas
     labels  : show stone's turn if True, no labels if False
     players : get color of next player
  """
  board = [['.  ']*n_cols for _ in range(n_rows)]
  players = cycle(players)
  
  for i, move in enumerate(moves):
    player = next(players)
    for mv in move.split(','):
      r, c = ord(mv[0])-97, int(mv[1:])-1
      board[c][r] = f"{player + str(i+1)*labels:3}"
  
  return board[::-1]


def board2string(board):
  return '\n'.join([' '.join(row) for row in board])

#################################

class Sq():
  def __init__(self, board, go_like=True, size=False, filename='board.svg'):
    process = intersections if go_like else squares
    if size:
      n_cols, n_rows = size
      board = board2string(read_game(n_cols, n_rows, board.split()))
    draw_board(*process(board), filename=filename)

#################################
############ Tests ############## 
#################################

# if __name__ == "__main__":

#   ko = """
#   . . . . .
#   . . x o .
#   . x o . .
#   . . x o .
#   . . . . .
#   """
  
#   Sq(ko, go_like=False)
  
#   match = """
#   d3 h4 a5
#   d6    c4
#   b5    e4
#   f4    f5
#   c2    h6
#   g6    h5,b1
#   """
  
#   Sq(match, go_like=False, size=(9,6))

#################################

# if __name__ == "__main__":
  
#   match = """
#   d3 h8 a9
#   d6    c4,b1
#   b5    e4
#   f4    f5
#   c2    h7
#   g6    h5
#   h6    e5
#   g5    e6
#   e2    e3
#   e7    d5
#   f7    f3,g3
#   """
  
#   board = read_game(9, 9, match.split())
#   draw_board(*squares(board2string(board)))

####

# if __name__ == "__main__":

#   grid = """
#   .  x88 .  o2  .  .
#   .  2  .  1  .  .
#   .  .  .  .  .  .
#   Q  O  #  .  X  ."""
  
#   draw_board(*intersections(grid))
#   draw_board(*squares(grid))

####

# if __name__ == "__main__":
#   stones = {}  
#   stones['white'] = [(3,2), (1,1)]
#   stones['black'] = [(2,1), (3,1)]
#   stones['cyan'] = [(4.5,4.5)]
  
#   labels = [(3,2,'3'), (3,1,'88'), (3,3,'a')]
#   markers = [(4,5,'blue',8,'o')] # https://matplotlib.org/stable/api/markers_api.html
  
#   draw_board(sz=(8,8), stones=stones, labels=labels, markers=markers)  