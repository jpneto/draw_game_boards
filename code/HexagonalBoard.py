# -*- coding: utf-8 -*-
# ref: https://stackoverflow.com/questions/46525981
#      https://stackoverflow.com/questions/67563362

import matplotlib.pyplot as plt

from matplotlib.patches import RegularPolygon
from math import sin, radians
from itertools import cycle
from collections import Counter

def draw_hexboard(board, *, 
                  hexcolor='earth', edgecolor=None, 
                  piece_sz=26, label_sz=18,
                  background='ivory', 
                  rotate=False,
                  filename='hexboard.svg'):
  """
  board : List[(int, int, int)]
    Coordinates (x,y,z) of all hexes making the board
    Use hex_coords() as a helper function
  hexcolor : str, optional
    The pallete to color fill the board hexes. 
    There are two available 'earth', 'rgb'. 
    Can also pass a single color, eg, 'white'.
    The default is 'earth'.
  edgecolor : str, optional
    The color to draw the hex edges. The default is None.
  piece_sz : the piece's size (default 26)  
  label_sz : the label's size (default 18)  
  backgroud : background color, can be a matplotlib color or a 
              rgb triple, eg (1, 1, .95)
    cf. https://matplotlib.org/stable/gallery/color/named_colors.html        
  rotate :
    True rotates board 60 degress
  filename : str, optional
    Filename with the board in SVG format. The default is 'hexboard.svg'.
  """
  colors = pattern(board, color_palette=hexcolor) 
  
  hcoord = [c[0] for c in board]
  vcoord = [2 * sin(radians(60)) * (c[1] - c[2]) / 3 for c in board]
  if not rotate:
    for i in range(len(vcoord)):
      hcoord[i], vcoord[i] = vcoord[i], -hcoord[i]
  
  fig, ax = plt.subplots(facecolor=background)
  ax.set_aspect('equal')
  ax.set_axis_off()
  ax.set_xlim(min(hcoord)-.7, max(hcoord)+.7) # scale the plot area 
  ax.set_ylim(min(vcoord)-.7, max(vcoord)+.7)  
  
  stones = [c[3] for c in board]
  for x, y, stone, color in zip(hcoord, vcoord, stones, colors):
    hex = RegularPolygon((x, y), 
                         numVertices=6, 
                         radius=2/3, 
                         orientation=radians(30 if rotate else 120), 
                         facecolor=color, 
                         alpha=1, 
                         edgecolor=edgecolor)
    ax.add_patch(hex)
    
    stone_color = {'x':'black', 'o':'white',  'r':'red',    'l':'blue', 
                   'g':'green', 'p':'purple', 'y':'yellow', 's':'silver'}
    stone_color_edge = {'x':'gray',  'o':'black', 'r':'black', 'l':'black', 
                        'g':'black', 'p':'black', 'y':'black', 's':'black'}
    stone_label = {'x':'white', 'o':'black', 'r':'black', 'l':'white', 
                   'g':'black', 'p':'white', 'y':'black', 's':'black', 
                   '.':'black'}
    
    if stone[0] in stone_color:
      ax.plot(x, y, 'o', markersize=piece_sz, 
                         markerfacecolor=stone_color[stone[0]], 
                         markeredgecolor=stone_color_edge[stone[0]], 
                         markeredgewidth=1)
      if len(stone)>1:
        ax.text(x, y, stone[1:], color=stone_label[stone[0]], 
                ha='center', va='center', size=label_sz)
               
    elif stone[0] == '.':
      ax.text(x, y, stone[1:], color='black', ha='center', va='center', size=label_sz)

  ax.autoscale_view()
  plt.savefig(filename, bbox_inches='tight') # save board as svg

###

def hex_coords(grid, square_like=False):
  """
  The grid is a multi-string with the description of a hex board:
  
     . . . .
    . x . . .
   . . o x . .
  . . . . . . .
   . . o . r .
    . . . . .
     . . . .
  
  The hex coordinates (x,y,z) will be computed like this:
    
            [0,0,1],    [0,1,0],   [0,2,-1],    [0,3,-2],
         [1,-1,1],   [1,0,0],   [1,1,-1],    [1,2,-2],   [1,3,-3],
      [2,-2,1],  [2,-1,0],   [2,0,-1],    [2,1,-2],  [2,2,-3],  [2,3,-4],
  [3,-3,1],   [3,-2,0],   [3,-1,-1],   [3,0,-2],   [3,1,-3], [3,2,-4],
      [4,-3,0], ...
        [5,-3,-1], ... 
        
  The function returns a list with tuples (x, y, z, label)
  
  """
  coords, last_sz, last_y, last_z = [], None, None, None
  lines = [line for line in grid.split('\n') if len(line)>0] # remove empty lines

  if not square_like: 
    # draw typical hex-hex boards
    for i, line in enumerate(lines):
      sz = len(line.split())
      if last_sz is None or last_sz < sz: # 1st row, or the rows continue to grow
        x, y, z = i, -i, 1
      else:                               # bottom half, rows are decreasing
        x, y, z = i, last_y, last_z-1      
      last_sz, last_y, last_z = sz, y, z
      for j, cell in enumerate(line.split(), start=1):
        coords.append( (x, y+j, z-j, cell) )
  else:
    # draw square-like board with hexes
    flag = True
    for i, line in enumerate(lines):
      sz = len(line.split())
      if flag:
        x, y, z = i, -i%2, 1
      else:
        x, y, z = i, -i%2, 1
      flag = not flag
      for j, cell in enumerate(line.split(), start=1):
        coords.append( (x, y+j, z-j, cell) )    
      
  return coords  

