import csv
from Classes.Tile import *
import time # TEMP

def saveGame(board, infobox):
	game = []
	for y in board: # Saving tiles currently on the board
		for x in y:
			tile = x.tile
			if tile != None:
				game.append(f"{x.coordinate}{tile.GetLetter()}") # coordinate of space followed by letter, for example "33A"

	
	for tile in [infobox.player1, infobox.player2]: # All the tiles on player racks
		letters = ""
		for tile in tile.GetRack():
			letters += tile.GetLetter()
		game.append(letters)

	letters = ""
	for tile in infobox.bag: # All the tiles left in the bag
		letters += tile.GetLetter()
	game.append(letters)
		
	game.append(infobox.player1.GetPoints())
	game.append(infobox.player2.GetPoints())
	game.append(infobox.p1Turn)

	with open("AI/games.csv", "a") as gamesFile:
		writer = csv.writer(gamesFile)
		writer.writerow(game)



def loadGame(index, board, infobox, root = None):
	for row in board:
		for space in row:
			space.tile = None
			space.UpdateButton()
		
	f = open("AI/games.csv", "r")
	gamesFile = list(csv.reader(f))
	print(f"Loading game #{index}")

	if index <= -2: # loading most recent game
		game = gamesFile[len(gamesFile)-1]
	else: # loading given game
		game = gamesFile[index-1]
		
	del gamesFile # conserving memory by removing the potentially very memory hungry variable
	f.close() # same reason as above
	
	letterVals = {} # Loading letter vals into a dictionary for tile instantiation
	f = open("standardletterdistribtion.csv", "r")
	letters = list(csv.reader(f))
	for letter in letters:
		letterVals[letter[0]] = int(letter[2])

	count = 0
	for i in game: # For each element of the saved game
		if len(i) == 3 and isInt(i[0]): #If it's an encoded tile to be placed
			tile = Tile(i[2], letterVals[i[2]]) # Create tile object
			board[int(i[1])][int(i[0])].PlayTile(tile) # Place the tile on the board
			count+=1
		else: # if it's not a tile
			break # break out of the loop, there are no more tiles

	infobox.player1.ClearRack()
	infobox.player2.ClearRack()
	infobox.bag = []

	for player in [infobox.player1, infobox.player2]:
		for letter in game[count]:
			tile = Tile(letter, letterVals[letter])
			player.AddLetter(tile)
		count += 1

	for letter in game[count]:
		tile = Tile(letter, letterVals[letter])
		infobox.bag.append(tile)
	count += 1

	infobox.player1.SetPoints(int(game[count]))
	infobox.player2.SetPoints(int(game[count+1]))

	if game[count+2] == "False":
		game[count+2] = False
	
	if not(bool(game[count+2])) and infobox.p1Turn:
		infobox.SwapTurn(board, False)
	if bool(game[count+2]) and not(infobox.p1Turn):
		infobox.SwapTurn(board, False)
		
	if root != None:
		root.update()
		
	
def isInt(num):
	try:
		int(num) 
		return True
	except:
		return False


		