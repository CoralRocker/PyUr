import player
import board

p1 = player.Player(1, False)
p2 = player.Player(2, False)

b = board.Board(p1, p2)
b.printBoard()
while True:
    instr = input("Player 1 Rolls")
    while True:
        roll = p1.roll()
        print(f"Rolled {roll}")
        instr = int(input("Chip to move"))
        ret = b.moveChip(0, instr, roll)
        print(ret)
        b.printBoard()
        print("\n")
        if ret not in [1, 3]:
            break

    instr = input("Player 2 Rolls")
    while True:
        roll = p2.roll()
        print(f"Rolled {roll}")
        ret = b.moveChip(1, 0, roll)
        print(ret)
        b.printBoard()
        print("\n")
        if ret not in [1, 3]:
            break
        

