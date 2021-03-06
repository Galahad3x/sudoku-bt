#!/usr/bin/python3

import pygame
import sys
from tqdm import tqdm

pygame.init()

SIZE = WIDTH, HEIGHT = 672, 672
BLACK = [100, 100, 100]
WHITE = [255, 255, 255]
RED = [255, 0, 0]

SCREEN = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Chess')


# ball = pygame.image.load("Images/basket.png")
# ball = pygame.transform.scale(ball,(64,64))
# ballrect = ball.get_rect()

class Piece:
    def __init__(self, color, pClass, coords):
        self.color = color  # "b" or "w"
        self.pClass = pClass  # "pawn","tower","knight","bishop","queen","king"
        self.hasMoved = False
        self.up, self.right = coords
        image_route = "Images/" + color + "" + pClass + ".png"
        # image_route = "Images/ball.png"
        self.image = pygame.image.load(image_route).convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rectangle = self.image.get_rect()

    def draw(self):
        for y, letter in enumerate("ABCDEFGH"):
            if letter == self.up:
                self.rectangle.y = y * 84 + 10
                self.rectangle.x = self.right * 84 + 10
                SCREEN.blit(self.image, self.rectangle)
                break

    def update(self, new_coords):
        self.hasMoved = True
        self.up, self.right = new_coords
        self.rectangle = self.image.get_rect()
        for y, letter in enumerate("ABCDEFGH"):
            if letter == self.up:
                self.rectangle.y = y * 84 + 10
                self.rectangle.x = self.right * 84 + 10
                break

    def copy(self):
        return Piece(self.color, self.pClass, (self.up, self.right))


