#!/usr/bin/python3

import sys, pygame
from time import sleep

pygame.init()

SIZE = WIDTH, HEIGHT = 672, 672
BLACK = [100,100,100]
WHITE = [255,255,255]
RED = [255,0,0]

SCREEN = pygame.display.set_mode(SIZE)

#ball = pygame.image.load("Images/basket.png")
#ball = pygame.transform.scale(ball,(64,64))
#ballrect = ball.get_rect()

class Piece:
	def __init__(self,color,pClass,coords):
		self.color = color # "b" or "w"
		self.pClass = pClass #"pawn","tower","knight","bishop","queen","king"
		self.hasMoved = False
		self.up, self.right = coords
		image_route = "Images/" + color + "" + pClass + ".png"
		#image_route = "Images/ball.png"
		self.image = pygame.image.load(image_route).convert_alpha()
		self.image = pygame.transform.scale(self.image,(64,64))
		self.rectangle = self.image.get_rect()
		
	def draw(self):
		for y, letter in enumerate("ABCDEFGH"):
			if letter == self.up:
				self.rectangle.y = y*84 + 10
				self.rectangle.x = self.right*84 + 10
				SCREEN.blit(self.image,self.rectangle)
				break
			
		
	def update(self,new_coords):
		self.hasMoved = True
		self.up, self.right = new_coords
		self.rectangle = self.image.get_rect()
		for y, letter in enumerate("ABCDEFGH"):
			if letter == self.up:
				self.rectangle.y = y*84 + 10
				self.rectangle.x = self.right*84 + 10
				break
		
	def copy(self):
		return Piece(self.color,self.pClass,self.coords)

