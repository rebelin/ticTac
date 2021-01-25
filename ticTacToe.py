# Rebecca Lin
# 5/19/17

import random

def valid_char(p): 
	""" Takes in an integer representing the player, asks for a character, and tells if the input is a valid character - asks again if it isn't. """
	
	validChar = False
			
	while validChar != True: # The loop will continue until a valid character input is entered
		char = input("Player {}, please enter your character: ".format(p))
		
		if ord(char) in characters: 
			characters.remove(ord(char)) # The list is immutable, so this makes sure the character isn't reused
			validChar = True # This ends the loop
			return char	
		else:
			print("That character is not valid. Please enter a different one. (No numbers!)")

def init_grid(n):
	""" Creates and returns a nxn grid of integers. """
	
	num = [] 
	grid = []

	for i in range(n * n): # Creates a list of numbers that will be added into the grid
		num.append(i)
	
	for i in range(n): 
		grid.append(num[:n])
		num = num[n:] # This splices the list of numbers, so that the used numbers aren't reused
	return grid

def greatest(board):
	""" Takes in a 2Dlist and returns the greatest number in the 2Dlist. """
	
	largest = 0
	for row in board:
		for item in row:
			if len(str(item)) > largest: # Takes the length of each item in the list and compares it to largest 
				largest = len(str(item))
	return largest
		
def print_grid(board, n):
	""" Takes in a 2D grid and its dimension(s), and prints it nicely. """
	
	last = greatest(board) 
	print(("--" + "-" * last + "-") * n + "-") # This is to line the horizontal borders nicely with the grid
	for row in board:
		for item in row:
			if len(str(item)) < last:
				print("| {}{}".format(item, " " * (last - len(str(item))), end = " ")
			else:
				print("| {}".format(item), end = " ") # end = " " prevents a newline after the print; it instead ends each print statement with a space
		print("|\n" + ("--" + "-" * last + "-") * n + "-") # Prints a "|" and new line of horizontal border after the row is done.

def who_is_first(): # Randomly determine who goes first
	""" Takes no parameters, gets a random float, and returns a boolean. """
	
	if random.random() < 0.5:
		return True
	else:
		return False
	
def valid_cell_num(p, board): # p indicates the player
	""" Takes in an integer representing the player and a list, asks for an integer, and tells if the input is a valid cell number - asks again if it isn't. """
	
	validNum = False
	dim = len(board) 
	
	while validNum != True: # The loop will continue until a valid integer/cell input is entered
		num = input("Player {}, please choose a cell number: ".format(p))
		try: 
			num = int(num)
			if num >= dim * dim: # Any number that isn't in the grid is invalid
				print("That cell doesn't exist. Please pick an available cell number.")
			else:
				validNum = True # This ends the loop
				return num		
		except ValueError: 
			print("That's not a number. Try again.")
	
def check_cell(cell, board): 
	""" Takes in a list and an integer, checks if the coordinate in the list is an integer, returns a boolean. """
	
	dim = len(board)
	row = cell // dim
	column = cell % dim
	
	if	type(board[row][column]) == int:
		return True
	else:
		return False
	
def check_rows(board, char):
	""" Checks whether any row in the board is homogeneous with the character and returns the result. """
	
	for row in board:
		if check_row(row, char):
			return True
		#else:
			#return False won't check the other rows
	
	# If it makes it through/past the loop, no rows are homogeneous
	return False		
	
def check_row(row, char):
	""" Takes a list of bools, and returns whether the list is homogeneous with the character. """
	
	for item in row:
		if item != char:
			return False
	
	# If we made it all the way through, then they were all the same
	return True

def check_columns(board, char):
	""" Takes in a list, checks whether any column in the nxn board is homogeneous with the character and returns a boolean. """

	dim = len(board)
	answer = False  
	n = 0 # counter
	
	while answer == False and n == 0: # Both conditions need to be met to loop
		for column in range(dim):
			test = True
			value = board[0][column]
			for row in board:
				if value != row[column]:
					test = False
			if test == True:
				answer = True # Ends Loop
			else:
				n += 1

	return answer	
		
def check_diagonals(board, char):
	""" Takes a list and a character, returns whether either diagonal is homogeneous with the character. """
	
	dim = len(board)
	answer = True
	for i in range(dim):
		if board[i][i] != char: # First diagonal
			answer = False
			
	for i in range(dim):	
		if board[i][2 - i] != char: # This is the other diagonal
			return False or answer # If answer is True, return True
	return True

def check_fill(board): # This is to check for a tie (when all cells are used, but no one wins)
	""" Takes in a list and returns whether the items in the list are all characters (no integers). """
	
	for row in board: 
		for item in row:
			if type(item) == int:	
				return False
	return True	

def check_win(board, char): 
	""" Takes in a list and a character, returns True if one of the conditions is True. """
	
	return check_rows(board, char) or check_columns(board, char) or check_diagonals(board, char)
	
def switch_players(currentPlayer):
	""" Takes in a character, creates a 2-tuple that changes and sets the character and number, respectively, and returns a 2-tuple. """
	
	if currentPlayer == p1:
		currentPlayer, num = p2, 2
	elif currentPlayer == p2:
		currentPlayer, num = p1, 1
	return currentPlayer, num

def player_move(p, char, cell, grid):  
	""" Takes in a integer that indicates the player, a character, an integer, and a list, replaces the integer in the grid with the character - asks again if there is already a character, and returns the new grid. """
	
	dim = len(grid)	
	row = cell // dim # Use integer division to get the row number
	column = cell % dim # Use modulation (the remainder) to get the column number
		
	if check_cell(cell, grid) == True:
		grid[row][column] = char # Sets/Changes the coordinate in the grid to the character
		return print_grid(grid, dim) # Lists are mutable, so when the value is set to the character, the character will stay as is in the grid
	else:	
		print("That cell has already been used. Try again.")
		player_move(p, char, valid_cell_num(p, grid), grid)
	
def gameplay(board, player, num): # player represents the character of whoever went first
	""" Takes in a list, a character, and an integer representing the player, and prints the result. """
	
	win = False
	while win != True and check_fill(board) != True: # Loop will end once one of the conditions equals True
		player, num = switch_players(player)
		player_move(num, player, valid_cell_num(num, board), board)
		if check_win(board, player) == True:
			print("Player {} wins!".format(num))
			win = True
		elif check_win(board, switch_players(player)[0]) == True: # Since switch_players() returns a tuple, [] indicate the place value in the tuple, like it would a list 
			print("Player {} wins!".format(switch_players(player)[1]))
			win = True
		elif check_fill(board) == True:
			print("It's a tie")
			
######## Main Program ########
	
print('Welcome to "Tic-Tac-Toe" game\n')

# Board size option
size = int(input("What size (square) grid would you like? "))
print("\nHere's what it looks like:")
board = init_grid(size)
print_grid(board, size)

print("\nEach player: choose a different character to use as a marker.")

characters = [] # This excludes numbers, so that the character the player chooses isn't a number
for i in range(33, 48):
	characters.append(i)
for i in range(58, 127):
	characters.append(i)
		
p1 = valid_char(1)
p2 = valid_char(2)
print()

first = who_is_first()
	
if first == True: # Determines who goes first
	print("Player 1 goes first.")
	player_move(1, p1, valid_cell_num(1, board), board)
	gameplay(board, p1, 1)
else:
	print("Player 2 goes first.")
	player_move(2, p2, valid_cell_num(2, board), board)
	gameplay(board, p2, 2)
