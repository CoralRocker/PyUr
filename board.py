import player
import colorful as cf
import curses
from math import floor
from dataclasses import dataclass


'''
Constants
'''
ILLEGAL_MOVE = 1
LEGAL_MOVE = 2
PLAY_AGAIN = 3
WIN_MOVE = 4


'''
Table of valid places on the game board and their appropriate scale values
Magic Numbers FTW.
Modifying this table will break shit.
'''
place_table = (((7,1),(7,5)), ((5,1),(5,5)),
            ((3,1),(3,5)), ((1,1),(1,5)),
            (1,3), (3,3), (5,3), (7,3),
            (9,3), (11,3), (13,3), (15,3),
            ((15,1),(15,5)), ((13,1),(13,5)))


'''
Return a list of text sized correctly for current window
splits text based on line length (splits at end of line, counting border if wanted) and newline characters.
'''
def str2Curses(inStr, bordersize=1, stdscr=False, height=False, width=False):
    height, width = stdscr.getmaxyx() if stdscr != False else height, width
    outBox = []
    inBox = inStr.split('\n')
    for s in inBox:
        count = 0
        tmpStr = ""
        for c in s:
            tmpStr += c
            count  += 1
            if count >= (width - 2*bordersize - 1):
                outBox.append(tmpStr)
                tmpStr = ""
                count = 0
        outBox.append(tmpStr)
    return outBox