class Board:
	def generate_board_array(self,player_side):
		if player_side.startswith("w"):
			b_array = {}
			for letter in "ABCDEFGH":
				b_array[letter] = []
				if letter == "A":
					b_array[letter].append(Piece("b","tower",(letter,0)))
					b_array[letter].append(Piece("b","knight",(letter,1)))
					b_array[letter].append(Piece("b","bishop",(letter,2)))
					b_array[letter].append(Piece("b","queen",(letter,3)))
					b_array[letter].append(Piece("b","king",(letter,4)))
					b_array[letter].append(Piece("b","bishop",(letter,5)))
					b_array[letter].append(Piece("b","knight",(letter,6)))
					b_array[letter].append(Piece("b","tower",(letter,7)))
				elif letter == "B":
					for ind in range(8):
						b_array[letter].append(Piece("b","pawn",(letter,ind)))
				elif letter == "G":
					for ind in range(8):
						b_array[letter].append(Piece("w","pawn",(letter,ind)))
				elif letter == "H":
					b_array[letter].append(Piece("w","tower",(letter,0)))
					b_array[letter].append(Piece("w","knight",(letter,1)))
					b_array[letter].append(Piece("w","bishop",(letter,2)))
					b_array[letter].append(Piece("w","queen",(letter,3)))
					b_array[letter].append(Piece("w","king",(letter,4)))
					b_array[letter].append(Piece("w","bishop",(letter,5)))
					b_array[letter].append(Piece("w","knight",(letter,6)))
					b_array[letter].append(Piece("w","tower",(letter,7)))
				else:
					for ind in range(8):
						b_array[letter].append(None)
		elif player_side.startswith("b"):
			b_array = {}
			for letter in "ABCDEFGH":
				b_array[letter] = []
				if letter == "A":
					b_array[letter].append(Piece("w","tower",(letter,0)))
					b_array[letter].append(Piece("w","knight",(letter,1)))
					b_array[letter].append(Piece("w","bishop",(letter,2)))
					b_array[letter].append(Piece("w","queen",(letter,3)))
					b_array[letter].append(Piece("w","king",(letter,4)))
					b_array[letter].append(Piece("w","bishop",(letter,5)))
					b_array[letter].append(Piece("w","knight",(letter,6)))
					b_array[letter].append(Piece("w","tower",(letter,7)))
				elif letter == "B":
					for ind in range(8):
						b_array[letter].append(Piece("w","pawn",(letter,ind)))
				elif letter == "G":
					for ind in range(8):
						b_array[letter].append(Piece("b","pawn",(letter,ind)))
				elif letter == "H":
					b_array[letter].append(Piece("b","tower",(letter,0)))
					b_array[letter].append(Piece("b","knight",(letter,1)))
					b_array[letter].append(Piece("b","bishop",(letter,2)))
					b_array[letter].append(Piece("b","queen",(letter,3)))
					b_array[letter].append(Piece("b","king",(letter,4)))
					b_array[letter].append(Piece("b","bishop",(letter,5)))
					b_array[letter].append(Piece("b","knight",(letter,6)))
					b_array[letter].append(Piece("b","tower",(letter,7)))
				else:
					for ind in range(8):
						b_array[letter].append(None)
		return b_array

	def __init__(self,player_side):
		self.player_side = player_side
		self.board_array = self.generate_board_array(player_side)
		
	def copy(self):
		new_barray = {}
		for letter in "ABCDEFGH":
			new_barray[letter] = []
			for piece in self.board_array[letter]:
				new_barray[letter].append(piece.copy())
		return new_barray
		
	def move_piece(self,piece_coords,new_coords):
		print("Moved piece " + str(piece_coords) + " to " + str(new_coords))
		if self.board_array[piece_coords[0]][piece_coords[1]] != None:
			self.board_array[piece_coords[0]][piece_coords[1]].update((new_coords[0],new_coords[1]))
			self.board_array[new_coords[0]][new_coords[1]] = self.board_array[piece_coords[0]][piece_coords[1]]
			self.board_array[piece_coords[0]][piece_coords[1]] = None
		place_pieces()
	
	def is_valid_move(self,from_coords,to_coords):
		piece_from = self.board_array[from_coords[0]][from_coords[1]]
		piece_to = self.board_array[to_coords[0]][to_coords[1]]
		print("Attempting to move " + str(from_coords) + " to " + str(to_coords))
		if piece_from == None:
			return False
		if piece_to != None:
			if piece_to.color == piece_from.color:
				return False
			elif piece_to.pClass == "king":
				return False
		if piece_from.pClass == "pawn":
				for y, letter in enumerate("ABCDEFGH"):
					if not piece_from.hasMoved:
						if self.player_side == piece_from.color and piece_from.up == letter:
							if y >= 2 and to_coords[0] == "ABCDEFGH"[y-2] and \
								self.board_array["ABCDEFGH"[y-1]][to_coords[1]] == None and \
								self.board_array["ABCDEFGH"[y-2]][to_coords[1]] == None:
								return True
						elif self.player_side != piece_from.color and \
							piece_from.up == letter and to_coords[0] == "ABCDEFGH__"[y+2] and \
							self.board_array["ABCDEFGH_"[y+1]][to_coords[1]] == None and \
							self.board_array["ABCDEFGH"[y+2]][to_coords[1]] == None:
							return True	
					if y >= 1 and self.player_side == piece_from.color and \
						piece_from.up == letter and to_coords[0] == "ABCDEFGH"[y-1] and \
						to_coords[1] == from_coords[1] and \
						self.board_array[to_coords[0]][to_coords[1]] == None:
						return True
					elif self.player_side != piece_from.color and \
						piece_from.up == letter and to_coords[0] == "ABCDEFGH_"[y+1] and \
						to_coords[1] == from_coords[1] and \
						self.board_array[to_coords[0]][to_coords[1]] == None:
						return True
					if y >= 1 and self.player_side == piece_from.color and \
						piece_from.up == letter and to_coords[0] == "ABCDEFGH"[y-1] and \
						self.board_array[to_coords[0]][to_coords[1]] != None and \
						abs(to_coords[1]-from_coords[1]) == 1:
						return True
					elif self.player_side != piece_from.color and \
						piece_from.up == letter and \
						to_coords[0] == "ABCDEFGH_"[y+1] and to_coords[1] == from_coords[1] and \
						self.board_array[to_coords[0]][to_coords[1]] != None and \
						abs(to_coords[1]-from_coords[1]) == 1:
						return True
				return False
		elif piece_from.pClass == "tower":
			if to_coords[0] == from_coords[0]:
				for elem in range(min(from_coords[1],to_coords[1])+1,max(from_coords[1],to_coords[1])): 
					if self.board_array[to_coords[0]][elem] != None:
						return False
				return True
			elif to_coords[1] == from_coords[1]:
				for elem in "ABCDEFGH"["ABCDEFGH".find(min(from_coords[0],to_coords[0]))+1:"ABCDEFGH".find(max(from_coords[0],to_coords[0]))]:
					if self.board_array[elem][to_coords[1]] != None:
						return False
				return True
			else:
				return False
		elif piece_from.pClass == "knight":
			for y, letter in enumerate("ABCDEFGH"):
				if piece_from.up == letter:
					if to_coords[0] == "ABCDEFGH__"[y + 2] or (y >= 2 and to_coords[0] == "ABCDEFGH"[y - 2]):
						if to_coords[1] == from_coords[1]+1 or to_coords[1] == from_coords[1]-1:
							return True
					elif to_coords[0] == "ABCDEFGH_"[y + 1] or (y >= 1 and to_coords[0] == "ABCDEFGH"[y - 1]):
						if to_coords[1] == from_coords[1]+2 or to_coords[1] == from_coords[1]-2:
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
			for i in range(1,8):
				if top_left:
					if (lett_ind-i) >= 0 and (left-i) >= 0 and \
						"ABCDEFGH"[lett_ind-i] == to_coords[0] and (left-i) == to_coords[1]:
						return True
				if bot_right:
					if (lett_ind+i) < 8 and (left+i) < 8 and \
						"ABCDEFGH"[lett_ind+i] == to_coords[0] and (left+i) == to_coords[1]:
						return True
				if top_right:
					if (lett_ind-i) >= 0 and (left+i) < 8 and \
						"ABCDEFGH"[lett_ind-i] == to_coords[0] and (left+i) == to_coords[1]:
						return True
				if bot_left:
					if (lett_ind+i) < 8 and (left-i) >= 0 and \
						"ABCDEFGH"[lett_ind+i] == to_coords[0] and (left-i) == to_coords[1]:
						return True
				if (lett_ind-i) >= 0 and (left-i) >= 0 and self.board_array["ABCDEFGH"[lett_ind-i]][left-i] != None:
					top_left = False
				if (lett_ind-i) >= 0 and (left+i) < 8 and self.board_array["ABCDEFGH"[lett_ind-i]][left+i] != None:
					top_right = False
				if (lett_ind+i) < 8 and (left-i) >= 0 and self.board_array["ABCDEFGH"[lett_ind+i]][left-i] != None:
					bot_left = False
				if (lett_ind+i) < 8 and (left+i) < 8 and self.board_array["ABCDEFGH"[lett_ind+i]][left+i] != None:
					bot_right = False
			return False
		elif piece_from.pClass == "queen":
			if to_coords[0] == from_coords[0]:
				for elem in range(min(from_coords[1],to_coords[1])+1,max(from_coords[1],to_coords[1])): 
					if self.board_array[to_coords[0]][elem] != None:
						return False
				return True
			elif to_coords[1] == from_coords[1]:
				for elem in "ABCDEFGH"["ABCDEFGH".find(min(from_coords[0],to_coords[0]))+1:"ABCDEFGH".find(max(from_coords[0],to_coords[0]))]:
					if self.board_array[elem][to_coords[1]] != None:
						return False
				return True
			left = piece_from.right
			lett_ind = 0
			to_ind = 0
			for y, letter in enumerate("ABCDEFGH"):
				if piece_from.up == letter:
					lett_ind = y
				if letter == to_coords[0]:
					to_ind = y
			for i in range(1,8):
				if top_left:
					if (lett_ind-i) >= 0 and (left-i) >= 0 and \
						"ABCDEFGH"[lett_ind-i] == to_coords[0] and (left-i) == to_coords[1]:
						return True
				if bot_right:
					if (lett_ind+i) < 8 and (left+i) < 8 and \
						"ABCDEFGH"[lett_ind+i] == to_coords[0] and (left+i) == to_coords[1]:
						return True
				if top_right:
					if (lett_ind-i) >= 0 and (left+i) < 8 and \
						"ABCDEFGH"[lett_ind-i] == to_coords[0] and (left+i) == to_coords[1]:
						return True
				if bot_left:
					if (lett_ind+i) < 8 and (left-i) >= 0 and \
						"ABCDEFGH"[lett_ind+i] == to_coords[0] and (left-i) == to_coords[1]:
						return True
				if (lett_ind-i) >= 0 and (left-i) >= 0 and self.board_array["ABCDEFGH"[lett_ind-i]][left-i] != None:
					top_left = False
				if (lett_ind-i) >= 0 and (left+i) < 8 and self.board_array["ABCDEFGH"[lett_ind-i]][left+i] != None:
					top_right = False
				if (lett_ind+i) < 8 and (left-i) >= 0 and self.board_array["ABCDEFGH"[lett_ind+i]][left-i] != None:
					bot_left = False
				if (lett_ind+i) < 8 and (left+i) < 8 and self.board_array["ABCDEFGH"[lett_ind+i]][left+i] != None:
					bot_right = False
			return False
		elif piece_from.pClass == "king":
			return (abs(ord(from_coords[0]) - ord(to_coords[0])) + abs(from_coords[1] - to_coords[1])) == 1
		else:
			return False
			
	
	def print_state(self):	
		for letter in "ABCDEFGH":
			print(letter,end=": ")
			for piece in self.board_array[letter]:
				if piece != None:
					print(piece.color,piece.pClass,"\t",piece.right,end=" ")
				else:
					print("None", end=" ")
			print()
	

