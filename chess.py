from board import Board
from pieces import *


def game_is_over():
    return False


class Chess:
    def __init__(self):
        self.board = Board()
        self.cuurrentPlayer = "White"

    def swapPlayers(self):
        if self.cuurrentPlayer == "White":
            self.cuurrentPlayer = "Black"
        else:
            self.cuurrentPlayer = "White"

    @staticmethod
    def isStringValidMove(move_input):
        try:
            a, b = move_input.split(" ")
            if len(a) == 2 and len(b) == 2:
                if a[0] and b[0] in [chr(x) for x in range(65, 73)]:
                    if int(a[1]) and int(b[1]) in [x for x in range(1, 9)]:
                        return True
            print("Invalid Input ")
            return False
        except:
            print("Invalid Input ")
            return False

    def play(self):
        self.board.placePieces()
        self.board.displayBoard()
        while not game_is_over():
            inp = input(self.cuurrentPlayer + "'s turn. Enter a move:\n>")
            if inp == "Exit":
                return

            while not self.isStringValidMove(inp):
                inp = input("Put valid input!  " + self.cuurrentPlayer + "'s turn. Enter a move:\n>")
                if inp == "Exit":
                    return
            a, b = inp.split(" ")
            curret, destination = (a[0], int(a[1])), (b[0], int(b[1]))

            while not self.board.makeMove(curret, destination, self.cuurrentPlayer):
                inp = input("Put valid input!  " + self.cuurrentPlayer + "'s turn. Enter a move:\n>")
                if inp == "Exit":
                    return
                if self.isStringValidMove(inp):
                    a, b = inp.split(" ")
                    curret, destination = (a[0], int(a[1])), (b[0], int(b[1]))

            # Promotion
            if self.board.getPiece(destination) is not None:
                if self.board.getPiece(destination).getName() == "Pawn":
                    if b[0] == 'A' or b[0] == 'H':
                        inp = input("Do you want to get promoted?\nChoose: Queen, Knight, Rook, Bishop or None\n>")
                        while inp != "Queen" and inp != "Knight" and inp != "Rook" and inp != "Bishop" and inp != "None":
                            inp = input("Enter valid Value\nChoose: Queen, Knight, Rook, Bishop or None\n>")
                        if inp == "None":
                            pass
                        elif inp == "Queen":
                            self.board.board[destination] = None
                            self.board.board[destination] = Queen(destination, self.cuurrentPlayer, self.board)
                        elif inp == "Knight":
                            self.board.board[destination] = None
                            self.board.board[destination] = Knight(destination, self.cuurrentPlayer, self.board)
                        elif inp == "Rook":
                            self.board.board[destination] = None
                            self.board.board[destination] = Rook(destination, self.cuurrentPlayer, self.board)
                        elif inp == "Bishop":
                            self.board.board[destination] = None
                            self.board.board[destination] = Bishop(destination, self.cuurrentPlayer, self.board)

            self.board.displayBoard()
            self.swapPlayers()


if __name__ == "__main__":
    game = Chess()
    game.play()
