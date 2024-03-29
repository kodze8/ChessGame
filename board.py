from pieces import Piece, Pawn, Rook, Knight, Bishop, Queen, King
import copy


class Board:

    def __init__(self):
        # declared all pieces with their position and
        self.rookW1 = Rook(('A', 1), "White", self)
        self.knightW2 = Knight(('A', 2), "White", self)
        self.bishopW3 = Bishop(('A', 3), "White", self)
        self.queenW4 = Queen(('A', 4), "White", self)
        self.kingW5 = King(('A', 5), "White", self)
        self.rookW8 = Rook(('A', 8), "White", self)
        self.knightW7 = Knight(('A', 7), "White", self)
        self.bishopW6 = Bishop(('A', 6), "White", self)

        self.rookB1 = Rook(('H', 1), "Black", self)
        self.knightB2 = Knight(('H', 2), "Black", self)
        self.bishopB3 = Bishop(('H', 3), "Black", self)
        self.queenB4 = Queen(('H', 4), "Black", self)
        self.kingB5 = King(('H', 5), "Black", self)
        self.rookB8 = Rook(('H', 8), "Black", self)
        self.knightB7 = Knight(('H', 7), "Black", self)
        self.bishopB6 = Bishop(('H', 6), "Black", self)

        self.pawnW1 = Pawn(('B', 1), "White", self)
        self.pawnW2 = Pawn(('B', 2), "White", self)
        self.pawnW3 = Pawn(('B', 3), "White", self)
        self.pawnW4 = Pawn(('B', 4), "White", self)
        self.pawnW5 = Pawn(('B', 5), "White", self)
        self.pawnW6 = Pawn(('B', 6), "White", self)
        self.pawnW7 = Pawn(('B', 7), "White", self)
        self.pawnW8 = Pawn(('B', 8), "White", self)

        self.pawnB1 = Pawn(('G', 1), "Black", self)
        self.pawnB2 = Pawn(('G', 2), "Black", self)
        self.pawnB3 = Pawn(('G', 3), "Black", self)
        self.pawnB4 = Pawn(('G', 4), "Black", self)
        self.pawnB5 = Pawn(('G', 5), "Black", self)
        self.pawnB6 = Pawn(('G', 6), "Black", self)
        self.pawnB7 = Pawn(('G', 7), "Black", self)
        self.pawnB8 = Pawn(('G', 8), "Black", self)

        self.white_pawns = [self.pawnW1, self.pawnW2, self.pawnW3, self.pawnW4, self.pawnW5, self.pawnW6, self.pawnW7,
                            self.pawnW8]
        self.blk_pawns = [self.pawnB1, self.pawnB2, self.pawnB3, self.pawnB4, self.pawnB5, self.pawnB6, self.pawnB7,
                          self.pawnB8]

        self.board = {}
        for char_code in range(ord('A'), ord('H') + 1):
            char = chr(char_code)
            for i in range(1, 9):
                self.board[(char, i)] = None

    def __getitem__(self, position):
        return self.board[position]

    def getPiece(self, position):
        return self.board[position]

    def placePieces(self):
        self.setPiece(('A', 1), self.rookW1)
        self.setPiece(('A', 2), self.knightW2)
        self.setPiece(('A', 3), self.bishopW3)
        self.setPiece(('A', 4), self.queenW4)
        self.setPiece(('A', 5), self.kingW5)
        self.setPiece(('A', 6), self.bishopW6)
        self.setPiece(('A', 7), self.knightW7)
        self.setPiece(('A', 8), self.rookW8)

        self.setPiece(('H', 1), self.rookB1)
        self.setPiece(('H', 2), self.knightB2)
        self.setPiece(('H', 3), self.bishopB3)
        self.setPiece(('H', 4), self.queenB4)
        self.setPiece(('H', 5), self.kingB5)
        self.setPiece(('H', 6), self.bishopB6)
        self.setPiece(('H', 7), self.knightB7)
        self.setPiece(('H', 8), self.rookB8)

        for (a, b), y in self.board.items():
            if a == 'B':
                self.setPiece((a, b), self.white_pawns[b - 1])
            elif a == 'G':
                self.setPiece((a, b), self.blk_pawns[b - 1])

    def setPiece(self, position, piece):
        self.board[position] = piece

    def king_needs_help(self, player_color):
        kng = self.kingW5
        if player_color == "Black":
            kng = self.kingB5
        loc0, loc1 = kng.positionS[0], kng.positionS[1]
        for _, y in self.board.items():
            if y is not None and y.color != kng.color:
                if y.checkMove((loc0, loc1)):
                    return True
        return False

    def after_move_king_still_needs_help(self, start, end, player):
        temp = Board()
        temp.board = copy.deepcopy(self.board)

        pc = temp.getPiece(start)
        old_position = pc.positionS
        pc.positionS = end
        temp.setPiece(end, pc)
        temp.board[old_position] = None

        # if king protect itself and moves
        if isinstance(temp.getPiece(end), King):
            if temp.getPiece(end).color == player:
                loc0, loc1 = temp.getPiece(end).positionS[0], temp.getPiece(end).positionS[1]
                for piece in temp.board.values():
                    if piece is not None and piece.color != player:
                        if isinstance(piece, King):
                            continue  # Skip checking the opponent's king
                        if piece.checkMove((loc0, loc1)):
                            return True  # King is not safe
                return False

        # if another piece of player tries to save the King
        kng = temp.kingW5 if player == "White" else temp.kingB5
        loc0, loc1 = kng.positionS[0], kng.positionS[1]

        for piece in temp.board.values():
            if piece is not None and piece.color != player:
                if isinstance(piece, King):
                    continue  # Skip checking the opponent's king
                if piece.checkMove((loc0, loc1)):
                    return True  # King is not safe

        return False  # King is safe

    def makeMove(self, start_position, end_position, player):
        if self.board[start_position] is not None:
            pc = self.getPiece(start_position)
            if pc.color == player:
                if self.getPiece(end_position) == None or self.getPiece(end_position).color is not player:
                    if self.board[start_position].checkMove(end_position):
                        if self.king_needs_help(player):
                            if self.after_move_king_still_needs_help(start_position, end_position, player):
                                print("Check! enter another input!")
                                return False
                        pc = self.getPiece(start_position)
                        oldPosition = pc.positionS
                        pc.positionS = end_position
                        self.setPiece(end_position, pc)
                        self.board[oldPosition] = None
                        return True
                    else:
                        print("INVALID MOVE")
                        return False
                else:
                    print("You can't kill your piece")
                    return False
            else:
                print("It's not your piece")
                return False

    def displayBoard(self):
        temp = ""
        print("  (1) (2)(3) (4) (5)(6) (7)(8)")
        for (a, b), y in self.board.items():
            string_to_add = ""
            if y is not None:
                string_to_add = "[" + y.getIcon() + "]"
            else:
                string_to_add += "[ ]"
            if b == 1:
                temp += str(a) + " " + string_to_add
            elif b == 8:
                temp += string_to_add
                print(temp)
                temp = ""
            else:
                temp += string_to_add