'''
Might be temporary, might not. 
Stores all the information necessary for a single chip movement.
'''
@dataclass
class stoneMove:
    pos: int
    owner: chr
    side: int = -1
    pid: int = 1

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
        if ftm > 14:
            return ILLEGAL_MOVE
        if ftm == 14:
            self._players[plyNum].move(chipNum, move)
            self._board[crm][0 if plyNum == 0 or len(self._board[crm]) == 1 else 1] = None
            return WIN_MOVE

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

    def drawBoard(stdscr):
        curses.noecho()
        curses.curs_set(0)
        stdscr.keypad(True)
        stdscr.clear()
        curses.start_color()
        curses.use_default_colors()
        curses.init_color(11, 1000, 0, 0)
        curses.init_color(12, 0, 1000, 0)
        curses.init_pair(1, 11, -1)
        curses.init_pair(2, 12, -1)
    
        moveList = [stoneMove(2, '1', 0, 2), stoneMove(3, '2', 1, 1), stoneMove(13, curses.ACS_CKBOARD, pid=1, side=0)] 
        
        dbf = open("debug", "w")
    
        height, width = stdscr.getmaxyx()
        dbf.write(f"H: {height} W: {width}\n")
    
        xscale = floor((width-1) / 16)
        yscale = floor((height-1) / 6)
        dbf.write(f"XSCL {xscale} YSCL {yscale}\n")
       
        if xscale > 2*yscale:
            xscale = yscale * 2
        else:
            xscale -= 1 if xscale % 2 == 1 else 0
            yscale = int(xscale/2)
        dbf.write(f"POST XSCL {xscale} YSCL {yscale}\n")
    
        cellSize = (2*xscale - 1, 2*yscale - 1)
        
        p = 0
        selected = [0,0]
    
        while True:
            stdscr.erase()
            for y in range(0, (6*yscale) + 1):
                for x in range(0, (16*xscale) + 1):
                    duplet = place_table[selected[p]][p] if type(place_table[selected[p]][p]) is tuple else place_table[selected[p]]
                    if (xscale*(duplet[0]-1)) < x < (xscale*(duplet[0]+1)) and (yscale*(duplet[1]-1)) < y < (yscale*(duplet[1]+1)):
                        stdscr.addch(int((height/2 - (6*yscale)/2) + y), int((width/2 - (16*xscale)/2) + x), ' ', curses.A_REVERSE)
    
                    if y == 0:
                        if x in [0, (12*xscale)]:
                            stdscr.addch(int((height/2 - (6*yscale)/2) + y), int((width/2 - (16*xscale)/2) + x), curses.ACS_ULCORNER)
                        elif x in [(8*xscale), (16*xscale)]:
                            stdscr.addch(int((height/2 - (6*yscale)/2) + y), int((width/2 - (16*xscale)/2) + x), curses.ACS_URCORNER)
                        elif x < (12*xscale) and x > (8*xscale):
                            continue
                        elif x % (2*xscale) == 0:
                            stdscr.addch(int((height/2 - (6*yscale)/2) + y), int((width/2 - (16*xscale)/2) + x), curses.ACS_TTEE)
                        else:
                            stdscr.addch(int((height/2 - (6*yscale)/2) + y), int((width/2 - (16*xscale)/2) + x), curses.ACS_HLINE)
                    elif y == (6*yscale):
                        if x in [0, (12*xscale)]:
                            stdscr.addch(int((height/2 - (6*yscale)/2) + y), int((width/2 - (16*xscale)/2) + x), curses.ACS_LLCORNER)
                        elif x in [(8*xscale), (16*xscale)]:
                            stdscr.addch(int((height/2 - (6*yscale)/2) + y), int((width/2 - (16*xscale)/2) + x), curses.ACS_LRCORNER)
                        elif x < (12*xscale) and x > (8*xscale):
                            continue
                        elif x % (2*xscale) == 0:
                            stdscr.addch(int((height/2 - (6*yscale)/2) + y), int((width/2 - (16*xscale)/2) + x), curses.ACS_BTEE)
                        else:
                            stdscr.addch(int((height/2 - (6*yscale)/2) + y), int((width/2 - (16*xscale)/2) + x), curses.ACS_HLINE)
                    elif y % (2*yscale) != 0:
                        if 0 < y < (2*yscale) or  (4*yscale) < y < (6*yscale):
                            if x < (12*xscale) and x > (8*xscale):
                                continue
                            if x in [xscale, 13*xscale] or (y in [yscale, 5*yscale] and (0 < x < 2*xscale or 12*xscale < x < 14*xscale)):
                                stdscr.addch(int((height/2 - (6*yscale)/2) + y), int((width/2 - (16*xscale)/2) + x), 'X')
                        if (x == (7*xscale) and 2*yscale < y < 4*yscale) or (y == 3*yscale and 6*xscale < x < 8*xscale):
                            stdscr.addch(int((height/2 - (6*yscale)/2) + y), int((width/2 - (16*xscale)/2) + x), 'X')
                        if x % (2*xscale) == 0:
                            stdscr.addch(int((height/2 - (6*yscale)/2) + y), int((width/2 - (16*xscale)/2) + x), curses.ACS_VLINE)
                    elif y in [2*yscale,4*yscale]:
                        if x == 0:
                            stdscr.addch(int((height/2 - (6*yscale)/2) + y), int((width/2 - (16*xscale)/2) + x), curses.ACS_LTEE)
                        elif x == (16*xscale):
                            stdscr.addch(int((height/2 - (6*yscale)/2) + y), int((width/2 - (16*xscale)/2) + x), curses.ACS_RTEE)
                        elif x == (10*xscale):
                            if y == (2*yscale):
                                stdscr.addch(int((height/2 - (6*yscale)/2) + y), int((width/2 - (16*xscale)/2) + x), curses.ACS_TTEE)
                            elif y == (4*yscale):
                                stdscr.addch(int((height/2 - (6*yscale)/2) + y), int((width/2 - (16*xscale)/2) + x), curses.ACS_BTEE)
                        elif x % (2*xscale) == 0:
                            stdscr.addch(int((height/2 - (6*yscale)/2) + y), int((width/2 - (16*xscale)/2) + x), curses.ACS_PLUS)
                        else:
                            stdscr.addch(int((height/2 - (6*yscale)/2) + y), int((width/2 - (16*xscale)/2) + x), curses.ACS_HLINE)
    
            for y in range(0, 6*yscale, yscale):
                for x in range(0, 16*xscale, xscale):
                    #if y in [yscale, 3*yscale, 5*yscale]:
                    for stone in moveList:
                        tmp = []
                        if stone.pos in [0,1,2,3,12,13,14] and stone.side == -1:
                            continue
                        if stone.pos not in [0,1,2,3,12,13,14] and stone.side != -1:
                            stone.side = -1
                        if stone.side != -1:
                            tmp = place_table[stone.pos][stone.side]
                        else:
                            tmp = place_table[stone.pos]
                        if x == tmp[0]*xscale and y == tmp[1]*yscale:
                            if cellSize[0] <= 3 or cellSize[1] <= 3:
                                stdscr.addch(int((height/2 - (6*yscale)/2) + y), int((width/2 - (16*xscale)/2) + x), stone.owner)
                            else:
                                smaller = cellSize[0] if cellSize[0] <= cellSize[1] else cellSize[1]
                                for y2 in range(y-int((smaller-1)/2-1), y+int((smaller-1)/2)):
                                    for x2 in range(x-int((smaller-1)/2-1), x+int((smaller-1)/2)):
                                        if x == x2 and y == y2:
                                            stdscr.addch(int((height/2 - (6*yscale)/2) + y2), int((width/2 - (16*xscale)/2) + x2), curses.ACS_DIAMOND)
                                        else:
                                            stdscr.addch(int((height/2 - (6*yscale)/2) + y2), int((width/2 - (16*xscale)/2) + x2), stone.owner, curses.color_pair(stone.pid))
    
            
    
    
            stdscr.refresh()
            c = stdscr.getch()
            if chr(c) == 'q':
                break
            elif c == curses.KEY_RESIZE:
                height, width = stdscr.getmaxyx()
                dbf.write(f"H: {height} W: {width}\n")
    
                xscale = floor((width-1) / 16)
                yscale = floor((height-1) / 6)
                dbf.write(f"XSCL {xscale} YSCL {yscale}\n")
       
                if xscale > 2*yscale:
                    xscale = yscale * 2
                else:
                    xscale -= 1 if xscale % 2 == 1 else 0
                    yscale = int(xscale/2)
                dbf.write(f"POST XSCL {xscale} YSCL {yscale}\n")
                cellSize = (2*xscale - 1, 2*yscale - 1)
            elif c == curses.KEY_UP:
                selected[p] = selected[p]+1 if selected[p] != 13 else 0
            elif c == curses.KEY_DOWN:
                selected[p] = selected[p]-1 if selected[p] != 0 else 13



    def printBoard(self):
        cf.use_true_colors()
        p1_str = cf.red("#")
        p2_str = cf.blue("#")
        
        print("P1 Chips: ", end='')
        p1_unplayed = list(filter(lambda x: x._pos == -1, self._players[0]._stones))
        tmpstr = ""
        for i in p1_unplayed:
            tmpstr += str(i._id) + " "
        print(cf.red(tmpstr))

        for i in reversed(range(0,4)):
            tmp = 'X'  if i in self._star_pos else ' '
            tmp2 = cf.red(str(self._board[i][0]._id)) if self._board[i][0] != None else None
            print(f"[{tmp2 if self._board[i][0] != None else tmp }]", end='')
        print("      ", end='') # Space

        for i in reversed(range(12,14)):
            tmp = 'X'  if i in self._star_pos else ' '
            tmp2 = cf.red(str(self._board[i][0]._id)) if self._board[i][0] != None else None
            print(f"[{tmp2 if self._board[i][0] != None else tmp }]", end='')
        print("")

        for i in range(4, 12):
            tmp = 'X'  if i in self._star_pos else ' '
            p1_s = cf.red(str(self._board[i][0]._id)) if self._board[i][0] != None else None
            p2_s = cf.blue(str(self._board[i][0]._id)) if self._board[i][0] != None else None
            print(f"[{(p1_s if self._board[i][0]._player == self._players[0] else p2_s) if self._board[i][0] != None  else tmp }]", end='')
        print("")
        
        for i in reversed(range(0,4)):
            tmp = 'X'  if i in self._star_pos else ' '
            tmp2 = cf.blue(str(self._board[i][1]._id)) if self._board[i][1] != None else None
            print(f"[{tmp2 if self._board[i][1] != None else tmp }]", end='')
        print("      ", end='') # Space
        for i in reversed(range(12,14)):
            tmp2 = cf.blue(str(self._board[i][1]._id)) if self._board[i][1] != None else None
            tmp = 'X'  if i in self._star_pos else ' '
            print(f"[{tmp2 if self._board[i][1] != None else tmp }]", end='')
        print("")
        print("P2 Chips: ", end='')
        p2_unplayed = list(filter(lambda x: x._pos == -1, self._players[1]._stones))
        tmpstr = ""
        for i in p2_unplayed:
            tmpstr += str(i._id) + " "
        print(cf.red(tmpstr))

        

