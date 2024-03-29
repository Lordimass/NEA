import tkinter as tk
import csv

###########################
# Imports
import config
import dependents
import saveload
from Classes.Space     import *
from Classes.Tile      import *
from Classes.Indicator import *
from Classes.Player    import *
from Classes.Infobox   import *
from Classes.Pass      import *
from keypressed		   import *

###########################
# Variable Definitions
centre         = round(config.num_tiles/2)-1
selected_space = [centre, centre]
right          = True
words          = []
playedlist     = []

###########################
# Window Setup
root = tk.Tk()

screen_size   = (root.winfo_screenwidth(), root.winfo_screenheight())
screen_buffer = dependents.screen_buffer(config.screen_buffer_percent, screen_size)
win_size      = (screen_size[0]-screen_buffer[0], screen_size[1]-screen_buffer[1])
win_buffer    = dependents.win_buffer(config.win_buffer_percent, win_size)
tile_size     = dependents.tile_size(win_size, win_buffer, config.num_tiles)
info_pos      = dependents.info_pos(win_size, win_buffer, tile_size, config.num_tiles)
info_size     = dependents.info_size(win_size, win_buffer, info_pos)
pass_pos	  = dependents.pass_pos(info_pos, info_size)
pass_size     = dependents.pass_size(info_size, win_buffer, win_size, pass_pos)

root.title    ("Scrabble NEA - Sam Knight")
root.geometry (f"{win_size[0]}x{win_size[1]}")
root.resizable(config.resizable[0], config.resizable[1])
root.configure(bg = config.background_colour)

###########################
# Functions and Subroutine Definitions
def SelectSpace(coordinate, manual = False):
	#############
	# Handling indicators and selecting new space
	global selected_space
	last_space = spaces[selected_space[1]][selected_space[0]]
	if last_space.indicators != None:
		for indicator in last_space.indicators:
			indicator.button.destroy()
		last_space.indicators = None	
	selected_space = [int(coordinate[0]), int(coordinate[1])]
	
	#############
	# Removing old tiles
	if manual: # Only runs this if the user clicked another space, not automatically when typing
		global wordstring
		global playedlist
		global words
		wordstring = ""
		words = []
		
		if infobox.p1Turn == True:
			player = player1
			playernum = "1"
		else:
			player = player2
			playernum = "2"
			
		for tile in playedlist: # For every tile that got placed
			print(f"Tile ({tile.GetLetter()}) removed at [{int(tile.position[1])}, {int(tile.position[0])}]")
			space = spaces[int(tile.position[1])][int(tile.position[0])]
			space.tile = None # Remove from space
			player.AddLetter(tile) # Add back to player's rack
			tile.position = playernum # Update tile's attribute
			space.UpdateButton() # Update the button to represent the tile removal
			
		playedlist = [] # Clear the list
		infobox.UpdateText() # Update the infobox to represent the rack change
			
		

def ChangeDirection(new_right):
	global right
	right = new_right
	spaces[selected_space[1]][selected_space[0]].SelectSpace(True) #Reselect space
	

def InstantiateSpaces(tile_size, win_buffer, multipliers, ButtonCallback = SelectSpace):
	spaces = [[]]
	for row in range(0, config.num_tiles):
		for column in range(0, config.num_tiles):
			space = Space(f"{column}{row}", multipliers[column][row],
						  tile_size, win_buffer, ButtonCallback, ChangeDirection)
			spaces[row].append(space)
		spaces.append([])
		
	spaces.pop(len(spaces)-1)
	return spaces

def LoadMultipliers(num_tiles):
	multipliers = []
	loaded = False
	try:
		file = open(f"multiplierpos{num_tiles}.csv", "r")
		loaded = True
	except:
		print(f"Failed to load file multiplierpos{num_tiles}.csv, using a blank grid instead")
	if loaded:
		reader = csv.reader(file)
		for line in reader:
			row = []
			for i in line: # Converting "None" strings into None type
				if i == "None":
					row.append(None)
				else:
					row.append(i)
			multipliers.append(row)
		file.close
	else: # Allowing for grid sizes with no defined multipliers
		for column in range(num_tiles):
			multipliers.append([])
			for row in range(num_tiles):
				multipliers[column].append(None)

	return multipliers

def SetLetterDists(num_tiles):
	standard_dists = {}
	file = open("standardletterdistribtion.csv", "r")
	reader = csv.reader(file)
	for line in reader:
		standard_dists[line[0]] = [line[1], line[2]]

	multiplier = num_tiles/15
	new_dists = {}
	for letter in standard_dists:
		quantity = round(int(standard_dists[letter][0])*multiplier)
		if quantity <= 0: #To prevent some rarer letters from not being included at all
			quantity = 1
		new_dists[letter] = [quantity, standard_dists[letter][1]]
		
	return new_dists

def InstantiateTiles(letter_dists):
	bag = []
	for letter in letter_dists:
		for i in range(letter_dists[letter][0]):
			bag.append(Tile(letter, int(letter_dists[letter][1])))
	return bag

def DrawLetters(player1, player2, bag, infobox):
	player1.DrawLetters(bag)
	player2.DrawLetters(bag)
	infobox.UpdateText()

def KeyPressedCallback(returned_words, returned_playedlist):
	global words
	global playedlist
	words = returned_words
	playedlist = returned_playedlist
	print(words)
	
###########################
# Setup
multipliers = LoadMultipliers(config.num_tiles)
spaces      = InstantiateSpaces(tile_size, win_buffer, multipliers)
new_dists   = SetLetterDists(config.num_tiles)
bag         = InstantiateTiles(new_dists)
player1     = Player(True)
player2     = Player(False, True)
infobox     = Infobox(player1, player2, bag, info_pos, info_size)
pass_obj    = Pass(pass_pos, pass_size, infobox, spaces)

if config.game_index != -1:
	saveload.loadGame(config.game_index, spaces, infobox)

DrawLetters(player1, player2, bag, infobox)
spaces[selected_space[0]][selected_space[1]].SelectSpace()

root.bind("<Key>", lambda event:KeyPressed(event, infobox.p1Turn, player1, player2,
										   words, spaces, selected_space, right, infobox,
										   KeyPressedCallback, playedlist, root))
