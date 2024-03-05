import math
import os
import random
from PIL import Image as Img
from PIL.Image import Image

def resize_images(images: list[list[Image]], target_size: tuple[int, int]) -> list[list[Image]]:
  resized_images: list[list[Image]] = []
  for row in images:
    resized_row: list[Image] = []
    for img in row:
      resized_row.append(img.resize(target_size))
    resized_images.append(resized_row)
  return resized_images

def calculate_target_size(images: list[list[Image]], collage_width: int, collage_height: int, rows: int, cols: int, margin: int) -> tuple[int, int]:
  max_width = max(img.size[0] for row in images for img in row)
  max_height = max(img.size[1] for row in images for img in row)
  
  available_width = collage_width - (margin * 2) * (cols + 1)
  available_height = collage_height - (margin * 2) * (rows + 1)
  
  scale = min(available_width / (max_width * cols), available_height / (max_height * rows))
  target_width = int(max_width * scale)
  target_height = int(max_height * scale)
  
  return target_width, target_height

def create_collage(images: list[list[Image]], output_path, collage_width=1920, collage_height=1080, collage_padding=100, margin=20, bg_color=(255, 255, 255)) -> None:
  rows = len(images)
  cols = len(images[0])

  target_size = calculate_target_size(images, collage_width - (collage_padding * 2), collage_height - (collage_padding * 2), rows, cols, margin)
  print(target_size)

  resized_images = resize_images(images, target_size)

  total_width = collage_width
  total_height = collage_height

  collage = Img.new('RGB', (total_width, total_height), color=bg_color)
  
  y_grid_offset = (collage_height - (collage_padding * 2) - (target_size[1] * rows + (margin * 2) * rows - 1)) // 2
  x_grid_offset = (collage_width - (collage_padding * 2) - (target_size[0] * cols + (margin * 2) * cols - 1)) // 2

  y_offset = margin + y_grid_offset + collage_padding
  for row in resized_images:
    x_offset = margin + x_grid_offset + collage_padding
    for img in row:
        collage.paste(img, (x_offset, y_offset))
        x_offset += img.size[0] + margin * 2
    y_offset += target_size[1] + margin * 2
  
  collage.save(output_path)

def get_images_from_folder(folder_path: str) -> list[str]:
  try:
    files = [os.path.join(folder_path, fn) for fn in os.listdir(folder_path)]
    images = [fn for fn in files if os.path.splitext(fn)[1].lower() in ('.jpg', '.jpeg', '.png')]
    return images
  except Exception as e:
    print(f"Error: {e}")
    return []

def run_script(folders: list[str]) -> None: 
  images = []
  for folder in folders:
    images += get_images_from_folder("images/" + folder)

  if not images:
    raise Exception('No images found in the specified folders')
  
  random.shuffle(images)

  total_images = len(images)
  cols = int(math.sqrt(total_images))
  rows = int(math.ceil(total_images / cols))
  
  images_matrix = []
  for i in range(0, total_images, rows):
    images_matrix.append([Img.open(img) for img in images[i:i + rows]])

  print('Making collage...')
  create_collage(images_matrix, "collage.tiff")
  print('Collage is ready!')

def main() -> None:
  folders = ["1369_12_Наклейки 3-D_3"]
  try:
    run_script(folders)
  except Exception as e:
    print(f"Error: {e}")
  
if __name__ == '__main__':
  main()