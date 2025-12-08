# *********************************************
# ASCII Image Converter - Block method + Plot
# *********************************************

# ----------------------------------------
# Imports
# ----------------------------------------
import argparse # Argument parser
import numpy as np # Numerical operations
import matplotlib.pyplot as plt # Plotting
from PIL import Image, ImageEnhance # Image processing
import os

# Adjust sys.path to import custom modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in os.sys.path:
    os.sys.path.insert(0, parent_dir)

# import custom plotting function
try:
    from ploting import ploting  # Custom plotting function
except ImportError as e:
    print(f"Error importing ploting module: {e}")
    raise

# ----------------------------------------
# ASCII character sets
# ----------------------------------------
# 70-level grayscale
G_SCALE_FULL = r"&@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~i!lI;:,\"^`'. "
# 10-level grayscale
G_SCALE_SHORT = r"@%#*+=-:. "

# +++++++++++++++++++++++++++++++++
# FUNCTIONS
# +++++++++++++++++++++++++++++++++
# ----------------------------------------
# Average luminance of a block
# ----------------------------------------
# Function to compute average luminance of an image block
# Converts block to numpy array and computes average
# numpy is used for efficient numerical computation
# calcules the mean pixel value in the block
# Returns average luminance as a float
# ----------------------------------------
def get_avg_luminance(image_block):
    arr = np.array(image_block)
    return np.average(arr)

# ++++++++++++++++++++++++++++++
# MAIN
# ++++++++++++++++++++++++++++++
# ----------------------------------------
# Argument parsing: input image, columns, levels, contrast
# ----------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument("image", help="Input image")
parser.add_argument("--cols", type=int, default=120, help="Number of ASCII columns")
parser.add_argument("--multilevel", action="store_true", help="Use 70-level grayscale")
parser.add_argument("--contrast", type=float, default=1.5, help="Contrast boost")
args = parser.parse_args()

# Load image and preprocess enhancements:
# convert to grayscale with 'L' mode: luminance
# enhance contrast for better ASCII mapping
img = Image.open(args.image).convert("L")
img = ImageEnhance.Contrast(img).enhance(args.contrast)

width, height = img.size
# cols and rows for ASCII art dimensions
cols = args.cols
scale = 0.5  # vertical correction factor
# width between columns is for calculating block width
w = width / cols
# height between rows is for calculating block height
h = w / scale
# number of rows based on image height and block height
rows = int(height / h)

if rows <= 0:
    raise ValueError("Image too small for this number of columns.")

print(f"Image size: {width}x{height} → ASCII size: {cols}x{rows}")

# ----------------------------------------
# Convert to ASCII
# ----------------------------------------
ascii_img = []
# choose grayscale set based on user input
# gscale is length of vector of characters
gscale = G_SCALE_FULL if args.multilevel else G_SCALE_SHORT
# number of grayscale levels calculating length of vector - 1
levels = len(gscale) - 1

# Loop through image blocks
for row in range(rows):
    # y1 and y2 define the vertical boundaries of the block
    y1, y2 = int(row*h), int((row+1)*h)
    # append empty string for new row
    ascii_img.append("")

    # Loop through columns
    for i in range(cols):
        # x1 and x2 define the horizontal boundaries of the block
        x1, x2 = int(i*w), int((i+1)*w)
        # crop is PIL function to extract block from image
        block = img.crop((x1, y1, x2, y2))
        # get average luminance of the block
        avg = int(get_avg_luminance(block))
        # map average to grayscale character
        char = gscale[int((avg / 255) * levels)]
        # append character to the current row
        ascii_img[row] += char

# Join rows into single string with newlines
ascii_str = "\n".join(ascii_img)

# ----------------------------------------
# Showing and saving results
# ----------------------------------------
# Input image
img_arr = np.array(img)
ploting(img_arr, "Input Image", "gray")

# ASCII
scale_factor = 20  # Ajusta este valor para cambiar el tamaño de la imagen ASCII 
plot_width = cols / scale_factor
plot_height = (rows / scale_factor) * scale # Usamos 'scale' para compensar la altura del caracter

fig, ax = plt.subplots(figsize=(plot_width, plot_height))

ax.text(
    0, 1, ascii_str,
    fontfamily="monospace",
    fontsize=6, 
    ha="left",
    va="top",
    usetex=False 
)

ax.axis("off")


# Guardar solo ASCII
ascii_img_file = "ascii_only.png"
# Usar bbox_inches='tight' es crucial para eliminar el espacio extra alrededor del texto
fig.savefig(ascii_img_file, dpi=300, bbox_inches='tight', pad_inches=0.1)

plt.close(fig)

try:
    ascii_img_pil = Image.open(ascii_img_file)
except FileNotFoundError:
    print(f"Error: No se encontró el archivo de imagen: {ascii_img_file}")

ascii_img_arr = np.array(ascii_img_pil)
ploting(ascii_img_arr, "ASCII Art", None)


ascii_txt_file = "ascii_output.txt"
with open(ascii_txt_file, "w") as f:
    f.write(ascii_str)
print(f"ASCII art saved to {ascii_txt_file}")