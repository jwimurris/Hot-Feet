import pygame
import os
import random
import time
from pygame.locals import KEYDOWN
import numpy as np
import sys
sys.path.append(os.path.join("modules"))
from modules.game_presets import WIN, WIDTH, HEIGHT, TILE_XY_COUNT, STARTING_BOARD, STEPSIZE, BACKGROUND
from modules.objects import Tile, Player#, Cursor
from modules.controls import Cursor
from modules.helper_functions import redraw_window
 
"""
TODO: 
We need a selector that shows on screen where the cursor is and what actions are available
--> to do this, we need a function that shows which objects collide with the cursor. 
So which tile from the list and which player from the list.  --> use collide function from 
space shooter for this!

"""

pygame.font.init() #you have to initialize font first (if you want to write in the game)


pygame.display.set_caption("Hotfeet") #Setting the name of the window

#load music
pygame.mixer.init()



def main():
	"""This functions triggers the game to run"""
	run = True
	paused = False
	FPS = 60
	clock= pygame.time.Clock()

	
	lost = False
	lost_count = 0 #variable to determine how many seconds to pauze the game before quiting out after losing. 

	songswitch = 0
	count = 0


	tiles = []
	
	players = []
	player_turn_count = 0
	player_start_positions = {
		"player 1" : (int(STEPSIZE*(TILE_XY_COUNT/2)-20), HEIGHT - STEPSIZE), 
		"player 2" : (int(STEPSIZE*(TILE_XY_COUNT/2)-20), 6), 
		"player 3" : (-10, int(STEPSIZE*(TILE_XY_COUNT/2)-40)), 
		"player 4" : (WIDTH - STEPSIZE, int(STEPSIZE*(TILE_XY_COUNT/2)-40))
		}

	center_x = range(3, WIDTH, int(WIDTH/TILE_XY_COUNT))[int(TILE_XY_COUNT/2)]
	center_y = range(3, HEIGHT, int(HEIGHT/TILE_XY_COUNT))[int(TILE_XY_COUNT/2)]
	# cursor = Cursor(center_x, center_y)
	cursor = Cursor(int(STEPSIZE*(TILE_XY_COUNT/2)-28), HEIGHT - STEPSIZE*0.95)

	#spawning players	
	for player in player_start_positions: 
		players.append(Player(player_start_positions[player], player))

	#generating game board..
	for row, x in zip(STARTING_BOARD, range(3, WIDTH, int(WIDTH/TILE_XY_COUNT))): 
		for health, y in zip(row, range(3, HEIGHT, int(HEIGHT/TILE_XY_COUNT))):
			tiles.append(Tile(x, y, health))

	while run: 
		clock.tick(FPS) #makes sure the game runs at the frames set by FPS
		if not pygame.mixer.music.get_busy():
			songswitch=play_music(songswitch)


		if lost: 
			run = False
		
		#handeling player pause or quet input:
		for event in pygame.event.get(): 
			if event.type == pygame.QUIT: #  if someone clicks the X in the corner it makes sure the games ends
				run = False
				pygame.mixer.music.stop()
			elif event.type == KEYDOWN:
				if event.key == pygame.K_p: 
					paused = not paused
					if paused: 
						pygame.mixer.music.pause()
					else: 
						pygame.mixer.music.unpause()

		redraw_window(tiles, players, cursor, lost, paused) 
		if not paused:
			count += 1
			if count == 3600: 
				run == False

			
			cursor.interact(count, tiles, players)

			#making sure that cursor and player snaps to tiles --> fixed position
			for tile in tiles: 
				for player in players: 
					if player.contact(tile): 
						# print (f"{player.player}, contacts tile at {tile.x, tile.y} while at {player.x, player.y}")
						player.x, player.y = tile.x, tile.y
						# if turn_ends: 
						# 	tile.health -= 1
				# if tile is destroyed, remove from board
				if tile.health <= 0: 
					tiles.remove(tile)

			# if keys[pygame.K_SPACE]: 
			# 	player.shoot()

			player_turn = player_turn_count % len(players) + 1
			for player in players: 
				player.menu(cursor, WIN, tiles, players, lost, paused)
				if player.player == f"player {player_turn}": 
					player.active = True
					if player.action_points <= 0: 
						player_turn_count += 1
						player.active = False
						player.action_points = 4
						for tile in tiles: 
							if player.contact(tile):
								tile.health -= 1
			
		



		

def main_menu(): 
	run = True
	title_font = pygame.font.SysFont("comicsans", 70)
	subtitle_font = pygame.font.SysFont("comicsans", 30)
	pygame.mixer.music.load(os.path.join("assets", "music", "08 Black Blade.mp3"))
	
	while run: 
		if not pygame.mixer.music.get_busy():
			pygame.mixer.music.play(-1)
		WIN.blit(BACKGROUND, (0,0))
		title_label = title_font.render("Welcome to Hotfeet", 1, (255,255,255))
		subtitle_label = subtitle_font.render("Press the mouse to begin...", 1, (255,255,255))
		WIN.blit(title_label, ((WIDTH/2)-title_label.get_width()/2,(HEIGHT/2)-title_label.get_height()/2))
		WIN.blit(subtitle_label, ((WIDTH/2)-subtitle_label.get_width()/2,(HEIGHT/1.5)-subtitle_label.get_height()/2))
		pygame.display.update()
		for event in pygame.event.get(): 
			if event.type == pygame.QUIT: #  if someone clicks the X in the corner it makes sure the games ends
			 	pygame.mixer.music.stop()
			 	run = False
			if event.type == pygame.MOUSEBUTTONDOWN: 
				pygame.mixer.music.stop()
				main()	
	pygame.quit()


def play_music(songswitch=1):
	"""
	Music player
	"""
	files = os.listdir(os.path.join("assets", "music")) 
	files = [fl for fl in files if fl.endswith(".mp3")] 
	song = files[(songswitch % len(files))]
	print(song)
	pygame.mixer.music.load(os.path.join("assets", "music", song))
	pygame.mixer.music.play()
	return songswitch+1

	

main_menu()

