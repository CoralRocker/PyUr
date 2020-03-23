import random

class Player:
    def __init__(self, ID, is_computer=False):
        self._computer = is_computer
        self._pid = ID
        self._num_stones = 7
        self._wins = []
        self._stones = []
        for s in range(0, 7):
            self._stones.append(Stone(s, self))
       
    def __eq__(self, other):
        if type(other) is str:
            return self._pid == other
        elif type(other) is Player:
            return self._pid == other._pid
        return False

    def move(self, stone, move):
        ret = self._stones[stone].move(move)
        if self._stones[stone]._win:
            self._wins.append(self._stones[stone])
            # self._stones[stone] = None

    def hasWon(self):
        return len(self._wins) == 7

    '''
    Roll the equivalent of four d4's. Return sum of 1s and 2s
    '''
    def roll(self):
        s = 0
        for i in range(0, 4):
            s += 1 if random.randint(1, 4) < 3 else 0
        return s

class Stone:
    def __init__(self, ID, player=None):
        self._player = player
        self._id = ID # For recognition by the board
        self._pos = -1 # Negative if not on board
        self._is_safe = False
        self._max_pos = 14 # Num movable tiles on board
        self._win = False

    def move(self, move):
        if self._pos + move <= self._max_pos:
            self._pos += move
            if self._pos == self._max_pos:
                self._win = True
            return 0
        else:
            return -1



