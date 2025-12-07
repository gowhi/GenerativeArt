# *********************************************
# Perlin Noise Generation and Visualization: Optimized Version
# ---------------------------------------------
# This script generates a 2D Perlin noise map and displays it using Matplotlib.
# The code has been optimized for better performance by precomputing normalized coordinates.    
# *********************************************

# Force the graphical backend
import matplotlib
# TkAgg is often more compatible across different systems
matplotlib.use("TkAgg")

# Show images and plots
import matplotlib.pyplot as plt
# Create matrixes and numerical operations
import numpy as np
# Generate Perlin noise
from perlin_noise import PerlinNoise

# Size of the individual images
size = 200

# Precompute normalized coordinates
# Optimization to avoid repeated division in the loop
coords = np.indices((size, size)).transpose(1,2,0) / size

# Create Perlin noise instance for generation of noise
# Octaves control the level of detail (fractality levels)
# Seed ensures reproducibility (same noise pattern on each run)
noises = [
    PerlinNoise(octaves=1, seed=10),
    PerlinNoise(octaves=2, seed=20),
    PerlinNoise(octaves=4, seed=30),
    PerlinNoise(octaves=6, seed=40)
]

# Generate images for each noise instance
imgs = []
for noise in noises:
    # Generate the map
    # 1. Normalize the coordinates [i/size]
    # 2. Get noise value at that coordinate [-1, 1]
    # 3. Store the value in the image matrix
    img = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            img[i,j] = noise(coords[i,j].tolist())  # Convert to list for PerlinNoise input
    imgs.append(img)

cmaps = ['inferno', 'viridis', 'plasma', 'magma']
# Initialize image matrix
img = np.zeros((size, size))

for i in range(size):
    for j in range(size):
        img[i,j] = noise(coords[i,j].tolist())  # Convert to list for PerlinNoise input

# # Display the generated Perlin noise image
# # 1. fig,axes creates a figure with multiple subplots
# # 2. figsize sets the overall size of the figure
# # 3. gridspec_kw removes spacing between subplots for a cleaner look
# fig, axes = plt.subplots(
#     2, 2,
#     figsize=(8, 8),
#     gridspec_kw={'wspace':0, 'hspace':0}
# )
# # 2. Loop through axes, images, and color maps to display each image
# for ax, img, cmap in zip(axes.flatten(), imgs, cmaps):
#     ax.imshow(img, cmap=cmap)
#     ax.axis('off')  # Hide axes

# plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
# # Show the final figure
# plt.show()

# Display the generated Perlin noise images in a 2x2 grid
# subplots creates a figure with multiple subplots
fig, axes = plt.subplots(2, 2, figsize=(8,8),
                         gridspec_kw={'wspace':0, 'hspace':0})

# Show each image in its respective subplot
for ax, img, cmap in zip(axes.flatten(), imgs, cmaps):
    ax.imshow(img, cmap=cmap, aspect='auto')  # aspect='auto' to fill the subplot
    ax.axis('off')  # Hide axes for cleaner look

plt.subplots_adjust(left=0, right=1, top=1, bottom=0)  # que ocupen todo el espacio
plt.show()
