import pygame
import os
# import sys
# sys.path.append(os.path.join("..","..", "hotfeet"))
from game_presets import WIN, WIDTH, HEIGHT, TILE_XY_COUNT, STEPSIZE, TILE_FONT, PLAYER_FONT, MENU_FONT, BACKGROUND
from helper_functions import load_img, collide, redraw_window
from pygame.locals import KEYDOWN
import math
from controls import Cursor, generate_posible_coordinates


#loading tile images
TILE_LVL1 = load_img("floor_lvl1_outlined.png")
TILE_LVL2 = load_img("floor_lvl2_outlined.png")
TILE_LVL3 = load_img("floor_lvl3_outlined.png")
TILE_LVL4 = load_img("floor_lvl4_outlined.png")
VOLCANO = load_img("Volcano.png")

#loading player images
PLAYER1 = load_img("ninja.png")#, modifier=1.3)
# PLAYER1 = pygame.transform.rotate(PLAYER1, 90)
PLAYER2 = load_img("archer.png")#, modifier=1.3)
PLAYER3 = load_img("mage.png")#, modifier=1.3)
# PLAYER3 = pygame.transform.rotate(PLAYER3, 45)
PLAYER4 = load_img("knight.png")#, modifier=1.3)
# PLAYER4 = pygame.transform.rotate(PLAYER4, 225)


pygame.font.init()


class Tile:
	"""docstring for Tiles"""
	HEALTH2IMG = {
	1: TILE_LVL1, 
	2: TILE_LVL2,
	3: TILE_LVL3, 
	4: TILE_LVL4, 
	5: VOLCANO
	}

	def __init__(self, x, y, health = 3):
		# super(Tiles, self).__init__()
		self.x, self.y = x, y
		self.health = health
		self.img = self.HEALTH2IMG[self.health]
		self.mask = pygame.mask.from_surface(self.img)

	def damage(self, dmg): 
		self.health -= dmg
		if self.health > 0: 
			self.img = self.HEALTH2IMG[self.health]
			self.mask = pygame.mask.from_surface(self.img)

	def draw(self, window): 
		window.blit(self.img, (self.x, self.y))
		health_label = TILE_FONT.render(f"{self.health}", 1, (50,255,60))
		window.blit(health_label, (self.x+self.get_width()/5, self.y+self.get_height()/5))

	def get_width(self): 
		return self.img.get_width()

	def get_height(self): 
		return self.img.get_height()


class Interact: 
	"""
	This class defines how the player can interact with its avatar and world
	"""
	def generate_menu(self, window, tiles, players, lost, paused): 
		"""
		This function generates a menu from which the player can choose a few actions. 
		"""
		run = True
		index = 0
		options = ["Move", "Attack", "Show Cards", "Back"]
		screen = pygame.Surface((STEPSIZE*4, STEPSIZE*2.5), pygame.SRCALPHA)   # per-pixel alpha
		screen.fill((250,255,200,128)) 
		x, y = self.get_visual_xy(screen)
		info = f"{self.player.capitalize()}                   AP = {self.action_points}"
		info_label = MENU_FONT.render(info,1, (155,80,255))
		print("in player menu")
		while run: 
			selected_option = options[index]
			window.blit(screen, (x, y))
			window.blit(info_label, (x+10, y+5))
			line_spacing = 5+info_label.get_height()*2
			for opt in options: 
				if opt == selected_option: #highlighting the selected option
					opt_label = MENU_FONT.render(opt, 1, (60,50,255))
				else:
					opt_label = MENU_FONT.render(opt, 1, (255,50,60))
				window.blit(opt_label, (x+10, y + line_spacing))
				line_spacing += opt_label.get_height()+10

			#handeling player pause or quit input:
			for event in pygame.event.get(): 
				if event.type == KEYDOWN:
					if event.key == pygame.K_SPACE:
						if selected_option == "Back":
							print("leaving player menu") 
							run = False
						elif selected_option == "Move": 
							choice = self.choose_path(tiles, players, lost, paused)
							if choice: 
								run = False
						elif selected_option == "Attack": 
							choice = self.attack(tiles, players, lost, paused)
							if choice: 
								run = False
					if event.key == pygame.K_UP: #incrementing the index based on key presses
						index -=1
					if event.key == pygame.K_DOWN: 
						index +=1
					if event.key == pygame.K_ESCAPE: 
						run = False

			#setting the index to the boundaries of the option list
			if index >= len(options): 
				index = len(options)-1
			elif index < 0: 
				index = 0
			pygame.display.update() #refreshing display

	def get_visual_xy(self, visual): 
		"""
		This function returns the xy positions to blit the visual. The position is determined
		by the position of the object (player mostly) and how much space is left on the screen 
		in relation to the object position. 
		:obj: the object which xy coordinates are used. 
		:visual: the visual to display 

		:returns xy coordinates 
		"""
		if self.x + STEPSIZE + visual.get_width() < WIDTH:
			x = self.x + STEPSIZE 
		else: 
			x = self.x - STEPSIZE - visual.get_width()
		if self.y - visual.get_height() > 0: 
			y = self.y - visual.get_height()
		else: 
			y = self.y + STEPSIZE
		return x, y

	def show_range(self, cursor, window, tiles, range_of_positions=None, active = False, ): 
		"""
		Draws the range of the player

		"""
		if cursor.contact(self) or active: 
			if not range_of_positions: 
				range_of_positions = generate_posible_coordinates(self, tiles)
			for pos in range_of_positions: 
				pos.draw(window)

	def choose_path(self, tiles, players, lost, paused): 
		run = True
		cursor = Cursor(self.x, self.y)
		count = 0
		choice = False
		range_of_positions = generate_posible_coordinates(self, tiles)
		while run == True and self.action_points > 0: 
			cursor.draw(WIN)
			cursor.interact(count, tiles, players, limit2tiles = True)
			for event in pygame.event.get(): 
				if event.type == KEYDOWN:
					if event.key == pygame.K_SPACE:
						if len([player for player in players if cursor.contact(player)]) == 0:
							self.x, self.y = cursor.x, cursor.y
							self.action_points -= 1
							run = False
							choice = True
						else: 
							print("tile already occupied!")
					if event.key == pygame.K_ESCAPE: 
						run = False
			count += 1
			redraw_window(tiles, players, cursor, lost, paused) 
			self.show_range(cursor, WIN, tiles, range_of_positions, active = True)
			pygame.display.update()
		return choice



