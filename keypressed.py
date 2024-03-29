import config
import tkinter as tk
from findword import FindWord
from countpoints import *
import saveload

def KeyPressed(event, p1Turn, player1, player2, words, spaces, selected_space, right, infobox, callback, played, root):
	letters    = "abcdefghijklmnopqrstuvwxyz"
	keyPressed = event.keysym.lower()
	space      = spaces[selected_space[1]][selected_space[0]]
	obstructed = True # Assume that the typing is obstructed until it's proven otherwise

	if p1Turn: # Finding who's turn it is
		player = player1
	else:
		player = player2
############################################
# Playing a letter
	if keyPressed in letters: 
		
		selected = None
		for tile in player.GetRack(): # Checking if the letter is in the player's rack
			if tile.GetLetter().lower() == keyPressed:
				selected = tile 
				break
		if selected == None:
			callback(words, played)
			return None
			
		while obstructed: # Checking for tile obstructions
			if space.tile != None: 
				output = SelectNextSpace(spaces, right, selected_space) 
				if output == None: # If it can't select the next space, break out of the function
					callback(words, played)
					return None # Button bindings cannot return anything, this just signals to stop the function
				else: # Otherwise, update the selected space
					space = output
					selected_space = [int(space.coordinate[0]), int(space.coordinate[1])]
			else:
				obstructed = False

		space.PlayTile(selected) # Actually playing the tile
		played.append(selected)
		player.RemoveLetter(selected.GetLetter())
		infobox.UpdateText()
		
		new_words = CheckForWords(selected, spaces)
		words = UpdateWords(words, new_words)
		
		output = SelectNextSpace(spaces, right, selected_space) # Selecting the next space in direction
		if output == None:
			callback(words, played)
			return None
		else:
			space = output
			
############################################
# Removing a letter
	elif keyPressed == "backspace":
		if played != []:
			while space.tile not in played:
				output = SelectNextSpace(spaces, right, selected_space, True) # Select previous space
				if output == None:
					callback(words, played)
					return None
				else:
					space = output
					selected_space = [int(space.coordinate[0]), int(space.coordinate[1])]
			
			tile = space.tile
			space.tile = None # Remove space's record of tile
			player.AddLetter(tile) # Add tile back to player's rack
			
			if p1Turn: # Update tile's record of position
				tile.position = "1"
			else:
				tile.position = "2"
			
			played.pop(played.index(tile))
			space.UpdateButton() # Update space's button
			infobox.UpdateText() # Update infobox 		
			

############################################
# Attempt to finish word
	elif keyPressed == "return":
		for word in words:
			if FindWord(word) == False:
				print(f"Word '{word.upper()}' not able to be played")
				return None

		print(f"Word '{words[0].upper()}' played")
		player.AddPoints(CountPoints(played, spaces))
		if len(words) > 1: #prevents double counting words when there are no crosswords
			for word in words[:len(words)-1]: # Iterate through each word other than the main word
				player.AddPoints(CountPoints(None, None, word))			
		played = []
		words  = []
		
		infobox.SwapTurn(spaces)

		if not infobox.p1Turn:
			infobox.player2.FindMove(spaces, infobox, root)
			
			
	
############################################
# Arrow key controls
	elif keyPressed in ["up", "down", "left", "right"]:
		if keyPressed   == "up":    SelectNextSpace(spaces, False, selected_space, True, True, True)
		elif keyPressed == "down":  SelectNextSpace(spaces, False, selected_space, False, True, True)
		elif keyPressed == "left":  SelectNextSpace(spaces, True, selected_space, True, True, True)
		elif keyPressed == "right": SelectNextSpace(spaces, True, selected_space, False, True, True)
		played = []
		words = []

############################################
		
	callback(words, played)
	return None

############################################
# Selecting adjacent spaces
def SelectNextSpace(spaces, right, selected_space, prev = False, manual = False, loop = False):
	if prev: # Lets the function also select the previous space (function generalisation)
		prev = -1
	else:
		prev = 1

	if loop: # Allows looping around the grid, used for arrow keys
		if right:
			space = spaces[selected_space[1]][(selected_space[0]+prev)%config.num_tiles]
			space.SelectSpace(manual)
			return space
		else:
			space = spaces[(selected_space[1]+prev)%config.num_tiles][selected_space[0]]
			space.SelectSpace(manual)
			return space
	
	if right:
		try:
			space = spaces[selected_space[1]][selected_space[0]+prev]
			space.SelectSpace(manual)
			return space
		except:
			return None
	else:
		try:
			space = spaces[selected_space[1]+prev][selected_space[0]]
			space.SelectSpace(manual)
			return space
		except:
			return None

############################################
# Finding all words made (Includes cross words)
def CheckForWords(tile, spaces):
	coords     = [tile.position[0],tile.position[1]]
	words      = []

	for right in [[1,0], [0,1]]: # Check both left and down
		for dir in [1,-1]: # Check both forward and back
			end = False
			pointer = [int(coords[0]), int(coords[1])] # Point to next tile in direction
			wordstring = f"{tile.GetLetter()}"
			while not end:
				pointer = [pointer[0]+right[0]*dir, pointer[1]+right[1]*dir]
				leftright = pointer[0]>=config.num_tiles or pointer[0]<0 # Checking if it's crossed the left or right edges
				topbottom = pointer[1]>=config.num_tiles or pointer[1]<0
				if leftright or topbottom:
					end = True
					break
				
				if spaces[pointer[1]][pointer[0]].tile != None: # If this next tile isn't empty
					if dir == 1: # If itss going forward
						wordstring += spaces[pointer[1]][pointer[0]].tile.GetLetter() # Add it to the end of the string
					else: # If it's going backwards
						wordstring  = spaces[pointer[1]][pointer[0]].tile.GetLetter() + wordstring # Add it to the beginning
				else:
					end = True # Break the loop, it's found the end
					
			if len(wordstring)>1: words.append(wordstring)

	return words

def UpdateWords(words,newWords): # Given the new words found, return what the new word list should be
	if len(newWords) == 2: # Can only ever detect two max words from one tile, left-right and up-down word
		start = words[:(len(words)-1)]+[newWords[0]] # Add the new word detected to the first part of the words array
		end = [newWords[1]] # The main word being typed
		words = start + end
			
	elif len(newWords) == 1: # If only one word was found
		if len(words) != 0: # Only used at the beginning when the list is empty
			words[len(words)-1] = newWords[0]
		else:
			return newWords

	return words