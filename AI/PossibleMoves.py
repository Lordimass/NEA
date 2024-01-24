import itertools
import config
import csv
import saveload
from findword import FindWord
from dependents import list_to_string
from countpoints import CountPoints

def PossibleMoves(board, infobox, root):
	words = [] # Store of potential words that have already been checked
			   # for validity, saves checking against the wordlist again
	directions = [True, False] # Left/Right or Up/Down
	game_index = LatestGameIndex() # Index of the current game to reload to
	player = infobox.player2
	rack = player.GetRack()

	rack_letters = "" 
	for tiles in rack:
		rack_letters += tiles.GetLetter()

	for rowNum in range(0, len(board)):
		for colNum in range(0, len(board[rowNum])): # Iterating through every space to check for moves
			space = board[rowNum][colNum]
			tile = space.tile

			if tile == None: # skip space if it's empty
				continue
			print(f"Looking at {colNum}, {rowNum}")

			for direction in directions: # Look in each direction
				# Creating list of tiles "  a g  i" where letters are the letters already on the board
				gls_spaces = [space]

				for forwards_backwards in [1,-1]: # go forward and backwards
					pointer = [colNum, rowNum]
					keep = False # Decides whether to keep the letters string or not

					# Finding the number of spaces to look in seeking direction, and numerice direction
					if direction and forwards_backwards == 1: # Right
						tile_range = config.num_tiles - pointer[0] -1 # -1 to account for 0 index
					elif direction and forwards_backwards == -1: # Left
						tile_range = pointer[0]
					elif not(direction) and forwards_backwards == 1: # Down
						tile_range = config.num_tiles - pointer[1] -1
					elif not(direction) and forwards_backwards == -1: # Up
						tile_range = pointer[1]

					numericed_direction = numerice_direction(direction, forwards_backwards)

					# Iterating as far as possible in direction
					for i in range(tile_range):
						pointer[0] += numericed_direction[0]
						pointer[1] += numericed_direction[1]
						next_space = board[pointer[1]][pointer[0]]

						if next_space.tile == None: # Empty space
							keep = True # Letter string should only be considered
										# when there are gaps to play letters in to

						if forwards_backwards == 1:
							gls_spaces.append(next_space)
						else:
							gls_spaces = [next_space] + gls_spaces

				if not keep: # If there were no gaps found, move on to the next tile
					continue

				# Generating gappy letter string
				gls = ""
				for i in gls_spaces:
					if i.tile != None:
						gls += i.tile.GetLetter()
					else:
						gls += " "

				# Debugging section to count the number of permutations to be iterated through
				count = 0
				for k in range(1, gls.count(" ")):
					for i in itertools.permutations(rack_letters, k): 
						count+=1
				print(f"Iterating over {count} possible moves for ({colNum},{rowNum}) (Horizontal = {direction})") 

				best_move = [game_index, 0] # [index of games.csv of the best move save,
											# number of points it scores]
				invalids = 0
				# Generate all possible combinations of letters from the rack that will fit in the gaps
				for count in range(1, gls.count(" ")):
					for perm in itertools.permutations(rack_letters, count):
						valid = True
						points = 0
						perm = list_to_string(perm) # Perm is returned as a list of letters,
													# so it needs to be converted to a string
						perm = perm.strip(" ")

						if (perm in words) or (perm.count(" ") > 0): # Skipping duplicate and invalid results
							invalids += 1
							continue

						# Fill perm with letters already on the board
						index = 0
						for letter in gls:
							if letter != " ":
								perm = perm[:index] + letter + perm[index:]
							index += 1

						words.append(perm)

						# If word is invalid, move to next permutation
						if not FindWord(perm, False): 
							continue

						print(f'''	
	  Trying word: {perm}
	  At:          ({colNum},{rowNum})
	  Horizontal:  {direction}
	  GappyWord™:  {gls.replace(" ", "_")}\n''')

						# Picking a tile to anchor from, will then place tiles forward and backward from here
						for anchor_space in gls_spaces:
							if anchor_space.tile != None and anchor_space.tile.GetLetter() in perm:
								break

						played_tiles = []

						# Playing tiles forward and backward from anchor space
						for forward_backward in [1,-1]:
							pointer_space_coords = [int(anchor_space.coordinate[0]), int(anchor_space.coordinate[1])]
							perm_index = perm.index(anchor_space.tile.GetLetter())
							numericed_direction = numerice_direction(direction, forward_backward)

							# Determining how many letters in direction there are to play
							if forward_backward == 1:
								for_range = range(len(perm[perm_index+1:]))
							else:
								for_range = range(len(perm[:perm_index]))

							# Playing tiles in range
							for i in for_range:
								perm_index += forward_backward
								pointer_space_coords[0] += numericed_direction[0]
								pointer_space_coords[1] += numericed_direction[1]
								try:
									pointer_space = board[pointer_space_coords[1]][pointer_space_coords[0]]
								except:
									valid = False

								if pointer_space.tile == None:
									# Finding the tile in the player's rack to play
									for tile in rack:
										if tile.GetLetter() == perm[perm_index]:
											break

									if tile == None:
										raise(f"Unable to find tile '{perm[perm_index]}'")

									pointer_space.PlayTile(tile)
									player.RemoveLetter(perm[perm_index])
									played_tiles.append(tile)

						points += CountPoints(played_tiles, board)

						# Iterate through each played tile to find cross words
						for anchor_tile in played_tiles:
							word = ""
							for forward_backward in [1,-1]:
								numericed_direction = numerice_direction(not(direction), forward_backward)
								if forward_backward == 1:
									pointer_space_coords = [int(anchor_tile.position[0]),
															int(anchor_tile.position[1])]
								else:
									pointer_space_coords = [int(anchor_tile.position[0])+numericed_direction[0],
															int(anchor_tile.position[1])+numericed_direction[1]]

								xOK = pointer_space_coords[0]<config.num_tiles
								yOK = pointer_space_coords[1]<config.num_tiles
								while xOK and yOK:
									pointer_space = board[pointer_space_coords[1]][pointer_space_coords[0]]

									if pointer_space.tile == None:
										break

									if forward_backward == 1:
										word += pointer_space.tile.GetLetter()
									else:
										word = pointer_space.tile.GetLetter() + word

									pointer_space_coords[0] += numericed_direction[0]
									pointer_space_coords[1] += numericed_direction[1]

							if len(word)==1:
								continue

							if not(FindWord(word)):
								valid = False
								break
							else:
								points += CountPoints(None, None, word)

						if valid and points > best_move[1]:# If it's better than the
														   #current saved best move
							player.AddPoints(points)
							infobox.SwapTurn(board)
							infobox.UpdateText()
							saveload.saveGame(board, infobox)
							best_move = [LatestGameIndex(), points]
						saveload.loadGame(game_index, board, infobox, root)
				print(f"Eliminated {invalids} moves pre-word check")
	saveload.loadGame(best_move[0], board, infobox) # Load the best move found

	if best_move[1] == 0: # To prevent getting stuck if no moves are found
		infobox.SwapTurn(board)

def numerice_direction(direction, forwards_backwards):
	if direction and forwards_backwards == 1: # Right
		numericed_direction = [1,0]
	elif direction and forwards_backwards == -1: # Left
		numericed_direction = [-1,0]
	elif not(direction) and forwards_backwards == 1: # Down
		numericed_direction = [0,1]
	elif not(direction) and forwards_backwards == -1: # Up
		numericed_direction = [0,-1]

	return numericed_direction

def LatestGameIndex():
	f = open("AI/games.csv", "r")
	gamesFile = list(csv.reader(f))
	return len(gamesFile)
	del gamesFile
	f.close()