mode                  = "pvp"
game_index			  = -2 # Index of game to load from games.csv 
						   # Set to -1 for a new game
						   # Set to -2 to open the last game
wordlist_path         = "wordlists/CSW21.txt"

screen_buffer_percent = (0.01, 0.09)
win_buffer_percent    = (0.05, 0.05)
resizable             = (False, False)

num_tiles             = 7 # Between 2 and 10 (HEX currently not implemented)
rack_size			  = 7

font                  = "Courier New"
default_font_size     = 15
font_weight           = "bold" # "bold" or "normal"
font_slant			  = "roman" # "italic" or "roman"
subscript             = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉") # Translation table for subscript characters

font         = (font,
				default_font_size,
				font_weight,
				font_slant)

background_colour     = "#ffffff"
info_box_colour       = "#FCFCE3"
indicator_colour	  = "#ff9e99"
pass_colour           = "#8de38a"
colours               = {None  : "#FCFCE3",
						 "Tile": "#f2daac",
						 "DW"  : "#A3CBFF",
 						 "DL"  : "#FFE6CC",
 						 "TW"  : "#F8CECC",
 						 "TL"  : "#DAE8FC"}

# Boundaries for num_tiles
if str(type(num_tiles)) != "<class 'int'>":
	raise TypeError("num_tiles in config.py must be an integer")
elif num_tiles<=1:
	num_tiles=2
elif num_tiles>10:
	num_tiles=10

# Boundaries for rack_size
if str(type(rack_size)) != "<class 'int'>":
	raise TypeError("rack_size in config.py must be an integer")
elif rack_size<2:
	rack_size=2


