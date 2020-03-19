import curses
from math import floor

def drawBoard(stdscr):
    curses.noecho()
    curses.curs_set(0)
    stdscr.keypad(True)
    stdscr.clear()

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

curses.wrapper(drawBoard)