def setup_tiles():
	#print("Setting up tiles")
	for i in range(8):
		for j in range(8):
			if (i+j) % 2 == 0:
				pygame.draw.rect(SCREEN,WHITE,pygame.Rect(i*84,j*84,84,84))
			else:
				pygame.draw.rect(SCREEN,BLACK,pygame.Rect(i*84,j*84,84,84))
	


def place_pieces():
	for ind, letter in enumerate("ABCDEFGH"):
		for piece in BOARD.board_array[letter]:
			if piece != None:
				piece.draw()
	pygame.display.flip()


def setup_board():
	setup_tiles()
	place_pieces()
	pygame.display.flip()
	

def game_loop():
	selected_piece = None
	
	while True:
		sleep(0.1)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONUP:
				pos = pygame.mouse.get_pos()
				
				for y, letter in enumerate("ABCDEFGH"):
					if pos[1] // 84 == y:
						if selected_piece == None:
							selected_piece = (letter, pos[0]//84)
							print("Selected piece: " + letter + " " + str(pos[0]//84))
						else:
							if BOARD.is_valid_move(selected_piece, (letter, pos[0]//84)):
								BOARD.move_piece(selected_piece,(letter, pos[0]//84))
								selected_piece = None
								#moure peça
							else:
								print("Invalid move")
								selected_piece = None
								

		setup_board()
		
if __name__ in "__main__":
	BOARD = Board("w")
	game_loop()
	
