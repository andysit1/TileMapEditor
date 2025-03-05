import pygame
import csv
scroll = 0

#game window
FPS = 60
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
ROWS = 16
MAX_COLS = 150
TILE_TYPES = 21
TILE_SIZE = SCREEN_HEIGHT // ROWS


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Loaded Map')
world_data = [[[-1 for _ in range(MAX_COLS)] for _ in range(ROWS)] for _ in range(4)]  # 4 layers

img_list = []
for x in range(TILE_TYPES):
	img = pygame.image.load(f'img/tile/{x}.png').convert_alpha()
	img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
	img_list.append(img)


#load data
for l in range(4):
    with open(f'level{l}_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                world_data[l][x][y] = int(tile)

# function for drawing the world tiles
def draw_world():
    for layer_index, layer in enumerate(world_data):
        opacity = 255
        for y, row in enumerate(layer):
            for x, tile in enumerate(row):
                if tile >= 0:
                    tile_img = img_list[tile].copy()
                    tile_img.set_alpha(opacity)
                    screen.blit(tile_img, (x * TILE_SIZE - scroll, y * TILE_SIZE))

clock = pygame.time.Clock()

while True:
    clock.tick(FPS)
    draw_world()
    pygame.display.update()