class Board:
    @staticmethod
    def generate_board_array(player_side):
        b_array = {}
        if player_side.startswith("w"):
            for letter in "ABCDEFGH":
                b_array[letter] = []
                if letter == "A":
                    b_array[letter].append(Piece("b", "tower", (letter, 0)))
                    b_array[letter].append(Piece("b", "knight", (letter, 1)))
                    b_array[letter].append(Piece("b", "bishop", (letter, 2)))
                    b_array[letter].append(Piece("b", "queen", (letter, 3)))
                    b_array[letter].append(Piece("b", "king", (letter, 4)))
                    b_array[letter].append(Piece("b", "bishop", (letter, 5)))
                    b_array[letter].append(Piece("b", "knight", (letter, 6)))
                    b_array[letter].append(Piece("b", "tower", (letter, 7)))
                elif letter == "B":
                    for ind in range(8):
                        b_array[letter].append(Piece("b", "pawn", (letter, ind)))
                elif letter == "G":
                    for ind in range(8):
                        b_array[letter].append(Piece("w", "pawn", (letter, ind)))
                elif letter == "H":
                    b_array[letter].append(Piece("w", "tower", (letter, 0)))
                    b_array[letter].append(Piece("w", "knight", (letter, 1)))
                    b_array[letter].append(Piece("w", "bishop", (letter, 2)))
                    b_array[letter].append(Piece("w", "queen", (letter, 3)))
                    b_array[letter].append(Piece("w", "king", (letter, 4)))
                    b_array[letter].append(Piece("w", "bishop", (letter, 5)))
                    b_array[letter].append(Piece("w", "knight", (letter, 6)))
                    b_array[letter].append(Piece("w", "tower", (letter, 7)))
                else:
                    for ind in range(8):
                        b_array[letter].append(None)
        elif player_side.startswith("b"):
            for letter in "ABCDEFGH":
                b_array[letter] = []
                if letter == "A":
                    b_array[letter].append(Piece("w", "tower", (letter, 0)))
                    b_array[letter].append(Piece("w", "knight", (letter, 1)))
                    b_array[letter].append(Piece("w", "bishop", (letter, 2)))
                    b_array[letter].append(Piece("w", "queen", (letter, 3)))
                    b_array[letter].append(Piece("w", "king", (letter, 4)))
                    b_array[letter].append(Piece("w", "bishop", (letter, 5)))
                    b_array[letter].append(Piece("w", "knight", (letter, 6)))
                    b_array[letter].append(Piece("w", "tower", (letter, 7)))
                elif letter == "B":
                    for ind in range(8):
                        b_array[letter].append(Piece("w", "pawn", (letter, ind)))
                elif letter == "G":
                    for ind in range(8):
                        b_array[letter].append(Piece("b", "pawn", (letter, ind)))
                elif letter == "H":
                    b_array[letter].append(Piece("b", "tower", (letter, 0)))
                    b_array[letter].append(Piece("b", "knight", (letter, 1)))
                    b_array[letter].append(Piece("b", "bishop", (letter, 2)))
                    b_array[letter].append(Piece("b", "queen", (letter, 3)))
                    b_array[letter].append(Piece("b", "king", (letter, 4)))
                    b_array[letter].append(Piece("b", "bishop", (letter, 5)))
                    b_array[letter].append(Piece("b", "knight", (letter, 6)))
                    b_array[letter].append(Piece("b", "tower", (letter, 7)))
                else:
                    for ind in range(8):
                        b_array[letter].append(None)
        return b_array

    def __init__(self, name, player_side):
        self.name = name
        self.player_side = player_side
        self.board_array = Board.generate_board_array(player_side)
        self.check = {'b': False, 'w': False}

    def new_board(self, name, player_side, board_array, check):
        self.name = name
        self.player_side = player_side
        self.board_array = board_array
        self.check = check

    def copy(self):
        new_barray = {}
        for letter in "ABCDEFGH":
            new_barray[letter] = []
            for piece in self.board_array[letter]:
                if piece is not None:
                    new_barray[letter].append(piece.copy())
                else:
                    new_barray[letter].append(None)
        new_board = Board("new_board", "w")
        new_board.new_board(new_board.name, self.player_side, new_barray, self.check)
        return new_board

    def move_piece(self, piece_coords, new_coords):
        if self.board_array[piece_coords[0]][piece_coords[1]] is not None:
            self.board_array[piece_coords[0]][piece_coords[1]].update((new_coords[0], new_coords[1]))
            self.board_array[new_coords[0]][new_coords[1]] = self.board_array[piece_coords[0]][piece_coords[1]]
            self.board_array[piece_coords[0]][piece_coords[1]] = None
            if self.name == "BOARD":
                print("Moved piece " + str(piece_coords) + " to " + str(new_coords))
            king_x = king_y = None
            stop = False
            for y in self.board_array.keys():
                for x, piece in enumerate(self.board_array[y]):
                    if piece is not None and piece.color == self.board_array[new_coords[0]][new_coords[1]].color \
                            and piece.pClass == "king":
                        king_x, king_y = x, y
                        stop = True
                        break
                if stop:
                    break
            if self.board_array[new_coords[0]][new_coords[1]].pClass == "pawn":
                if new_coords[0] == "A" or new_coords[0] == "H":
                    self.board_array[new_coords[0]][new_coords[1]].pClass = "queen"
                    image_route = "Images/" + self.board_array[new_coords[0]][new_coords[1]].color + "" + "queen" + ".png"
                    self.image = pygame.image.load(image_route).convert_alpha()
                    self.image = pygame.transform.scale(self.image, (64, 64))
                    self.rectangle = self.image.get_rect()
            self.check['b'] = self.check['w'] = False
            stop = False
            for y in self.board_array.keys():
                for x, piece in enumerate(self.board_array[y]):
                    if piece is not None \
                            and piece.pClass == "king" \
                            and piece.color != self.board_array[new_coords[0]][new_coords[1]].color:
                        if self.is_valid_move(new_coords, (y, x)):
                            if self.board_array[new_coords[0]][new_coords[1]].color == "w":
                                self.check['b'] = True
                                stop = True
                                break
                            elif self.board_array[new_coords[0]][new_coords[1]].color == "b":
                                self.check['w'] = True
                                stop = True
                                break
                    if piece is not None \
                            and piece.color != self.board_array[new_coords[0]][new_coords[1]].color \
                            and self.is_valid_move((y, x), (king_y, king_x)):
                        if piece.color == "b":
                            self.check['w'] = True
                            stop = True
                            break
                        else:
                            self.check['b'] = True
                            stop = True
                            break
                    elif piece is not None:
                        if piece.color == "b":
                            self.check['w'] = False or self.check['w']
                        else:
                            self.check['b'] = False or self.check['b']
                if stop:
                    break
        if self.name == "BOARD":
            if self.check['w']:
                print("White in check")
            if self.check['b']:
                print("Black in check")
            place_pieces()

    def is_valid_move(self, from_coords, to_coords):
        if to_coords[0] is None or from_coords[0] is None or to_coords[1] is None or from_coords[1] is None:
            return False
        piece_from = self.board_array[from_coords[0]][from_coords[1]]
        piece_to = self.board_array[to_coords[0]][to_coords[1]]
        # print("Attempting to move " + str(from_coords) + " to " + str(to_coords))
        if piece_from is None:
            return False
        if piece_to is not None:
            if piece_to.color == piece_from.color:
                return False
        if self.is_valid_move_2(from_coords, to_coords):
            current_color = piece_from.color
            new_board = self.copy()
            new_board.move_piece(from_coords, to_coords)
            if new_board.check[current_color]:
                return False
            else:
                return True
        return False

    def is_valid_move_2(self, from_coords, to_coords):
        piece_from = self.board_array[from_coords[0]][from_coords[1]]
        # print("Attempting to move " + str(from_coords) + " to " + str(to_coords))
        if piece_from.pClass == "pawn":
            for y, letter in enumerate("ABCDEFGH"):
                if not piece_from.hasMoved:
                    if self.player_side == piece_from.color and piece_from.up == letter:
                        if y >= 2 and to_coords[0] == "ABCDEFGH"[y - 2] and \
                                self.board_array["ABCDEFGH"[y - 1]][to_coords[1]] is None and \
                                self.board_array["ABCDEFGH"[y - 2]][to_coords[1]] is None and \
                                to_coords[1] == from_coords[1]:
                            return True
                    elif self.player_side != piece_from.color and \
                            piece_from.up == letter and to_coords[0] == "ABCDEFGH__"[y + 2] and \
                            self.board_array["ABCDEFGH_"[y + 1]][to_coords[1]] is None and \
                            self.board_array["ABCDEFGH__"[y + 2]][to_coords[1]] is None and \
                            to_coords[1] == from_coords[1]:
                        return True
                if self.player_side == piece_from.color and \
                        piece_from.up == letter and to_coords[0] == "ABCDEFGH"[y - 1] and \
                        to_coords[1] == from_coords[1] and \
                        self.board_array[to_coords[0]][to_coords[1]] is None:
                    return True
                elif self.player_side != piece_from.color and \
                        piece_from.up == letter and to_coords[0] == "ABCDEFGH_"[y + 1] and \
                        to_coords[1] == from_coords[1] and \
                        self.board_array[to_coords[0]][to_coords[1]] is None:
                    return True
                if y >= 1 and self.player_side == piece_from.color and \
                        piece_from.up == letter and to_coords[0] == "ABCDEFGH"[y - 1] and \
                        self.board_array[to_coords[0]][to_coords[1]] is not None and \
                        abs(to_coords[1] - from_coords[1]) == 1:
                    return True
                elif y < 7 and self.player_side != piece_from.color and \
                        piece_from.up == letter and to_coords[0] == "ABCDEFGH_"[y + 1] and \
                        self.board_array[to_coords[0]][to_coords[1]] is not None and \
                        abs(to_coords[1] - from_coords[1]) == 1:
                    return True
            return False
        elif piece_from.pClass == "tower":
            if to_coords[0] == from_coords[0]:
                for elem in range(min(from_coords[1], to_coords[1]) + 1, max(from_coords[1], to_coords[1])):
                    if self.board_array[to_coords[0]][elem] is not None:
                        return False
                return True
            elif to_coords[1] == from_coords[1]:
                for elem in "ABCDEFGH"["ABCDEFGH".find(min(from_coords[0], to_coords[0])) + 1:"ABCDEFGH".find(
                        max(from_coords[0], to_coords[0]))]:
                    if self.board_array[elem][to_coords[1]] is not None:
                        return False
                return True
            else:
                return False
        elif piece_from.pClass == "knight":
            for y, letter in enumerate("ABCDEFGH"):
                if piece_from.up == letter:
                    if to_coords[0] == "ABCDEFGH__"[y + 2] or (y >= 2 and to_coords[0] == "ABCDEFGH"[y - 2]):
                        if to_coords[1] == from_coords[1] + 1 or to_coords[1] == from_coords[1] - 1:
                            return True
                    elif to_coords[0] == "ABCDEFGH_"[y + 1] or (y >= 1 and to_coords[0] == "ABCDEFGH"[y - 1]):
                        if to_coords[1] == from_coords[1] + 2 or to_coords[1] == from_coords[1] - 2:
                            return True
                    return False
        elif piece_from.pClass == "bishop":
            left = piece_from.right
            top_left = top_right = bot_left = bot_right = True
            lett_ind = 0
            to_ind = 0
            for y, letter in enumerate("ABCDEFGH"):
                if piece_from.up == letter:
                    lett_ind = y
                if letter == to_coords[0]:
                    to_ind = y
            if lett_ind == to_ind or from_coords[1] == to_coords[1]:
                return False
            for i in range(1, 8):
                if top_left:
                    if (lett_ind - i) >= 0 and (left - i) >= 0 and \
                            "ABCDEFGH"[lett_ind - i] == to_coords[0] and (left - i) == to_coords[1]:
                        return True
                if bot_right:
                    if (lett_ind + i) < 8 and (left + i) < 8 and \
                            "ABCDEFGH"[lett_ind + i] == to_coords[0] and (left + i) == to_coords[1]:
                        return True
                if top_right:
                    if (lett_ind - i) >= 0 and (left + i) < 8 and \
                            "ABCDEFGH"[lett_ind - i] == to_coords[0] and (left + i) == to_coords[1]:
                        return True
                if bot_left:
                    if (lett_ind + i) < 8 and (left - i) >= 0 and \
                            "ABCDEFGH"[lett_ind + i] == to_coords[0] and (left - i) == to_coords[1]:
                        return True
                if (lett_ind - i) >= 0 and (left - i) >= 0 and \
                        self.board_array["ABCDEFGH"[lett_ind - i]][left - i] is not None:
                    top_left = False
                if (lett_ind - i) >= 0 and (left + i) < 8 and \
                        self.board_array["ABCDEFGH"[lett_ind - i]][left + i] is not None:
                    top_right = False
                if (lett_ind + i) < 8 and (left - i) >= 0 and \
                        self.board_array["ABCDEFGH"[lett_ind + i]][left - i] is not None:
                    bot_left = False
                if (lett_ind + i) < 8 and (left + i) < 8 and \
                        self.board_array["ABCDEFGH"[lett_ind + i]][left + i] is not None:
                    bot_right = False
            return False
        elif piece_from.pClass == "queen":
            if to_coords[0] == from_coords[0]:
                for elem in range(min(from_coords[1], to_coords[1]) + 1, max(from_coords[1], to_coords[1])):
                    if self.board_array[to_coords[0]][elem] is not None:
                        return False
                return True
            elif to_coords[1] == from_coords[1]:
                for elem in "ABCDEFGH"["ABCDEFGH".find(min(from_coords[0], to_coords[0])) + 1:"ABCDEFGH".find(
                        max(from_coords[0], to_coords[0]))]:
                    if self.board_array[elem][to_coords[1]] is not None:
                        return False
                return True
            left = piece_from.right
            lett_ind = 0
            top_left = top_right = bot_left = bot_right = True
            for y, letter in enumerate("ABCDEFGH"):
                if piece_from.up == letter:
                    lett_ind = y
            for i in range(1, 8):
                if top_left:
                    if (lett_ind - i) >= 0 and (left - i) >= 0 and \
                            "ABCDEFGH"[lett_ind - i] == to_coords[0] and (left - i) == to_coords[1]:
                        return True
                if bot_right:
                    if (lett_ind + i) < 8 and (left + i) < 8 and \
                            "ABCDEFGH"[lett_ind + i] == to_coords[0] and (left + i) == to_coords[1]:
                        return True
                if top_right:
                    if (lett_ind - i) >= 0 and (left + i) < 8 and \
                            "ABCDEFGH"[lett_ind - i] == to_coords[0] and (left + i) == to_coords[1]:
                        return True
                if bot_left:
                    if (lett_ind + i) < 8 and (left - i) >= 0 and \
                            "ABCDEFGH"[lett_ind + i] == to_coords[0] and (left - i) == to_coords[1]:
                        return True
                if (lett_ind - i) >= 0 and (left - i) >= 0 and \
                        self.board_array["ABCDEFGH"[lett_ind - i]][left - i] is not None:
                    top_left = False
                if (lett_ind - i) >= 0 and (left + i) < 8 and \
                        self.board_array["ABCDEFGH"[lett_ind - i]][left + i] is not None:
                    top_right = False
                if (lett_ind + i) < 8 and (left - i) >= 0 and \
                        self.board_array["ABCDEFGH"[lett_ind + i]][left - i] is not None:
                    bot_left = False
                if (lett_ind + i) < 8 and (left + i) < 8 and \
                        self.board_array["ABCDEFGH"[lett_ind + i]][left + i] is not None:
                    bot_right = False
            return False
        elif piece_from.pClass == "king":
            if to_coords[0] == from_coords[0] or to_coords[1] == from_coords[1]:
                return (abs(ord(from_coords[0]) - ord(to_coords[0])) + abs(from_coords[1] - to_coords[1])) == 1
            else:
                return (abs(ord(from_coords[0]) - ord(to_coords[0]))) == 1 and (
                    abs(from_coords[1] - to_coords[1])) == 1
        else:
            return False

    def print_state(self):
        for letter in "ABCDEFGH":
            print(letter, end=": ")
            for piece in self.board_array[letter]:
                if piece is not None:
                    print(piece.color, piece.pClass, "\t", piece.right, end=" ")
                else:
                    print("None", end=" ")
            print()

    def possible_moves(self, sidee):
        moves = []
        for y in self.board_array.keys():
            for x, piece in enumerate(self.board_array[y]):
                if piece is not None and piece.color == sidee:
                    for yy in self.board_array.keys():
                        for xx, piece2 in enumerate(self.board_array[y]):
                            if self.is_valid_move((y, x), (yy, xx)):
                                moves.append(((y, x), (yy, xx)))
        return moves

    def has_moves(self, sidee):
        for y in self.board_array.keys():
            for x, piece in enumerate(self.board_array[y]):
                if piece is not None and piece.color == sidee:
                    for yy in self.board_array.keys():
                        for xx, piece2 in enumerate(self.board_array[y]):
                            if self.is_valid_move((y, x), (yy, xx)):
                                return True
        return False

    def possible_moves_from(self, piece_coords):
        moves = []
        piece = self.board_array[piece_coords[0]][piece_coords[1]]
        if piece is not None:
            for yy in self.board_array.keys():
                for xx, piece2 in enumerate(self.board_array[yy]):
                    if self.is_valid_move((piece_coords[0], piece_coords[1]), (yy, xx)):
                        moves.append(((piece_coords[0], piece_coords[1]), (yy, xx)))
        return moves

    def score(self, side):
        score = 0
        for y in self.board_array.keys():
            for x, piece in enumerate(self.board_array[y]):
                if piece is not None:
                    if piece.color == side:
                        if piece.pClass == "pawn":
                            score += 1
                        elif piece.pClass == "tower":
                            score += 4
                        elif piece.pClass == "knight":
                            score += 3
                        elif piece.pClass == "bishop":
                            score += 4
                        elif piece.pClass == "queen":
                            score += 7
                        elif piece.pClass == "king":
                            score += 10
        if self.check[side]:
            score -= 10
        for key in self.check.keys():
            if key != side and self.check[key]:
                score += 10
        return score


