import matplotlib.pyplot as plt
import numpy as np

def ploting(image, title, cmap):
    try:
        if image.ndim == 2:  # Grayscale image
            plt.imshow(image, cmap='gray')
        else:
            plt.imshow(image, cmap=cmap)
        
        plt.title(title)
        plt.axis('off')
        plt.show()
        
    except Exception as e:
        print(f"Error displaying image: {e}")