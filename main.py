import player
import board

p1 = player.Player(1, False)
p2 = player.Player(2, False)

b = board.Board(p1, p2)

while True:
    instr = input("Player 1 Rolls")
    roll = p1.roll()
    print(f"Rolled {roll}")
    ret = b.moveChip(0, 0, roll)
    print(ret)
    b.printBoard()
    print("\n")

    instr = input("Player 2 Rolls")
    roll = p2.roll()
    print(f"Rolled {roll}")
    ret = b.moveChip(1, 0, roll)
    print(ret)
    b.printBoard()
    print("\n")


