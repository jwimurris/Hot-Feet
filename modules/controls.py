import pygame
from helper_functions import load_img, collide
from game_presets import WIDTH, HEIGHT, TILE_XY_COUNT, STEPSIZE
import math

class Cursor: 
	
	def __init__(self, x, y): 
		self.x, self.y = x, y
		self.img = None
		self.cursor = pygame.Surface((STEPSIZE, STEPSIZE), pygame.SRCALPHA)   # per-pixel alpha
		self.cursor.fill((200,255,200,128))                         # notice the alpha value in the color
		self.mask = pygame.mask.from_surface(self.cursor)

	def interact(self, count, tiles, players, limit2tiles = False): 
		direction = None
		# back = "left"
		keys = pygame.key.get_pressed()
		if count % 3 == 0:
			if (keys[pygame.K_UP] or keys[pygame.K_w]):  #move up if not at limit of screen
				direction = "up"
			if (keys[pygame.K_DOWN] or keys[pygame.K_s]):  
				direction = "down"
			if (keys[pygame.K_LEFT] or keys[pygame.K_a]):  
				direction = "left"
			if (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
				direction = "right"
			if direction:
				back = self.move(direction)
			players_in_contact = [player for player in players if self.contact((player))]# and not limit2tiles]
			tiles_in_contact = [tile for tile in tiles if self.contact(tile)] + players_in_contact
			# if limit2tiles: #Removing non-available tiles (that is tiles with players on it) when in movement/attack menu
			# 	for tile in tiles_in_contact: 
			# 		players_on_tile = [player for player in players if player.contact(tile)]
			# 		if len(players_on_tile) > 0: 
			# 			tiles_in_contact.remove(tile)
			# 			print("can't attack this tile")
				# tiles_in_contact = [tile for tile in tiles_in_contact if not player.contact(tile)]
			if tiles_in_contact: 
				self.snap_into_position(direction, tiles_in_contact)
			else: 
				if limit2tiles:
					back = self.move(back)
					tiles_in_contact = [tile for tile in tiles if self.contact(tile)]
					if tiles_in_contact: 
						self.snap_into_position(direction, tiles_in_contact)


	def move(self, direction): 
		back = None
		if direction == "up" and (self.y - STEPSIZE) > 0: 
			self.y -= STEPSIZE
			back = "down"
		elif direction == "down" and (self.y + STEPSIZE*2) < HEIGHT:
			self.y += STEPSIZE
			back = "up"
		elif direction == "left" and (self.x - STEPSIZE) > 0:
			self.x -= STEPSIZE
			back = "right"
		elif direction == "right" and (self.x + STEPSIZE*2) < WIDTH:
			self.x += STEPSIZE
			back = "left"
		if back: 
			return back
		
	def draw(self, window): 
		window.blit(self.cursor, (self.x, self.y))
		# pygame.draw.rect(window, (200, 255, 200), (self.x, self.y, STEPSIZE, STEPSIZE),0)

	def contact(self, obj): 
		return collide(self, obj)

	def snap_into_position(self, direction, tiles_in_contact):
		if direction == "up" or direction == "left":
			self.x, self.y = tiles_in_contact[-1].x, tiles_in_contact[-1].y
		else: 
			self.x, self.y = tiles_in_contact[0].x, tiles_in_contact[0].y



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

	def snap_into_position(self, tiles_in_contact, player_x):
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


def generate_posible_coordinates(player, tiles):
	"""
	:returns a list of possible positions
	""" 
	range_of_positions = []
	for steps_in_row, offset in zip(range(player.action_points*2+1, 0, -2), range(0, player.action_points+1)): 
		steps_per_side = math.floor(steps_in_row/2)
		for pos in range(steps_per_side, -steps_per_side-1, -1): 
			# print (f"pos = {pos}")
			x = player.x - STEPSIZE*pos
			y_up = player.y - offset*STEPSIZE
			y_down = player.y + offset*STEPSIZE 
			if offset>0: 
				positions = [HighlightedTile(x, y_up, above = True), HighlightedTile(x, y_down, above=False)]
			else: 
				positions = [HighlightedTile(x, y_up, above = True)]
			for htile in positions: 
				tiles_in_contact = [tile for tile in tiles if htile.contact(tile)]
				if tiles_in_contact: 
					htile.snap_into_position(tiles_in_contact, player.x)
				else: 
					positions.remove(htile)
			range_of_positions += positions


	return range_of_positions
		