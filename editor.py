import pygame
import button
import csv
import pickle
import os



pygame.init()

clock = pygame.time.Clock()
FPS = 60

# game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
LOWER_MARGIN = 100
SIDE_MARGIN = 300

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('Level Editor')

# define game variables
ROWS = 16
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS


# Dynamically determine the number of tile types
tile_files = [f for f in os.listdir('img/tile') if f.endswith(('.png', '.jpg'))]
TILE_TYPES = len(tile_files)
level = 0
current_tile = 0
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 4
preview_mode = False

# load images
pine1_img = pygame.image.load('img/Background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('img/Background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('img/Background/mountain.png').convert_alpha()
sky_img = pygame.image.load('img/Background/sky_cloud.png').convert_alpha()

# store tiles in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'img/tile/{x}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

save_img = pygame.image.load('img/save_btn.png').convert_alpha()
load_img = pygame.image.load('img/load_btn.png').convert_alpha()
preview_img = pygame.image.load('img/load_btn.png').convert_alpha()

# define colours
GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

# define font
font = pygame.font.SysFont('Futura', 30)

# create empty tile list
world_data = [[[-1 for _ in range(MAX_COLS)] for _ in range(ROWS)] for _ in range(4)]  # 4 layers

# create ground
for tile in range(0, MAX_COLS):
    world_data[0][ROWS - 1][tile] = 0

# function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# create function for drawing background
def draw_bg():
    screen.fill(GREEN)
    width = sky_img.get_width()
    for x in range(4):
        screen.blit(sky_img, ((x * width) - scroll * 0.5, 0))
        screen.blit(mountain_img, ((x * width) - scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 300))
        screen.blit(pine1_img, ((x * width) - scroll * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
        screen.blit(pine2_img, ((x * width) - scroll * 0.8, SCREEN_HEIGHT - pine2_img.get_height()))

# draw grid
def draw_grid():
    for c in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, SCREEN_HEIGHT))
    for c in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))

# function for drawing the world tiles
def draw_world():
    for layer_index, layer in enumerate(world_data):
        opacity = 255 if preview_mode or layer_index == level else 128  # Opaque for inactive layers, full in preview
        for y, row in enumerate(layer):
            for x, tile in enumerate(row):
                if tile >= 0:
                    tile_img = img_list[tile].copy()
                    tile_img.set_alpha(opacity)
                    screen.blit(tile_img, (x * TILE_SIZE - scroll, y * TILE_SIZE))

# create buttons
save_button = button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 50, save_img, 1)
load_button = button.Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 50, load_img, 1)
preview_button = button.Button(SCREEN_WIDTH // 2 + 400, SCREEN_HEIGHT + LOWER_MARGIN - 50, preview_img, 1)

button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
    tile_button = button.Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, img_list[i], 1)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = 0

run = True
while run:
    clock.tick(FPS)
    draw_bg()
    draw_grid()
    draw_world()

    draw_text(f'Level: {level}', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
    draw_text('Press UP or DOWN to change level', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 60)

    if save_button.draw(screen):
        for l in range(4):

            with open(f'level{l}_data.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                for row in world_data[l]:
                    writer.writerow(row)

    if load_button.draw(screen):
        scroll = 0
        for l in range(4):
            with open(f'level{l}_data.csv', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                        world_data[l][x][y] = int(tile)

    if preview_button.draw(screen):
        preview_mode = not preview_mode

    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count
    pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

    if scroll_left and scroll > 0:
        scroll -= 5 * scroll_speed
    if scroll_right and scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
        scroll += 5 * scroll_speed

    pos = pygame.mouse.get_pos()
    x = (pos[0] + scroll) // TILE_SIZE
    y = pos[1] // TILE_SIZE
    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
        if pygame.mouse.get_pressed()[0]:
            world_data[level][y][x] = current_tile
        if pygame.mouse.get_pressed()[2]:
            world_data[level][y][x] = -1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level = min(level + 1, 3)
            if event.key == pygame.K_DOWN:
                level = max(level - 1, 0)
            if event.key == pygame.K_a:
                scroll_left = True
            if event.key == pygame.K_d:
                scroll_right = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                scroll_left = False
            if event.key == pygame.K_d:
                scroll_right = False

    pygame.display.update()
pygame.quit()
