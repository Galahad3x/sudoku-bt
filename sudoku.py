#!/usr/bin/python3

from time import sleep
import sys

SUDOKU_WIDTH = 0
SUDOKU_HEIGHT = 0
REGION_WIDTH = 0
REGION_HEIGHT = 0

def is_full(sudoku):
	for row in sudoku:
		for elem in row:
			if elem == 0:
				return False
	return True

def correct_rows(sudoku):
	for row in sudoku:
		elems = []
		for elem in row:
			if elem != 0:
				if elem in elems:
					#print("Rows: " + str(elem) + " in " + str(elems))
					return False
				if elem >= 1 and elem <= SUDOKU_WIDTH:
					elems.append(elem)
				else:
					#print("Rows: " + str(elem) + " out of range")
					return False
	return True

def correct_columns(sudoku):
	for j in range(SUDOKU_WIDTH):
		elems = []
		for i, row in enumerate(sudoku):
			if sudoku[i][j] != 0:
				if sudoku[i][j] in elems:
					#print("Cols: " + str(sudoku[i][j]) + " in " + str(elems))				
					return False
				if sudoku[i][j] >= 1 and sudoku[i][j] <= SUDOKU_HEIGHT:
					elems.append(sudoku[i][j])
				else:
					#print("Cols: " + str(sudoku[i][j]) + " out of range")
					return False
	return True

def correct_regions(sudoku):
	width_regions = int(SUDOKU_WIDTH // REGION_WIDTH)
	height_regions = int(SUDOKU_HEIGHT // REGION_HEIGHT)
	for hc in range(height_regions):
		for wc in range(width_regions):
			elems = []
			for row in range(REGION_HEIGHT):
				for elem in range(REGION_WIDTH):
					element = sudoku[hc*REGION_HEIGHT + row][wc*REGION_WIDTH + elem]
					if element != 0:
						if element in elems:
							#print("Regs: " + str(element) + " in " + str(elems))
							return False
						if element >= 1 and element <=(REGION_WIDTH*REGION_HEIGHT):
							elems.append(element)
						else:
							#print("Regs: " + str(element) + " out of range")
							return False
	return True					

def is_correct(sudoku):
	return correct_rows(sudoku) and correct_columns(sudoku) and correct_regions(sudoku)
	
def is_done(sudoku):
	return is_full(sudoku) and is_correct(sudoku)

def check_for_regions():
	if SUDOKU_WIDTH % REGION_WIDTH != 0:
		print("ERROR: Region and sudoku width aren't divisible")
		raise SystemExit
	if SUDOKU_HEIGHT % REGION_HEIGHT != 0:
		print("ERROR: Region and sudoku height aren't divisible")
		raise SystemExit


def read_input():
	global REGION_WIDTH, REGION_HEIGHT, SUDOKU_WIDTH, SUDOKU_HEIGHT
	first_row = input().split(" ")
	if len(first_row) != 2:
		print("ERROR: First line of input is wrong")
		raise SystemExit
	try:
		REGION_WIDTH = int(first_row[0])
		REGION_HEIGHT = int(first_row[1])
	except IndexError:
		print("ERROR: Missing region width and/or height")
		raise SystemExit
	sudoku = [[int(x) for x in input().split(" ")]]
	read_row = input()
	while read_row != "":
		new_row = [int(x) for x in read_row.split(" ")]
		if len(new_row) != len(sudoku[-1]):
			print("ERROR: Sudoku rows aren't the same size")
			raise SystemExit	
		else:
			sudoku.append(new_row)
			read_row = input()
	SUDOKU_WIDTH = len(sudoku[0])
	SUDOKU_HEIGHT = len(sudoku)
	return sudoku
	
def read_file(filename):
	global REGION_WIDTH, REGION_HEIGHT, SUDOKU_WIDTH, SUDOKU_HEIGHT
	with open(filename,"r") as f:
		first_row = f.readline().split(" ")
		if len(first_row) != 2:
			print("ERROR: First line of input is wrong")
			raise SystemExit
		try:
			REGION_WIDTH = int(first_row[0])
			REGION_HEIGHT = int(first_row[1])
		except IndexError:
			print("ERROR: Missing region width and/or height")
			raise SystemExit
		sudoku = [[int(x) for x in f.readline()[:-1].split(" ")]]
		read_row = f.readline()[:-1]
		while read_row != "":
			new_row = [int(x) for x in read_row.split(" ")]
			if len(new_row) != len(sudoku[-1]):
				print("ERROR: Sudoku rows aren't the same size")
				raise SystemExit	
			else:
				sudoku.append(new_row)
				read_row = f.readline()[:-1]
		SUDOKU_WIDTH = len(sudoku[0])
		SUDOKU_HEIGHT = len(sudoku)
		return sudoku


def prettify(sudoku):
	prettified = ""
	line_break = "|" + "|".join(["-------"]*3) + "|\n"
	for i, row in enumerate(sudoku):
		if i % REGION_HEIGHT == 0:
			prettified += line_break
		for j, elem in enumerate(row):
			if j % REGION_WIDTH == 0 and j != 0:
				prettified += " |"
			elif j % REGION_WIDTH == 0:
				prettified += "|"			
			prettified += " " + str(elem)
		prettified += " |\n"
	prettified += line_break
	return prettified[:-1]

def solve_sudoku(sudoku):
	# print("Solving:\n" + prettify(sudoku))
	if is_done(sudoku):
		return sudoku
	else:
		if is_full(sudoku):
			return False
		should_stop = False
		for i, row in enumerate(sudoku):
			for j, elem in enumerate(row):
				if elem == 0:
					first0_i, first0_j = i, j
					should_stop = True
					break
			if should_stop:
				break
		for possible_sol in range(REGION_WIDTH*REGION_HEIGHT):
			# print("Possible: ", possible_sol+1)
			new_sudoku = []
			for row in sudoku:
				new_sudoku.append(row[:])
			new_sudoku[first0_i][first0_j] = possible_sol+1
			print(prettify(new_sudoku))
			#dump = input()
			if is_correct(new_sudoku):
				solved = solve_sudoku(new_sudoku)
				if solved != False:
					return solved
		# print(prettify(sudoku) + "has no solution")
		return False
			
						
	

if __name__ == "__main__":
	if len(sys.argv) >= 2:
		sudoku = read_file(sys.argv[1])
	else:
		sudoku = read_input()
	check_for_regions()
	#print(prettify(sudoku))
	solved_sudoku = solve_sudoku(sudoku)
	print("\n\n\nSolved sudoku: ")
	print(prettify(solved_sudoku))
