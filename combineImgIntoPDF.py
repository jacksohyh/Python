from PIL import Image
import os
import re

# Set the folder path (replace with your own path)
folder_path = input('Input folder name: ')

# Extract folder name for the PDF file name
folder_name = os.path.basename(folder_path)
output_pdf_path = os.path.join(folder_path, f"{folder_name}.pdf")

# Natural sorting function to handle alphanumeric filenames correctly
def natural_sort_key(text):
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r'(\d+)', text)]

# Get all image file paths, sorted in natural order
image_files = [f for f in os.listdir(folder_path) if f.endswith(('png', 'jpg', 'jpeg'))]
image_files.sort(key=natural_sort_key)  # Sort the files naturally

# Open images and convert them to RGB
images = []
for file in image_files:
    image_path = os.path.join(folder_path, file)
    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    images.append(img)

# Save images as a single PDF
if images:
    images[0].save(output_pdf_path, save_all=True, append_images=images[1:])
    print(f'PDF saved successfully at {output_pdf_path}')
else:
    print('No images found in the specified folder.')
