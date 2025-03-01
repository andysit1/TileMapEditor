import os

# Dynamically determine the number of tile types
tile_files = [f for f in os.listdir('img/tile') if f.endswith(('.png', '.jpg'))]
TILE_TYPES = len(tile_files)

print(TILE_TYPES)
