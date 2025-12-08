import os
import argparse
from PIL import Image
import imageio.v2 as imageio 
import numpy as np

def create_gif_from_directory(
    directory,
    output_filename="output.gif",
    rows=1,
    cols=1,
    canvas_width=800,
    canvas_height=600,
    image_size=(300, 200),
    frame_duration=0.5,
    loop=0
):
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' not found.")
        return

    image_files = [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))
    ]

    if not image_files:
        print(f"No images found in directory '{directory}'.")
        return

    frames = []
    
    images_per_page = rows * cols
    cell_width = canvas_width // cols
    cell_height = canvas_height // rows
    
    target_width, target_height = image_size
    
    num_pages = (len(image_files) + images_per_page - 1) // images_per_page
    
    for page_index in range(num_pages):
        canvas = Image.new('RGB', (canvas_width, canvas_height), (255, 255, 255))
        start_index = page_index * images_per_page
        
        for r in range(rows):
            for c in range(cols):
                current_image_index = start_index + r * cols + c
                
                if current_image_index < len(image_files):
                    try:
                        img_path = image_files[current_image_index]
                        img = Image.open(img_path).convert('RGB')
                        
                        # --- CORRECCIÓN DE PROPORCIÓN (FIT/ENCAJAR) ---
                        original_width, original_height = img.size
                        width_ratio = target_width / original_width
                        height_ratio = target_height / original_height
                        fit_ratio = min(width_ratio, height_ratio)
                        new_width = int(original_width * fit_ratio)
                        new_height = int(original_height * fit_ratio)
                        img_resized = img.resize((new_width, new_height), Image.LANCZOS)
                        
                        # --- CÁLCULO DE POSICIÓN Y CENTRADO EN LA CELDA ---
                        cell_x = c * cell_width
                        cell_y = r * cell_height
                        x_offset = cell_x + (cell_width - new_width) // 2
                        y_offset = cell_y + (cell_height - new_height) // 2
                        
                        canvas.paste(img_resized, (x_offset, y_offset))
                    except Exception as e:
                        print(f"No se pudo procesar la imagen {image_files[current_image_index]}: {e}")
                        
        frames.append(np.array(canvas)) # ⬅️ ¡CORRECCIÓN APLICADA!
    
    if not frames:
        print("No se pudieron crear frames para el GIF.")
        return

    # Guardar el GIF
    try:
        # imageio recibe ahora la lista de arrays de píxeles (NumPy)
        durations_list = [frame_duration] * len(frames)
        imageio.mimsave(output_filename, frames, duration=durations_list, loop=loop)
        print(f"GIF '{output_filename}' creado exitosamente con {len(frames)} frames/páginas.")
    except Exception as e:
        print(f"Error al guardar el GIF: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crea un GIF animado a partir de imágenes en un directorio.")
    parser.add_argument("directory", type=str, help="Ruta al directorio de las imágenes.")
    parser.add_argument("--output", type=str, default="output.gif", help="Nombre del archivo GIF de salida.")
    parser.add_argument("--rows", type=int, default=3, help="Número de filas en la cuadrícula del canvas.")
    parser.add_argument("--cols", type=int, default=3, help="Número de columnas en la cuadrícula del canvas.")
    parser.add_argument("--canvas_width", type=int, default=800, help="Ancho del lienzo del GIF.")
    parser.add_argument("--canvas_height", type=int, default=600, help="Alto del lienzo del GIF.")
    parser.add_argument("--image_width", type=int, default=300, help="Ancho al que se redimensionará cada imagen para el frame.")
    parser.add_argument("--image_height", type=int, default=200, help="Alto al que se redimensionará cada imagen para el frame.")
    parser.add_argument("--duration", type=float, default=0.5, help="Duración de cada frame en segundos.")
    parser.add_argument("--loop", type=int, default=0, help="Número de veces que el GIF debe repetirse. 0 para infinito.")

    args = parser.parse_args()

    # Combinamos image_width y image_height en una tupla para image_size
    image_size_tuple = (args.image_width, args.image_height)

    # Llama a la función principal con los argumentos
    create_gif_from_directory(
        args.directory,
        output_filename=args.output,
        rows=args.rows,
        cols=args.cols,
        canvas_width=args.canvas_width,
        canvas_height=args.canvas_height,
        image_size=image_size_tuple,
        frame_duration=args.duration,
        loop=args.loop
    )