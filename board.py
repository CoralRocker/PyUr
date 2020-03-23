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
        if ftm > 14:
            return ILLEGAL_MOVE
        if ftm == 14:
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
