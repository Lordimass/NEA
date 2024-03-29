from math import floor

def screen_buffer(screen_buffer_percent, screen_size):
    screen_buffer = []
    screen_buffer.append(floor(screen_buffer_percent[0]*screen_size[0]))
    screen_buffer.append(floor(screen_buffer_percent[1]*screen_size[1]))
    return tuple(screen_buffer)

def win_buffer(win_buffer_percent, win_size):
    win_buffer = []
    win_buffer.append(floor(win_buffer_percent[0]*win_size[0]))
    win_buffer.append(floor(win_buffer_percent[1]*win_size[1]))
    return tuple(win_buffer)

def tile_size(win_size, win_buffer, num_tiles):
    space = win_size[1] - (2*win_buffer[1])
    return space//num_tiles

def info_pos(win_size, win_buffer, tile_size, num_tiles):
    x = (2*win_buffer[0]) + (tile_size*num_tiles)
    y = win_buffer[1]
    return (x,y)

def info_size(win_size, win_buffer, info_pos):
    x = win_size[0] - win_buffer[0] - info_pos[0]
    y = (win_size[1] - (2*win_buffer[1]))*0.9
    return (x,y)

def pass_pos(info_pos, info_size):
	x = info_pos[0]
	y = info_pos[1]+info_size[1]
	return(x,y)

def pass_size(info_size, win_buffer, win_size, pass_pos):
	x = info_size[0]
	y = win_size[1]-(2*win_buffer[1])-info_size[1]
	return(x,y)

def list_to_string(list):
	string = ""
	for i in list:
		string += i
	return string