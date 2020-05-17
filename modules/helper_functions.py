import os
import pygame
from game_presets import WIDTH, HEIGHT, TILE_XY_COUNT, STEPSIZE, MENU_FONT, BACKGROUND, WIN, MAIN_FONT, LOST_FONT
from pygame.locals import KEYDOWN


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

def redraw_window(tiles, players, cursor, lost, paused): 
		WIN.blit(BACKGROUND, (0,0)) #first draw background as 1st layer --> With BLIT you can draw SOURCE is picture, dest = coordinates
		# player.draw(WIN)

		#drawing tiles
		for tile in tiles: 
			tile.draw(WIN)
		
		for player in players: 
			player.draw(WIN)
			player.show_range(cursor, WIN, tiles)

		cursor.draw(WIN)

		if lost: 
			lost_label = LOST_FONT.render("You lost!!", 1, (255,255,255))
			WIN.blit(lost_label, ((WIDTH/2-lost_label.get_width()/2),HEIGHT/2))

		if paused: 
			paused_label = LOST_FONT.render("Game Paused (press 'p' to unpause)", 1, (255,255,255))
			WIN.blit(paused_label, ((WIDTH/2-paused_label.get_width()/2),HEIGHT/2))

		pygame.display.update() #refreshing display


# def generate_menu(obj, window): 
# 	run = True
# 	index = 0
# 	options = ["Move", "Attack", "Range", "Back"]
# 	screen = pygame.Surface((STEPSIZE*4, STEPSIZE*2.5), pygame.SRCALPHA)   # per-pixel alpha
# 	screen.fill((250,255,200,128)) 
# 	x, y = get_visual_xy(obj, screen)
# 	info = f"{obj.player.capitalize()}                   AP = {obj.action_points}"
# 	info_label = MENU_FONT.render(info,1, (155,80,255))
# 	print("in player menu")
# 	while run: 
# 		selected_option = options[index]
# 		window.blit(screen, (x, y))
# 		window.blit(info_label, (x+10, y+5))
# 		line_spacing = 5+info_label.get_height()*2
# 		for opt in options: 
# 			if opt == selected_option: #highlighting the selected option
# 				opt_label = MENU_FONT.render(opt, 1, (60,50,255))
# 			else:
# 				opt_label = MENU_FONT.render(opt, 1, (255,50,60))
# 			window.blit(opt_label, (x+10, y + line_spacing))
# 			line_spacing += opt_label.get_height()+10


# 		#handeling player pause or quet input:
# 		for event in pygame.event.get(): 
# 			if event.type == KEYDOWN:
# 				if event.key == pygame.K_SPACE:
# 					print("leaving player menu") 
# 					run = False
# 				if event.key == pygame.K_UP: #incrementing the index based on key presses
# 					index -=1
# 				if event.key == pygame.K_DOWN: 
# 					index +=1

# 		#setting the index to the boundaries of the option list
# 		if index >= len(options): 
# 			index = len(options)-1
# 		elif index < 0: 
# 			index = 0
# 		pygame.display.update() #refreshing display

# def get_visual_xy(obj, visual): 
# 	"""
# 	This function returns the xy positions to blit the visual. The position is determined
# 	by the position of the object (player mostly) and how much space is left on the screen 
# 	in relation to the object position. 
# 	:obj: the object which xy coordinates are used. 
# 	:visual: the visual to display 

# 	:returns xy coordinates 
# 	"""
# 	if obj.x + STEPSIZE + visual.get_width() < WIDTH:
# 		x = obj.x + STEPSIZE 
# 	else: 
# 		x = obj.x - STEPSIZE - visual.get_width()
# 	if obj.y - visual.get_height() > 0: 
# 		y = obj.y - visual.get_height()
# 	else: 
# 		y = obj.y + STEPSIZE
# 	return x, y