class Player(Interact): 
	"""
	This class defines player objects
	"""
	PLAYER2IMG = {
	"player 1": PLAYER1, 
	"player 2": PLAYER2, 
	"player 3": PLAYER3, 
	"player 4": PLAYER4
	}
	__name__ = "Player"

	def __init__(self, start_position, player): 
		self.x, self.y = start_position 
		self.player = player
		self.active = False
		self.action_points = 4
		self.img = self.PLAYER2IMG[self.player]
		self.mask = pygame.mask.from_surface(self.img)

	def move(self, path2destination = []): 
		"""path should be an iterable containing the directions the player should move"""
		for direction in path2destination:
			if self.action_points > 0 and self.active == True:  
				if direction == "up" and (self.y - STEPSIZE) > 0: 
					self.y -= STEPSIZE
				elif direction == "down" and (self.y + STEPSIZE) < HEIGHT:
					self.y += STEPSIZE
				elif direction == "left" and (self.x - STEPSIZE) > 0:
					self.x -= STEPSIZE
				elif direction == "right" and (self.x + STEPSIZE) < WIDTH:
					self.x += STEPSIZE
				self.action_points -= 1
				self.check_turn()

	def attack(self, tiles, players, lost, paused, amount = 1):
		run = True
		cursor = Cursor(self.x, self.y)
		count = 0
		choice = False
		range_of_positions = generate_posible_coordinates(self, tiles)
		while run == True and self.action_points > 0: 
			cursor.draw(WIN)
			cursor.interact(count, tiles, players, limit2tiles = True)
			for event in pygame.event.get(): 
				if event.type == KEYDOWN:
					if event.key == pygame.K_SPACE:
						for tile in tiles: 
							if cursor.contact(tile): 
								if len([player for player in players if cursor.contact(player)]) == 0:
									tile.damage(amount)
									self.action_points -= amount
									run = False
									choice = True
								else: 
									print("can't attack a tile that is occupied")
					if event.key == pygame.K_ESCAPE: 
						run = False
			count += 1
			redraw_window(tiles, players, cursor, lost, paused) 
			self.show_range(cursor, WIN, tiles, range_of_positions, active = True)
			pygame.display.update()
		return choice



		if self.action_points >= amount and self.active == True:
			tile.damage(amount)
			self.action_points -= amount
			# self.check_turn()

	def check_turn(self): 
		if self.active == True and self.action_points <= 0: 
			self.active = False
			self.action_points = 4

	def draw(self, window): 
		window.blit(self.img, (self.x, self.y))
		if self.active: 
			player_label = PLAYER_FONT.render(f"{self.player}", 1, (50,255,60))
		else: 
			player_label = PLAYER_FONT.render(f"{self.player}", 1, (255,50,60))
		window.blit(player_label, (self.x-player_label.get_width()/5, self.y-player_label.get_height()/2))

	def get_width(self): 
		return self.img.get_width()

	def get_height(self): 
		return self.img.get_height()

	def menu(self, cursor, window, tiles, players, lost, paused): 
		if cursor.contact(self) and self.active: 
			for event in pygame.event.get(): 
				if event.type == KEYDOWN:
					if event.key == pygame.K_SPACE:
						print("menu")
						self.generate_menu(window, tiles, players, lost, paused)

	def contact(self, obj): 
		return collide(self, obj)

	





		


# class Coin: 
# 	"""docstring for Coin"""
# 	def __init__(self, img): 
# 		self.img = img