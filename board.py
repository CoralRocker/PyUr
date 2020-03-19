import player
import colorful as cf
import curses
from math import floor

'''
Constants
'''
ILLEGAL_MOVE = 1
LEGAL_MOVE = 2
PLAY_AGAIN = 3
WIN_MOVE = 4


class Board:
    def __init__(self, player1, player2):
        self._players = (player1, player2)
        self._star_pos = [3, 7, 13] # Where the rosettes are on the board
        self._num_spaces = 14
        self._board = [] # List of lists. Some have only one val while others have 2.
        for space in range(0, self._num_spaces):
            if space < 4:
                self._board.append([None, None])
            elif space > 11:
                self._board.append([None, None])
            else:
                self._board.append([None])
        

    '''
    Returns one of the constants defined above
    '''
    def moveChip(self, plyNum, chipNum, move):
        crm = self._players[plyNum]._stones[chipNum]._pos # Current stone pos
        ftm = crm + move # Future stone pos

        '''
        Check if within board
        '''
        if ftm > self._num_spaces:
            return ILLEGAL_MOVE

        if ftm == self._num_spaces:
            self._board[crm][0 if plyNum == 0 or len(self._board[crm]) == 1 else 1] = None
            return WIN_MOVE
        '''
        Check if intercepts enemy player
        '''
        if len(self._board[ftm]) == 1:
            if self._board[ftm][0] != None:
                if self._board[ftm][0]._player != self._players[plyNum] and ftm not in self._star_pos:
                    self._board[ftm][0]._pos = -1 # Resets enemy chip position
                    self._board[ftm][0] = self._players[plyNum]._stones[chipNum] # Sets player chip to that spot
                    self._board[crm][0 if plyNum == 0 or len(self._board[crm]) == 1 else 1] = None
                    self._players[plyNum].move(chipNum, move) # Moves chip for player
                    return LEGAL_MOVE
                else:
                    return ILLEGAL_MOVE
            else:
                self._players[plyNum].move(chipNum, move)
                self._board[ftm][0] = self._players[plyNum]._stones[chipNum] # Sets player chip to that spot
                self._board[crm][0 if plyNum == 0 or len(self._board[crm]) == 1 else 1] = None
                if ftm in self._star_pos:
                    return PLAY_AGAIN
                else:
                    return LEGAL_MOVE
                    
        elif len(self._board[ftm]) == 2:
            if self._board[ftm][plyNum] != None:
                return ILLEGAL_MOVE
            else:
                self._board[ftm][plyNum] = self._players[plyNum]._stones[chipNum] # Sets player chip to that spot
                self._board[crm][0 if plyNum == 0 or len(self._board[crm]) == 1 else 1] = None
                self._players[plyNum].move(chipNum, move) # Moves chip for player
                if ftm in self._star_pos:
                    return PLAY_AGAIN
                elif ftm == self._num_spaces:
                    return WIN_MOVE
                else:
                    return LEGAL_MOVE

    def printBoard(self):
        cf.use_true_colors()
        p1_str = cf.red("#")
        p2_str = cf.blue("#")
        for i in reversed(range(0,4)):
            tmp = 'X'  if i in self._star_pos else ' '
            print(f"[{p1_str if self._board[i][0] != None else tmp }]", end='')
        print("      ", end='') # Space

        for i in reversed(range(12,14)):
            tmp = 'X'  if i in self._star_pos else ' '
            print(f"[{p1_str if self._board[i][0] != None else tmp }]", end='')
        print("")

        for i in range(4, 12):
            tmp = 'X'  if i in self._star_pos else ' '
            print(f"[{(p1_str if self._board[i][0]._player == self._players[0] else p2_str) if self._board[i][0] != None  else tmp }]", end='')
        print("")
        
        for i in reversed(range(0,4)):
            tmp = 'X'  if i in self._star_pos else ' '
            print(f"[{p2_str if self._board[i][1] != None else tmp }]", end='')
        print("      ", end='') # Space
        for i in reversed(range(12,14)):
            tmp = 'X'  if i in self._star_pos else ' '
            print(f"[{p2_str if self._board[i][1] != None else tmp }]", end='')
        print("")


    def drawBoard(self, stdscr):
        dbf = open("debug", "w")
        height, width = stdscr.getmaxyx()
        dbf.write(f"H: {height} W: {width}\n")

        xscale = floor(width/16 - 1)
        yscale = floor(height/2 - 2)
        dbf.write(f"XSCL {xscale} YSCL {yscale}\n")
        
        if yscale*2 > xscale:
            xscale -= 1 if xscale % 2 == 1 else 0
            yscale = int(xscale/2)
        elif xscale/2 > yscale:
            xscale = int(yscale*2)
        dbf.write(f"POST XSCL {xscale} YSCL {yscale}\n")


        for y in range(0, (6*yscale) + 1):
            for x in range(0, (16*xscale) + 1):
                if y == 0:
                    if x in [0, (12*xscale)]:
                        stdscr.insch(int((height/2 - (6*yscale)/2) + y), int((width/2 - (16*xscale)/2) + x), curses.ACS_ULCORNER)
                    elif x in [(8*xscale), (16*xscale)]:
                        stdscr.insch(int((height/2 - (6*yscale)/2) + y), int((width/2 - (16*xscale)/2) + x), curses.ACS_URCORNER)
                    elif x < (12*xscale) and x > (8*xscale):
                        continue
                    elif x % (2*xscale) == 0:
                        stdscr.insch(int((height/2 - (6*yscale)/2) + y), int((width/2 - (16*xscale)/2) + x), curses.ACS_TTEE)
                    else:
                        stdscr.insch(int((height/2 - (6*yscale)/2) + y), int((width/2 - (16*xscale)/2) + x), curses.ACS_HLINE)
                elif y == (6*yscale):
                    if x in [0, (12*xscale)]:
                        stdscr.insch(int((height/2 - (6*yscale)/2) + y), int((width/2 - (16*xscale)/2) + x), curses.ACS_LLCORNER)
                    elif x in [(8*xscale), (16*xscale)]:
                        stdscr.insch(int((height/2 - (6*yscale)/2) + y), int((width/2 - (16*xscale)/2) + x), curses.ACS_LRCORNER)
                    elif x < (12*xscale) and x > (8*xscale):
                        continue
                    elif x % (2*xscale) == 0:
                        stdscr.insch(int((height/2 - (6*yscale)/2) + y), int((width/2 - (16*xscale)/2) + x), curses.ACS_BTEE)
                    else:
                        stdscr.insch(int((height/2 - (6*yscale)/2) + y), int((width/2 - (16*xscale)/2) + x), curses.ACS_HLINE)
                elif y % (2*yscale) != 0:
                    if (y > 0 and y < (2*yscale)) or (y < (6*yscale) and y > (4*yscale)):
                        if x < (12*xscale) and x > (8*xscale):
                            continue
                    if x % (2*xscale) == 0:
                        stdscr.insch(int((height/2 - (6*yscale)/2) + y), int((width/2 - (16*xscale)/2) + x), curses.ACS_VLINE)
                elif y in [2*yscale,4*yscale]:
                    if x == 0:
                        stdscr.insch(int((height/2 - (6*yscale)/2) + y), int((width/2 - (16*xscale)/2) + x), curses.ACS_LTEE)
                    elif x == (16*xscale):
                        stdscr.insch(int((height/2 - (6*yscale)/2) + y), int((width/2 - (16*xscale)/2) + x), curses.ACS_RTEE)
                    elif x == (10*xscale):
                        if y == (2*yscale):
                            stdscr.insch(int((height/2 - (6*yscale)/2) + y), int((width/2 - (16*xscale)/2) + x), curses.ACS_TTEE)
                        elif y == (4*yscale):
                            stdscr.insch(int((height/2 - (6*yscale)/2) + y), int((width/2 - (16*xscale)/2) + x), curses.ACS_BTEE)
                    elif x % (2*xscale) == 0:
                        stdscr.insch(int((height/2 - (6*yscale)/2) + y), int((width/2 - (16*xscale)/2) + x), curses.ACS_PLUS)
                    else:
                        stdscr.insch(int((height/2 - (6*yscale)/2) + y), int((width/2 - (16*xscale)/2) + x), curses.ACS_HLINE)


        stdscr.refresh()
        c = stdscr.getch()

