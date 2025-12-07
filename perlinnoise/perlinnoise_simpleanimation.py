import matplotlib
matplotlib.use("Agg")  # Backend no interactivo para renderizar a archivo

import matplotlib.pyplot as plt
import numpy as np
from perlin_noise import PerlinNoise
from matplotlib.animation import FuncAnimation, PillowWriter

size = 200
coords = np.indices((size, size)).transpose(1,2,0) / size
cmaps = ['inferno', 'viridis', 'plasma', 'magma']

fig, axes = plt.subplots(2, 2, figsize=(8,8), gridspec_kw={'wspace':0, 'hspace':0})
for ax in axes.flatten():
    ax.axis('off')

imgs = [np.zeros((size, size)) for _ in range(4)]
ims = [axes.flatten()[i].imshow(imgs[i], cmap=cmaps[i], aspect='auto') for i in range(4)]

# Range of octaves for animation
octave_min = 1
octave_max = 6
steps = 20

# Update function for animation
# 1. For each frame, update the octave value
# 2. Regenerate the Perlin noise image for each subplot
# 3. Update the image data in the respective AxesImage object
# 4. Return the updated images for blitting
# This creates a smooth transition of noise patterns over time
def update(frame):
    for i in range(4):
        octave = octave_min + (frame % steps) * (octave_max - octave_min) / steps
        noise = PerlinNoise(octaves=int(octave), seed=10*(i+1))
        offset = frame / 101.0  # Smooth offset for animation
        img = np.zeros((size, size))
        for x in range(size):
            for y in range(size):
                coord = [coords[x, y, 0] + offset, coords[x, y, 1] + offset]
                img[x, y] = noise(coord)
        ims[i].set_data(img)
    return ims

# Create the animation object with FuncAnimation
# 1. fig is the figure to animate
# 2. update is the function called for each frame
# 3. frames is the total number of frames in the animation
# 4. interval sets the delay between frames in milliseconds
# 5. blit=True optimizes rendering by only redrawing changed parts
print("Generating animation...")
ani = FuncAnimation(fig, update, frames=60, interval=100, blit=False)

# Save the animation as a GIF
writer = PillowWriter(fps=10)
ani.save("perlin_animation.gif", writer=writer)
print("GIF saved as perlin_animation.gif")
