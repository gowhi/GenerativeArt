
# *********************************************
# Perlin Noise Generation and Visualization: Noob Version
# ---------------------------------------------
# This script generates a 2D Perlin noise map and displays it using Matplotlib.
# *********************************************

# Force the graphical backend
import matplotlib
matplotlib.use("QtAgg") 

# Show images and plots
import matplotlib.pyplot as plt
# Create matrixes and numerical operations
import numpy as np
# Generate Perlin noise
from perlin_noise import PerlinNoise

# Create Perlin noise instance for generation of noise
# Octaves control the level of detail (fractality levels)
# Seed ensures reproducibility (same noise pattern on each run)
noise = PerlinNoise(octaves=4, seed=123)

# Size of the image
size = 300
img = np.zeros((size, size))

# Generate the map
# 1. Normalize the coordinates [i/size]
# 2. Get noise value at that coordinate [-1, 1]
# 3. Store the value in the image matrix
for i in range(size):
    for j in range(size):
        img[i][j] = noise([i/size, j/size])
# Display the generated Perlin noise image
# 1. imshow shows the matrix as an image
# 2. cmap='inferno' applies a color map for better visualization
# 3. axis('off') hides the axes for a cleaner look
# 4. show() renders the image on screen
plt.imshow(img, cmap='inferno')
plt.axis('off')
plt.show()