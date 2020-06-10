#!/usr/bin/python3

import sys, pygame
from time import sleep

pygame.init()

SIZE = WIDTH, HEIGHT = 512, 512
BLACK = [100,100,100]
WHITE = [255,255,255]

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
		#self.image_route = "Images/" + pClass + ".png"
		image_route = "Images/ball.png"
		self.image = pygame.image.load(image_route).convert_alpha()
		self.image = pygame.transform.scale(self.image,(64,64))
		self.rectangle = self.image.get_rect()
		
	def draw(self):
		for y, letter in enumerate("ABCDEFGH"):
			if letter == self.up:
				self.rectangle.y = y*64
				self.rectangle.x = self.right*64
				SCREEN.blit(self.image,self.rectangle)
				break
			
		
	def update(self,new_coords):
		self.up, self.right = new_coords
		self.rectangle = self.image.get_rect()
		pass

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
		self.board_array = self.generate_board_array(player_side)
		

def setup_tiles():
	#print("Setting up tiles")
	for i in range(8):
		for j in range(8):
			if (i+j) % 2 == 0:
				pygame.draw.rect(SCREEN,WHITE,pygame.Rect(i*64,j*64,64,64))
			else:
				pygame.draw.rect(SCREEN,BLACK,pygame.Rect(i*64,j*64,64,64))
	pygame.display.flip()


def place_pieces():
	for ind, letter in enumerate("ABCDEFGH"):
		for piece in BOARD.board_array[letter]:
			if piece != None:
				piece.draw()


def setup_board():
	setup_tiles()
	place_pieces()


def move_piece(piece_coords,new_coords):
	if BOARD.board_array[piece_coords[0]][piece_coords[1]] != None:
		BOARD.board_array[piece_coords[0]][piece_coords[1]].update((new_coords[0],new_coords[1]))
	

def game_loop():
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
			
		#ballrect = ballrect.move([1,0])
		
		setup_board()
		#screen.blit(ball,ballrect)
		pygame.display.flip()
		sleep(2)
		move_piece(("G",3),("E",3))
		
if __name__ in "__main__":
	BOARD = Board("w")
	game_loop()
	
