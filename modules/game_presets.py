import numpy as np
import pygame
import os
vec = pygame.math.Vector2


#BoardState
STARTING_BOARD = np.array([
	[3, 3, 2, 2, 2, 3, 2, 2, 2, 3, 3],
	[3, 1, 1, 2, 3, 3, 3, 2, 1, 1, 3], 
	[2, 1, 1, 2, 3, 3, 3, 2, 1, 1, 2], 
	[2, 2, 2, 3, 3, 3, 3, 3, 2, 2, 2],
	[2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2],
	[3, 3, 3, 3, 3, 5, 3, 3, 3, 3, 3],
	[2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2],
	[2, 2, 2, 3, 3, 3, 3, 3, 2, 2, 2],
	[2, 1, 1, 2, 3, 3, 3, 2, 1, 1, 2], 
	[3, 1, 1, 2, 3, 3, 3, 2, 1, 1, 3],
	[3, 3, 2, 2, 2, 3, 2, 2, 2, 3, 3], 
	])


TILE_XY_COUNT = STARTING_BOARD.shape[0]
STEPSIZE = 65
WIDTH = STEPSIZE*TILE_XY_COUNT
HEIGHT = WIDTH 


#Window
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #WIDTH and HEIGHT are now being defined in the ships module.. This is weird, should be in main.. 

#background
BACKGROUND = pygame.image.load(os.path.join("assets", "images", "lava_bg.png"))
BACKGROUND = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT)) # resizing the background to the width and height of the window



pygame.font.init()
TILE_FONT = pygame.font.SysFont("comicsans", 20)
PLAYER_FONT = pygame.font.SysFont("comicsans", 25)
MENU_FONT = pygame.font.SysFont("comicsans", 25)
MAIN_FONT = pygame.font.SysFont("comicsans", 50)
LOST_FONT = pygame.font.SysFont("comicsans", 40)

ARROWS = {}
arrow_img = pygame.image.load(os.path.join("assets", "images", 'arrowRight.png')).convert_alpha()
arrow_img = pygame.transform.scale(arrow_img, (STEPSIZE, STEPSIZE))
for dir in [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
    ARROWS[dir] = pygame.transform.rotate(arrow_img, vec(dir).angle_to(vec(1, 0)))

if __name__ == "__main__":
	for row, x in zip(STARTING_BOARD, range(3, WIDTH, int(WIDTH/TILE_XY_COUNT))): 
		for health, y in zip(row, range(3, HEIGHT, int(HEIGHT/TILE_XY_COUNT))):
			print (health)




