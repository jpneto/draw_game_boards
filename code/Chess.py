# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 09:50:12 2025

@author: jpn3t
"""
# ref: https://python-chess.readthedocs.io/en/latest/index.html

# pip install python-chess

import chess
import chess.svg

board = chess.Board("r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4")

print(board)

chess.svg.board(board)  # use Save As SVG at picture's pop-up menu 