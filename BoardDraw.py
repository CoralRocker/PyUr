import curses
from dataclasses import dataclass
from math import floor
import player

place_table = (((7,1),(7,5)), ((5,1),(5,5)),
            ((3,1),(3,5)), ((1,1),(1,5)),
            (1,3), (3,3), (5,3), (7,3),
            (9,3), (11,3), (13,3), (15,3),
            ((15,1),(15,5)), ((13,1),(13,5)))

'''
List containing tuples
tuples must follow following format: (board position, Player Color/Indicator, side if on single-person side (default to False))
'''
@dataclass
class stoneMove:
    pos: int
    owner: chr
    side: int = -1

moveList = [stoneMove(2, '1', 0), stoneMove(3, '2', 1), stoneMove(6, '1')] 

def drawBoard(stdscr):
    curses.noecho()
    curses.curs_set(0)
    stdscr.keypad(True)
    stdscr.clear()

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

    while True:
        stdscr.erase()
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
                    if 0 < y < (2*yscale) or  (4*yscale) < y < (6*yscale):
                        if x < (12*xscale) and x > (8*xscale):
                            continue
                        if x in [xscale, 13*xscale] or (y in [yscale, 5*yscale] and (0 < x < 2*xscale or 12*xscale < x < 14*xscale)):
                            stdscr.insch(int((height/2 - (6*yscale)/2) + y), int((width/2 - (16*xscale)/2) + x), 'X')
                    if (x == (7*xscale) and 2*yscale < y < 4*yscale) or (y == 3*yscale and 6*xscale < x < 8*xscale):
                        stdscr.insch(int((height/2 - (6*yscale)/2) + y), int((width/2 - (16*xscale)/2) + x), 'X')
                    
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
                            stdscr.addch(int((height/2 - (6*yscale)/2) + y), int((width/2 - (16*xscale)/2) + x), '#')

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


curses.wrapper(drawBoard)
