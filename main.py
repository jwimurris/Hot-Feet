import pygame
import os
import random
import time
from pygame.locals import KEYDOWN
import numpy as np
import sys
sys.path.append(os.path.join("modules"))
from modules.game_presets import WIN, WIDTH, HEIGHT, TILE_XY_COUNT, STARTING_BOARD, STEPSIZE, BACKGROUND
from modules.objects import Tile, Player, SquareGrid, vec#, WeightedGrid
from modules.controls import Cursor
from modules.helper_functions import redraw_window, check4hotfeet
 


pygame.font.init() #you have to initialize font first (if you want to write in the game)


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
		"player 1" : (int(STEPSIZE*(TILE_XY_COUNT/2)), HEIGHT - STEPSIZE), 
		"player 2" : (int(STEPSIZE*(TILE_XY_COUNT/2)), 0), 
		"player 3" : (0, int(STEPSIZE*(TILE_XY_COUNT/2))), 
		"player 4" : (WIDTH - STEPSIZE, int(STEPSIZE*(TILE_XY_COUNT/2)))
		}

	center_x = range(0, WIDTH, STEPSIZE)[int(TILE_XY_COUNT/2)]
	center_y = range(0, HEIGHT, STEPSIZE)[int(TILE_XY_COUNT/2)]
	cursor = Cursor(center_x, center_y)

	#generating game board..
	# board = SquareGrid(WIDTH, HEIGHT)
	board = SquareGrid(TILE_XY_COUNT, TILE_XY_COUNT)
	# board = WeightedGrid(WIDTH, HEIGHT)
	#generating tiles 
	for row, x in zip(STARTING_BOARD, range(0, WIDTH, STEPSIZE)): 
		for health, y in zip(row, range(0, HEIGHT, STEPSIZE)):
			tiles.append(Tile(x, y, health))

	#spawning players	
	for player in player_start_positions: 
		players.append(Player(player_start_positions[player], player))
		board.blocked.append(vec(player_start_positions[player])//STEPSIZE)

	player_count = len(players)

	while run: 
		clock.tick(FPS) #makes sure the game runs at the frames set by FPS
		if not pygame.mixer.music.get_busy():
			songswitch=play_music(songswitch)


		if lost: 
			run = False
		
		#handeling player pause or quit input:
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

		redraw_window(tiles, players, cursor, lost, paused, board) 
		if not paused:
			count += 1
			if count == 3600: 
				run == False

			
			cursor.interact(count, board)

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
					tile_position = vec(tile.x, tile.y) // STEPSIZE
					board.blocked.append(tile_position)
					tiles.remove(tile)

			# if keys[pygame.K_SPACE]: 
			# 	player.shoot()

			player_turn = player_turn_count % player_count
			for player in players: 
				if player.player == players[player_turn].player: 
					player.active = True
					player_turn_count, player_turn = check4hotfeet(player, players, tiles, player_turn_count, player_turn)
					player.menu(cursor, WIN, tiles, players, lost, paused, board)
					if player.action_points <= 0: 
						player_turn_count += 1
						player.active = False
						player.action_points = 4
						for tile in tiles: 
							if player.contact(tile):
								tile.health -= 1
								player.hotfeet = False	
						if player.player == players[len(players)-1].player: 
							player_count = len(players)
						



			pygame.display.set_caption(f"Hotfeet, running at: {int(clock.get_fps())} fps") #Setting the name of the window
			
		



		

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

	
if __name__ == "__main__":
	main_menu()