class Bot:
    def __init__(self, difficulty, bot_side):
        self.difficulty = difficulty
        self.bot_side = bot_side

    def move(self, board, play_side):
        return self.think_move(self.difficulty, board.copy(), play_side)

    def think_move(self, difficulty, board, play_side):
        if play_side == "w":
            possible_moves = board.possible_moves("b")
        else:
            possible_moves = board.possible_moves("w")
        important_moves = possible_moves[:]
        best_move = None
        best_score = None
        if difficulty == -1:
            for move in tqdm(possible_moves):
                # print("Possible move: " + str(move))
                bot_move = move
                move_score = self.calculate_score(bot_move, board)
                new_board = board.copy()
                new_board.move_piece(bot_move[0], bot_move[1])
                pl_best_move = None
                pl_best_score = None
                for pl_move in board.possible_moves(play_side):
                    # print("Possible player move: " + str(pl_move))
                    pl_board = new_board.copy()
                    pl_board.move_piece(pl_move[0], pl_move[1])
                    pl_move_score = pl_board.score(play_side) - new_board.score(play_side)
                    if pl_best_move is None or move_score >= pl_best_score:
                        pl_best_score = pl_move_score
                        pl_best_move = pl_move
                bot_score = move_score - pl_best_score
                if best_score is None or bot_score >= best_score:
                    best_score = bot_score
                    best_move = bot_move
            return best_move
        else:
            move_scores = {}
            move_boards = {}
            best_pl_moves = {}
            for move in tqdm(possible_moves):
                bot_move = move
                move_score = self.calculate_score(bot_move, board)
                new_board = board.copy()
                new_board.move_piece(bot_move[0], bot_move[1])
                pl_best_move = None
                pl_best_score = None
                for pl_move in board.possible_moves(play_side):
                    pl_board = new_board.copy()
                    pl_board.move_piece(pl_move[0], pl_move[1])
                    pl_move_score = pl_board.score(play_side) - new_board.score(play_side)
                    if pl_best_move is None or move_score >= pl_best_score:
                        pl_best_score = pl_move_score
                        pl_best_move = pl_move
                bot_score = move_score - pl_best_score
                move_scores[str(move)] = bot_score
                move_boards[str(move)] = board.copy()
                move_boards[str(move)].move_piece(move[0], move[1])
                move_boards[str(move)].move_piece(pl_best_move[0], pl_best_move[1])
            while difficulty > 1:
                for move in tqdm(important_moves):
                    best_next_move = None
                    best_next_score = None
                    if play_side == "w":
                        possible_moves = move_boards[str(move)].possible_moves("b")
                    else:
                        possible_moves = move_boards[str(move)].possible_moves("w")
                    for move2 in possible_moves:
                        bot_move = move2
                        move_score = self.calculate_score(bot_move, move_boards[str(move)])
                        new_board = move_boards[str(move)].copy()
                        new_board.move_piece(bot_move[0], bot_move[1])
                        pl_best_move = None
                        pl_best_score = None
                        for pl_move in new_board.possible_moves(play_side):
                            pl_board = new_board.copy()
                            pl_board.move_piece(pl_move[0], pl_move[1])
                            pl_move_score = pl_board.score(play_side) - new_board.score(play_side)
                            if pl_best_move is None or pl_move_score >= pl_best_score:
                                pl_best_score = pl_move_score
                                pl_best_move = pl_move
                        best_pl_moves[str(move)] = pl_best_move
                        bot_score = move_score - pl_best_score
                        if best_next_score is None or bot_score >= best_next_score:
                            best_next_score = bot_score
                            best_next_move = move2
                    move_scores[str(move)] += best_next_score
                    move_boards[str(move)].move_piece(best_next_move[0], best_next_move[1])
                    move_boards[str(move)].move_piece(best_pl_moves[str(move)][0], best_pl_moves[str(move)][1])
                difficulty -= 1
            max_score = None
            max_move = None
            for move in important_moves:
                if max_score is None or move_scores[str(move)] > max_score:
                    max_score = move_scores[str(move)]
                    max_move = move
            return max_move

    def calculate_score(self, move, board):
        board_copy = board.copy()
        old_score = board.score(self.bot_side)
        board_copy.move_piece(move[0], move[1])
        new_score = board_copy.score(self.bot_side)
        return new_score - old_score