###

# helper function (do not export)
def pattern(coords, color_palette='earth'):
  """ provides a color tiling for draw_board """
  sz_rows = Counter([a[0] for a in coords])
  max_sz = sz_rows.most_common(1)[0][0] # biggest row
  
  if color_palette == 'earth':
    palette = [(0.82, 0.54, 0.27), (0.91, 0.68, 0.44), (1, 0.81, 0.62)]
  elif color_palette == 'rgb':
    palette = ['lightsalmon', 'skyblue', 'palegreen'] 
  else:
    palette = [color_palette]
  
  colors = []
  last_x, last_sz, row = None, None, 0
  
  for x,*_ in coords:
    if x != last_x: # process next row
      gen = cycle(palette[row%len(palette):]+palette[:row%len(palette)])
      if last_sz and last_sz > sz_rows[row]:
        for _ in range(sz_rows[max_sz] - sz_rows[row]): 
          next(gen)
      last_sz = sz_rows[row]
      row += 1
      
    colors.append(next(gen))
    last_x = x
  return colors  
  
###

def read_hex_game(size, moves, corner, labels=True, players='xo'):
  """
  size    : the hex-board edge size
  moves   : a list of moves made
  corner  : at which coordinate is the top-left corner
  labels  : show stone's turn if True, no labels if False
  players : get color of next player
  """
  def get_rc(mv):
    """ given a move (like 'a1') return (row, colunm) where to put it """
    c, r = ord(mv[0])-97, int(mv[1:])-1
    r = r - r0
    if r < size: # at the top half board or middle row
      start_c = c0 - r - 1
    else:        # at the bottom half
      start_c = r - size + 1
    c = (c - start_c)//2
    return r, c    
  
  EMPTY = '.  '
  board = [[EMPTY]*i for i in range(size, 2*size)]
  board += [row[:] for row in reversed(board[:-1])]
  players = cycle(players)
  
  c0, r0 = ord(corner[0])-97, int(corner[1:])-1
  for i, move in enumerate(moves):
    player = next(players)
    if ':' in move: # some captures occurred
      adds, dels = move.split(':') 
    else:
      adds, dels = move, '' 
      
    for mv in adds.split(','):
      r, c = get_rc(mv)
      board[r][c] = f"{player + str(i+1)*labels:3}"
    
    if dels:
      for mv in dels.split(','):
        r, c = get_rc(mv)
        board[r][c] = EMPTY # remove captured piece from board
      
  
  # print('\n'.join(' '*((2*size-1)+(i-2*size+2 if (i>=size) else -i)) + ''.join(row) 
  #                 for i,row in enumerate(board)))  # dear Lord!
  return board[::-1]


def board2string(board):
  return '\n'.join([' '.join(row) for row in board])


#################################

class Hex():
  def __init__(self, board, size=False, square_like=False, 
               hexcolor='earth', edgecolor=None, background=None,
               filename='board.svg'):
    draw_hexboard(hex_coords(board, square_like=square_like), 
                  hexcolor=hexcolor, 
                  edgecolor=edgecolor, 
                  background=background,
                  filename=filename)   

#################################

# if __name__ == "__main__":
  
#   hex = """
#      . . . x . . .
#       . o . . . . .
#        . . x . . . .
#         . . . x o . .
#          . . . o . . .
#           . . . . . . .
#            . . . . . . .
#   """
#   Hex(hex, square_like=True, hexcolor='white', edgecolor='cyan', background='white')
  # draw_hexboard(hex_coords(hex, square_like=True), 
  #               hexcolor='white', edgecolor='cyan', background=None)   
  
  
# if __name__ == "__main__":
    
  # board = """
  #     . . . .
  #   . x . . .
  #   . . o x . .
  # . . . . . . .
  #   . . o . x .
  #   . . . . .
  #     . . . .
  # """
  
  # Hex(board)
  
  # match = """
  #   o4       i7,o7  
  #   n6,j8    h8,n8  
  #   i9,p6    k7,q7  
  #   l8,r12   r6,g9  
  #   p4,h10   r4,n10 
  #   q5,r2    m5,f10
  #   p2,s5    o3,t6
  #   m3,s3    n2,u5
  #   t4,h12   l2,k11 
  #   j4,p4    i3,g5  
  #   h4,h6    g3,i5  
  #   f4,j6    f6,l6
  #   e5,c7    d6,d8
  #   i11,r10  s9,j12
  #   t10,g11  u9,o11
  #   p12,o9   q9,n12
  #   v6,v8    l4,u7
  #   k3,w7    j2,k5:o4,i7
  #   m9,m11   
  #   """
  
  # moves = match.split()
  # board = read_hex_game(7, moves, corner='h1', players='ox')
  # draw_hexboard(hex_coords(board2string(board)), piece_sz=14, label_sz=8)
    
####

# if __name__ == "__main__":

#   board = """
#       . . . .♔
#      . x . . .
#     . . . g . .
#    . . . . . . .
#     . . . o . .
#      . . . o o
#       . . . .
#   """
  
#   coords = hex_coords(board)
#   draw_hexboard(coords, hexcolor='rgb', edgecolor=None, rotate=True) 