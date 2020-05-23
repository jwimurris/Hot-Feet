import os
import pygame
from game_presets import WIDTH, HEIGHT, TILE_XY_COUNT, STEPSIZE, MENU_FONT, BACKGROUND, WIN, MAIN_FONT, LOST_FONT, ARROWS
from pygame.locals import KEYDOWN
from collections import deque
import queue
vec = pygame.math.Vector2

def load_img(imgname, modifier = 1):
	"""When modifier increases, the size of the image decreases"""
	img = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", imgname))
	img = pygame.transform.scale(img, (int(WIDTH/(TILE_XY_COUNT*modifier)), int(HEIGHT/(TILE_XY_COUNT*modifier))))
	return img

def collide(obj1, obj2): 
	"""
	This function returns True if 2 object masks overlap
	--> this is a very important function. 
	"""
	offset_x = int(obj2.x - obj1.x)
	offset_y = int(obj2.y - obj1.y)
	return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def redraw_window(tiles, players, cursor, lost, paused, board): 
	"""
	This function draws/refreshes the window
	"""
	WIN.blit(BACKGROUND, (0,0)) #first draw background as 1st layer --> With BLIT you can draw SOURCE is picture, dest = coordinates
	# player.draw(WIN)

	#drawing tiles
	for tile in tiles: 
		tile.draw(WIN)
	
	for player in players: 
		player.draw(WIN)
		player.show_range(cursor, WIN, tiles, board)

	cursor.draw(WIN)

	if lost: 
		lost_label = LOST_FONT.render("You lost!!", 1, (255,255,255))
		WIN.blit(lost_label, ((WIDTH/2-lost_label.get_width()/2),HEIGHT/2))

	if paused: 
		paused_label = LOST_FONT.render("Game Paused (press 'p' to unpause)", 1, (255,255,255))
		WIN.blit(paused_label, ((WIDTH/2-paused_label.get_width()/2),HEIGHT/2))

	pygame.display.update() #refreshing display


def vec2int(v):
	"""
	some objects like sets or dictionaries don't accept vectors (unhashable). 
	So these vector needs to be converted to tuple with integers (x, y)
	"""
	return (int(v.x), int(v.y))

def tuple2vec(tup):
	"""
	This function is the opposite of vec2int and changes tuple coordinates back to vectors. 
	""" 
	return vec(tup[0], tup[1])


def breadth_first_search(board, start, end):
	"""
	BFS path finding algorithim : finds the shortest path

	arguments: 
	:board: gameboard == grid
	:start: position from which the algorithm starts finding new positions
	:end: end position, if reached stop

	:returns: a list that contains the path from start to end in vector coordinates
	"""
	paths = queue.Queue()
	current_path = [start] #path is always a list
	paths.put(current_path) #puts current path in queue
	if end in current_path: 
		return current_path
	search_board = True
	while search_board:
		current_path = paths.get()
		last_tile = current_path[-1]
		for next_tile in board.find_neighbors(last_tile):
			if next_tile not in current_path: 
				new_path = current_path + [next_tile]
				if end in new_path or end == next_tile: 
					search_board = False
					return new_path
				else: 
					paths.put(new_path)



def draw_path(window, path):
	"""
	This function draws the path the player can move

	Takes:

	:window: the window to draw arrows in
	:path: the shortest path to destination --> the path to draw arrows on:
	"""
	for index in range(len(path)): 
		if index == 0: 
			pass
		else: 
			previous = path[index-1]
			current = path[index]
			direction = current-previous # the direction vector of the arrows
			x = current.x * STEPSIZE + STEPSIZE / 2
			y = current.y * STEPSIZE + STEPSIZE / 2
			img = ARROWS[vec2int(direction)]
			r = img.get_rect(center=(x, y))
			window.blit(img, r)


def check4hotfeet(player, players, tiles, player_turn_count): 
	"""
	Function that checks whether player has hotfeet and save this state in player. If next turn 
	this is not fixed, player dies and is removed from player list. 

	hotfeet = when player is not in contact with any tile
	"""
	if player_turn_count != player.turn_count: #if new turn, check for hotfeet, else do nothing
		player.turn_count = player_turn_count #saving current count in player
		tiles_in_contact = []
		for tile in tiles: 
			if player.contact(tile):
				tiles_in_contact.append(tile)
		if len(tiles_in_contact) == 0:
			if player.hotfeet: 
				print(f"{player.player} lost!")
				player.active = False
				players.remove(player)
			else: 
				print(f"{player.player} has hotfeet!")
				player.hotfeet = True
		else: 
			player.hotfeet = False