def setup_tiles():
    # print("Setting up tiles")
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:
                pygame.draw.rect(SCREEN, WHITE, pygame.Rect(i * 84, j * 84, 84, 84))
            else:
                pygame.draw.rect(SCREEN, BLACK, pygame.Rect(i * 84, j * 84, 84, 84))


def place_pieces():
    for ind, letter in enumerate("ABCDEFGH"):
        for piece in BOARD.board_array[letter]:
            if piece is not None:
                piece.draw()
    pygame.display.flip()


def setup_board():
    setup_tiles()
    place_pieces()
    pygame.display.flip()


def game_loop_2p():
    selected_piece = None
    side = True  # True -> White, False -> Black

    print("White pieces' turn")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                for y, letter in enumerate("ABCDEFGH"):
                    if pos[1] // 84 == y:
                        if selected_piece is None:
                            if side:
                                if BOARD.has_moves("w"):
                                    if BOARD.board_array[letter][pos[0] // 84] is not None and \
                                            BOARD.board_array[letter][pos[0] // 84].color == "w":
                                        selected_piece = (letter, pos[0] // 84)
                                        print("Selected piece: " + letter + " " + str(pos[0] // 84))
                                    else:
                                        print("Not a valid piece")
                                else:
                                    if BOARD.check["w"]:
                                        print("End of the game: BLACK wins!")
                                    else:
                                        print("End of the game: Stalemate")
                            else:
                                if BOARD.has_moves("b"):
                                    if BOARD.board_array[letter][pos[0] // 84] is not None and \
                                            BOARD.board_array[letter][pos[0] // 84].color == "b":
                                        selected_piece = (letter, pos[0] // 84)
                                        print("Selected piece: " + letter + " " + str(pos[0] // 84))
                                    else:
                                        print("Not a valid piece")
                                else:
                                    if BOARD.check["b"]:
                                        print("End of the game: WHITE wins!")
                                    else:
                                        print("End of the game: Stalemate")

                        else:
                            if BOARD.is_valid_move(selected_piece, (letter, pos[0] // 84)):
                                BOARD.move_piece(selected_piece, (letter, pos[0] // 84))
                                selected_piece = None
                                side = not side
                                if side:
                                    print("White pieces' turn")
                                else:
                                    print("Black pieces' turn")
                            # moure peça
                            else:
                                print("Invalid move")
                                selected_piece = None

        setup_board()


def game_loop_1p(difficulty, player_side):
    if player_side == "w":
        bot = Bot(difficulty, "b")
    else:
        bot = Bot(difficulty, "w")
    selected_piece = None
    side = player_side == "w"  # True -> Player, False -> Bot

    if side:
        print("Your turn...")
    else:
        print("Computer is moving...")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                if side:
                    pos = pygame.mouse.get_pos()
                    for y, letter in enumerate("ABCDEFGH"):
                        if pos[1] // 84 == y:
                            if selected_piece is None:
                                if BOARD.has_moves(player_side):
                                    if BOARD.board_array[letter][pos[0] // 84] is not None and \
                                            BOARD.board_array[letter][pos[0] // 84].color == player_side:
                                        selected_piece = (letter, pos[0] // 84)
                                        print("Selected piece: " + letter + " " + str(pos[0] // 84))
                                    else:
                                        print("Not a valid piece")
                                else:
                                    if BOARD.check["w"]:
                                        print("End of the game: BLACK wins!")
                                    else:
                                        print("End of the game: Stalemate")
                            else:
                                if BOARD.is_valid_move(selected_piece, (letter, pos[0] // 84)):
                                    BOARD.move_piece(selected_piece, (letter, pos[0] // 84))
                                    selected_piece = None
                                    side = not side
                                    print("Computer is moving...")
                                    # moure peça
                                else:
                                    print("Invalid move")
                                    selected_piece = None
        if player_side == "w":
            if not BOARD.has_moves("b"):
                print("Game ended")
        else:
            if not BOARD.has_moves("w"):
                print("Game ended")

        if not side:
            setup_board()
            bot_move = bot.move(BOARD, player_side)
            BOARD.move_piece(bot_move[0], bot_move[1])
            side = not side
            print("Your turn...")

        if not BOARD.has_moves(player_side):
            print("Game ended")

        setup_board()


if __name__ in "__main__":
    mode = 0
    sde = "w"
    for cn, arg in enumerate(sys.argv):
        if arg == "-1p":
            mode = 0
        elif arg == "-2p":
            mode = 1
        if arg == "-w":
            sde = "w"
        elif arg == "-b":
            sde = "b"
    BOARD = Board("BOARD", sde)
    if mode == 0:
        game_loop_1p(3, sde)
    else:
        game_loop_2p()
