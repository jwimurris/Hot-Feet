import pygame
from helper_functions import load_img, collide, vec2int, tuple2vec
from game_presets import WIDTH, HEIGHT, TILE_XY_COUNT, STEPSIZE
import math
import queue
vec = pygame.math.Vector2

class Cursor: 
	
	def __init__(self, x, y): 
		self.x, self.y = x, y
		self.img = None
		self.cursor = pygame.Surface((STEPSIZE, STEPSIZE), pygame.SRCALPHA)   # per-pixel alpha
		self.cursor.fill((200,255,200,128))                         # notice the alpha value in the color
		self.mask = pygame.mask.from_surface(self.cursor)

	def interact(self, count, board, limit2tiles = False): 
		direction = None
		# back = "left"
		keys = pygame.key.get_pressed()
		if count % 3 == 0:
			if (keys[pygame.K_UP] or keys[pygame.K_w]):  #move up if not at limit of screen
				direction = vec(0, -1)
				self.move(direction,board, limit2tiles)
			if (keys[pygame.K_DOWN] or keys[pygame.K_s]):  
				direction = vec(0, 1)
				self.move(direction,board, limit2tiles)
			if (keys[pygame.K_LEFT] or keys[pygame.K_a]):  
				direction = vec(-1, 0)
				self.move(direction,board, limit2tiles)
			if (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
				direction = vec(1, 0)
				self.move(direction,board, limit2tiles)

	def move(self, direction, board, limit2tiles):
			if direction:
				movement = direction*STEPSIZE
				goal = vec(self.x+movement.x, self.y+movement.y)//STEPSIZE
				if board.in_bounds(goal):
					if limit2tiles: 
						if board.passable(goal): 
							self.x += movement.x
							self.y += movement.y
					else: 
						self.x += movement.x
						self.y += movement.y
	
	def draw(self, window): 
		window.blit(self.cursor, (self.x, self.y))
		# pygame.draw.rect(window, (200, 255, 200), (self.x, self.y, STEPSIZE, STEPSIZE),0)

	def contact(self, obj): 
		return collide(self, obj)

	# def snap_into_position(self, direction, tiles_in_contact):
	# 	if direction == "up" or direction == "left":
	# 		self.x, self.y = tiles_in_contact[-1].x, tiles_in_contact[-1].y
	# 	else: 
	# 		self.x, self.y = tiles_in_contact[0].x, tiles_in_contact[0].y



class HighlightedTile: 

	def __init__(self, x, y, above = True): 
		self.x, self.y = x, y
		self.step = pygame.Surface((STEPSIZE, STEPSIZE), pygame.SRCALPHA)
		self.step.fill((230,255,255,128))
		self.mask = pygame.mask.from_surface(self.step)
		self.above = above 

	def draw(self, window): 
		window.blit(self.step, (self.x, self.y))

	def contact(self, obj): 
		return collide(self, obj)

	def snap_into_position(self, tiles_in_contact):
		#finding the smallest difference between the tile coordinates and the guesed coordinates
		diffs = {}
		diffs["x"] = {}
		diffs["y"] = {}
		for tile in tiles_in_contact: 
			diffs["x"][tile.x-self.x] = tile.x
			diffs["y"][tile.y-self.y] = tile.y
		x = diffs["x"][min(diffs["x"].keys(), key=abs)]
		y = diffs["y"][min(diffs["y"].keys(), key=abs)]
		self.x, self.y = x, y


def generate_posible_coordinates(player, tiles, board):
	"""
	:returns a list of possible positions
	""" 
	range_of_positions = [] 
	start = tuple2vec((player.x, player.y))//STEPSIZE
	ap = player.action_points
	max_range = bfs_range(board, start, ap)
	for pos in max_range: 
		x, y = pos * STEPSIZE
		htile = HighlightedTile(x, y)
		tiles_in_contact = [tile for tile in tiles if htile.contact(tile)]
		if tiles_in_contact and board.passable(pos) and board.in_bounds(pos): 
			htile.snap_into_position(tiles_in_contact)
			range_of_positions.append(htile)
	return range_of_positions

def bfs_range(board, start, ap):
	"""
	Gets the max range the player can move/attack to. Utilizes BFS logic

	arguments: 
	:board: gameboard == grid
	:start: position from which the algorithm starts finding possible positions
	:ap: the amount of action points the player has left. --> determines range

	:returns: max_range = a set that contains the possible positions
	"""
	max_range = set()
	possible_paths = queue.Queue()
	current_path = [start] #path is always a list
	possible_paths.put(current_path) #puts current path in queue
	search_board = True
	if ap > 0: 
		while possible_paths.qsize()>0:
			current_path = possible_paths.get()
			last_tile = current_path[-1]
			neighbors = board.find_neighbors(last_tile)
			if neighbors: 
				for next_tile in neighbors:
					next_tile_converted = vec2int(next_tile) #convert to tuple to check with max range
					if next_tile_converted not in max_range: 
						new_path = current_path + [next_tile]
						if len(new_path)-1 == ap: 
							new_path = [vec2int(tile) for tile in new_path] #convert to list of tuples instead of vectors, because a set can't hash vectors
							max_range.update(new_path)
						elif len(new_path)-1 < ap: 
							possible_paths.put(new_path)
						else: 
							raise OverflowError(f"range can't exceed AP (current ap = {ap} while \
								pathlength was: {len(new_path)}")
					else: 
						new_path = current_path + [next_tile]
						new_path = [vec2int(tile) for tile in new_path] #convert to list of tuples instead of vectors, because a set can't hash vectors
						max_range.update(new_path)
			else: 
				new_path = [vec2int(tile) for tile in current_path] #convert to list of tuples instead of vectors, because a set can't hash vectors
				max_range.update(new_path)
		#convert back to list with vectors
		max_range = [tuple2vec(pos) for pos in list(max_range)]
		return max_range
	else: 
		return []






# def generate_posible_coordinates(player, tiles, board):
# 	"""
# 	:returns a list of possible positions
# 	""" 
# 	range_of_positions = []
# 	for steps_in_row, offset in zip(range(player.action_points*2+1, 0, -2), range(0, player.action_points+1)): 
# 		steps_per_side = math.floor(steps_in_row/2)
# 		for pos in range(steps_per_side, -steps_per_side-1, -1): 
# 			# print (f"pos = {pos}")
# 			x = player.x - STEPSIZE*pos
# 			y_up = player.y - offset*STEPSIZE
# 			y_down = player.y + offset*STEPSIZE 
# 			if offset>0: 
# 				positions = [HighlightedTile(x, y_up, above = True), HighlightedTile(x, y_down, above=False)]
# 			else: 
# 				positions = [HighlightedTile(x, y_up, above = True)]
# 			for htile in positions: 
# 				tiles_in_contact = [tile for tile in tiles if htile.contact(tile)]
# 				htile_vector_pos = vec(htile.x, htile.y)//STEPSIZE
# 				if tiles_in_contact and board.passable(htile_vector_pos) and board.in_bounds(htile_vector_pos): 
# 					htile.snap_into_position(tiles_in_contact, player.x)
# 				else: 
# 					positions.remove(htile)
# 			range_of_positions += positions


# 	return range_of_positions

# class Cursor: 
	
# 	def __init__(self, x, y): 
# 		self.x, self.y = x, y
# 		self.img = None
# 		self.cursor = pygame.Surface((STEPSIZE, STEPSIZE), pygame.SRCALPHA)   # per-pixel alpha
# 		self.cursor.fill((200,255,200,128))                         # notice the alpha value in the color
# 		self.mask = pygame.mask.from_surface(self.cursor)

# 	def interact(self, count, tiles, players, limit2tiles = False): 
# 		direction = None
# 		# back = "left"
# 		keys = pygame.key.get_pressed()
# 		if count % 3 == 0:
# 			if (keys[pygame.K_UP] or keys[pygame.K_w]):  #move up if not at limit of screen
# 				direction = "up"
# 			if (keys[pygame.K_DOWN] or keys[pygame.K_s]):  
# 				direction = "down"
# 			if (keys[pygame.K_LEFT] or keys[pygame.K_a]):  
# 				direction = "left"
# 			if (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
# 				direction = "right"
# 			if direction:
# 				back = self.move(direction)
# 			players_in_contact = [player for player in players if self.contact((player))]# and not limit2tiles]
# 			tiles_in_contact = [tile for tile in tiles if self.contact(tile)] + players_in_contact
# 			# if limit2tiles: #Removing non-available tiles (that is tiles with players on it) when in movement/attack menu
# 			# 	for tile in tiles_in_contact: 
# 			# 		players_on_tile = [player for player in players if player.contact(tile)]
# 			# 		if len(players_on_tile) > 0: 
# 			# 			tiles_in_contact.remove(tile)
# 			# 			print("can't attack this tile")
# 				# tiles_in_contact = [tile for tile in tiles_in_contact if not player.contact(tile)]
# 			if tiles_in_contact: 
# 				self.snap_into_position(direction, tiles_in_contact)
# 			else: 
# 				if limit2tiles:
# 					back = self.move(back)
# 					tiles_in_contact = [tile for tile in tiles if self.contact(tile)]
# 					if tiles_in_contact: 
# 						self.snap_into_position(direction, tiles_in_contact)


# 	def move(self, direction): 
# 		back = None
# 		if direction == "up" and (self.y) > 0: 
# 			self.y -= STEPSIZE
# 			back = "down"
# 		elif direction == "down" and (self.y + STEPSIZE) < HEIGHT:
# 			self.y += STEPSIZE
# 			back = "up"
# 		elif direction == "left" and (self.x) > 0:
# 			self.x -= STEPSIZE
# 			back = "right"
# 		elif direction == "right" and (self.x + STEPSIZE) < WIDTH:
# 			self.x += STEPSIZE
# 			back = "left"
# 		if back: 
# 			return back
		
# 	def draw(self, window): 
# 		window.blit(self.cursor, (self.x, self.y))
# 		# pygame.draw.rect(window, (200, 255, 200), (self.x, self.y, STEPSIZE, STEPSIZE),0)

# 	def contact(self, obj): 
# 		return collide(self, obj)

# 	def snap_into_position(self, direction, tiles_in_contact):
# 		if direction == "up" or direction == "left":
# 			self.x, self.y = tiles_in_contact[-1].x, tiles_in_contact[-1].y
# 		else: 
# 			self.x, self.y = tiles_in_contact[0].x, tiles_in_contact[0].y

		