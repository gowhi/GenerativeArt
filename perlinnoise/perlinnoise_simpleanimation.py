import numpy as np
from perlin_noise import PerlinNoise
from PIL import Image

size = 200
frames = 60
octave_min = 1
octave_max = 6
steps = 20

images = []

print("Generating frames for animated Perlin noise...")
for f in range(frames):
    imgs = []
    for i in range(4):
        octave = octave_min + (f % steps) * (octave_max - octave_min) / steps
        noise = PerlinNoise(octaves=int(octave), seed=10*(i+1))
        offset = f / 50.0

        # Generar la imagen
        coords = np.indices((size, size)).transpose(1,2,0) / size
        img = np.zeros((size, size), dtype=np.uint8)
        for x in range(size):
            for y in range(size):
                val = noise([coords[x,y,0] + offset, coords[x,y,1] + offset])
                # Normalizar a 0-255
                img[x,y] = int((val + 1) / 2 * 255)
        imgs.append(img)

    # Combinar las 4 imágenes en 2x2
    top = np.hstack((imgs[0], imgs[1]))
    bottom = np.hstack((imgs[2], imgs[3]))
    combined = np.vstack((top, bottom))

    images.append(Image.fromarray(combined))

# Guardar GIF animado
images[0].save('perlin_animation.gif', save_all=True, append_images=images[1:], duration=100, loop=0)
print("GIF animated saved as 'perlin_animation.gif'")
