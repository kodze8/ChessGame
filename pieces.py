# from board import Board

blackIcons = {"Pawn": "♙", "Rook": "♖", "Knight": "♘", "Bishop": "♗", "King": "♔", "Queen": "♕"}
whiteIcons = {"Pawn": "♟", "Rook": "♜", "Knight": "♞", "Bishop": "♝", "King": "♚", "Queen": "♛"}


class Piece:

    def __init__(self, position, color, board):
        self.board = board
        self.color = color
        self.position = position

    @property
    def positionS(self):
        return self.position

    @positionS.setter
    def positionS(self, position):
        self.position = position

    @property
    def colorSet(self):
        return self.color

    def checkMove(self, dest):
        if dest[0] == self.positionS[0] and dest[1] == self.positionS[1]:
            return False
        return True

    def move(self, dest):
        if self.checkMove(dest):
            Xtemp = self.positionS[0]
            Ytemp = self.positionS[1]

            self.board.board[(Xtemp, Ytemp)] = None
            self.positionS = dest

    def getName(self):
        dicToSearch = blackIcons
        if self.color == "White":
            dicToSearch = whiteIcons
        for k, v in dicToSearch.items():
            if self.getIcon() == v:
                return k

    def getIcon(self):
        return None


class Knight(Piece):
    def getName(self):
        return "Knight"

    def move(self, dest):
        super().move(dest)
        self.board.board[(dest[0], dest[1])] = Knight(dest, self.color, self.board)

    def checkMove(self, dest):
        super().checkMove(dest)
        if ((dest[0] == chr(ord(self.positionS[0]) + 2) or dest[0] == chr(ord(self.positionS[0]) - 2))
                and (dest[1] == self.positionS[1] + 1 or dest[1] == self.positionS[1] - 1)):
            return True
        if ((dest[1] == self.positionS[1] + 2 or dest[1] == self.positionS[1] - 2) and
                (dest[0] == chr(ord(self.positionS[0]) + 1) or dest[0] == chr(ord(self.positionS[0]) - 1))):
            return True
        return False

    def getIcon(self):
        if self.color == "White":
            return "♞"
        else:
            return "♘"


class Rook(Piece):
    def getName(self):
        return "Rook"

    def move(self, dest):
        super().move(dest)
        self.board.board[(dest[0], dest[1])] = Rook(dest, self.color, self.board)

    def checkMove(self, dest):
        super().checkMove(dest)
        if dest[0] == self.positionS[0]:
            d = dest[1]
            c = self.positionS[1]
            if d > c:
                c += 1
                while d > c:
                    if self.board[(dest[0], c)] is not None:
                        return False
                    c += 1
                return True
            elif d < c:
                c -= 1
                while d < c:
                    if self.board[(dest[0], c)] is not None:
                        return False
                    c -= 1
                return True
        elif dest[1] == self.positionS[1]:
            d = ord(dest[0])
            c = ord(self.positionS[0])
            if d > c:
                c += 1
                while d > c:
                    if self.board[(chr(c), dest[1])] is not None:
                        return False
                    c += 1
                return True
            elif d < c:
                c -= 1
                while d < c:
                    if self.board[(chr(c), dest[1])] is not None:
                        return False
                    c -= 1
                return True
        return False

    def getIcon(self):
        if self.color == "White":
            return "♜"
        else:
            return "♖"


class Bishop(Piece):
    def getName(self):
        return "Bishop"

    def move(self, dest):
        super().move(dest)
        self.board.board[(dest[0], dest[1])] = Bishop(dest, self.color, self.board)

    def checkMove(self, dest):
        c0, c1 = ord(self.positionS[0]), self.positionS[1]
        if ord(dest[0]) == c0 or dest[1] == c1:
            return False
        while ord(dest[0]) != c0 and dest[1] != c1:
            if self.board[(chr(c0), c1)] is not None and (c0 != ord(self.positionS[0]) and c1 != self.position[1]):
                return False
            if c0 > ord(dest[0]):
                c0 -= 1
            else:
                c0 += 1
            if c1 > dest[1]:
                c1 -= 1
            else:
                c1 += 1
        if dest[0] == chr(c0) and dest[1] == c1:
            return True
        else:
            return False

    def getIcon(self):
        if self.color == "White":
            return "♝"
        else:
            return "♗"


class Queen(Piece):
    def getName(self):
        return "Queen"

    def move(self, dest):
        super().move(dest)
        self.board.board[(dest[0], dest[1])] = Queen(dest, self.color, self.board)

    def checkMove(self, dest):
        pass
        super().checkMove(dest)
        bp = Bishop(self.position, self.color, self.board)
        rook = Rook(self.position, self.color, self.board)
        return bp.checkMove(dest) or rook.checkMove(dest)

    def getIcon(self):
        if self.color == "White":
            return "♛"
        else:
            return "♕"


class King(Piece):
    def getName(self):
        return "King"

    def move(self, dest):
        super().move(dest)
        self.board.board[(dest[0], dest[1])] = Queen(dest, self.color, self.board)

    def checkMove(self, dest):
        # check if moving unit is only one
        c0, c1 = ord(self.positionS[0]), self.positionS[1]
        d0, d1 = ord(dest[0]), dest[1]
        zeros_are_correct = True
        if c0 > d0:
            if c0 - d0 != 1:
                zeros_are_correct = False
        else:
            if d0 - c0 == 1:
                zeros_are_correct = False

        if c1 > d1:
            if c1 - d1 != 1:
                zeros_are_correct = False

        else:
            if d1 - c1 == 1:
                zeros_are_correct = False

        # chech for possible attacks
        for char_code in range(ord('A'), ord('H') + 1):
            char = chr(char_code)
            for i in range(1, 9):
                if self.board[(char, i)] is not None and (char != self.position[0] and i != self.position[1]):
                    if self.board.getPiece((char, i)).checkMove(dest):
                        return False
        return True and zeros_are_correct

    def getIcon(self):
        if self.color == "White":
            return "♚"
        else:
            return "♔"


class Pawn(Piece):

    def getName(self):
        return "Pawn"

    def move(self, dest):
        super().move(dest)
        self.board.board[(dest[0], dest[1])] = Pawn(dest, self.color, self.board)

    def getIcon(self):
        if self.color == "White":
            return "♟"
        else:
            return "♙"

    def checkMove(self, dest):
        if self.board[(dest[0], dest[1])] is None and self.positionS[1] == dest[1]:
            if self.color == "Black" and self.positionS[0] == 'G':
                if dest[0] == 'E' and self.board[('F', dest[1])] is None:
                    return True
            elif self.color == "White" and self.positionS[0] == 'B':
                if dest[0] == 'D' and self.board[('C', dest[1])] is None:
                    return True
            if self.color == "Black" and dest[0] == (chr(ord(self.position[0]) - 1)):
                return True
            elif self.color == "White" and dest[0] == (chr(ord(self.position[0]) + 1)):
                return True
            else:
                return False
        if not self.board[(dest[0], dest[1])] is None:
            if self.color == "Black" and dest[0] == (chr(ord(self.position[0]) - 1)) and (
                    dest[1] == self.positionS[1] + 1 or dest[1] == self.positionS[1] - 1):
                return True
            elif self.color == "White" and dest[0] == (chr(ord(self.position[0]) + 1)) and (
                    dest[1] == self.positionS[1] + 1 or dest[1] == self.positionS[1] - 1):
                return True
            else:
                return False
        else:
            return False
