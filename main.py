import player
import board
from random import randint

p1 = player.Player(1, False)
p2 = player.Player(2, False)

b = board.Board(p1, p2)
while True:
    while True:
        b.printBoard()
        roll = p1.roll()
        print(f"P1 Rolled {roll}")
        if roll != 0:
            instr = int(input("Chip to move: "))
            ret = b.moveChip(0, instr, roll)
            print(ret)
            b.printBoard()
            print("\n")
            if ret in [1, 3]:
                if ret == 1:
                    print("Illegal Move, go again")
                else:
                    print("Land on Rosette, Play Again!")
            else:
                break
        else:
            break

    while True:
        roll = p2.roll()
        print(f"P2 Rolled {roll}")

        ret = b.moveChip(1, randint(0, 6), roll)
        #print(ret)
        #b.printBoard()
        #print("\n")
        if ret not in [1, 3]:

            break
        

