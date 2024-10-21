from PIL import Image
import os
import subprocess
import multiprocessing

def remove_readonly(folder_path):
    subprocess.run(['attrib', '-R', folder_path])
    subprocess.run(['attrib', '-R', f"{folder_path}\\*.*", '/S'])

def delete_files_with_extension_batch(files):
    for file in files:
        os.remove(file)
        print(f"Deleted: {file}")

def delete_files_with_keywords_batch(files):
    deleteKeywords = load_delete_keywords()  # Load delete keywords
    for file in files:
        base_name = os.path.basename(file).lower()  # Get file's base name
        deleteKeywords_lower = [keyword.lower() for keyword in deleteKeywords]  # Convert keywords to lowercase for case-insensitive match
        
        if base_name in deleteKeywords_lower:
            try:
                os.remove(file)
                print(f"Deleted file based on keyword match: {file}")
            except Exception as e:
                print(f"Failed to delete {file}. Error: {e}")


def remove_empty_folders(root_folder):
    for subdir, dirs, _ in os.walk(root_folder, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(subdir, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
                print(f"Deleted empty folder: {dir_path}")

def load_delete_keywords():
    try:
        with open("exclusions.txt", "r") as file:
            content = file.read()
        keywords = [line.strip() for line in content.splitlines()]  # Trim each keyword
        return keywords
    except Exception as e:
        print(f"Error loading delete keywords from exclusions.txt: {e}")
        return []
    

def optimize_images_in_batch(image_batch, target_width=1920, target_height=1080, initial_quality=85, max_file_size=1024*1024):
   
    for image_path in image_batch:       
        if os.path.getsize(image_path) < max_file_size:
            continue
 
        try:
            with Image.open(image_path) as img:
                # Check the image's orientation (landscape or portrait)
                if img.width > img.height:  # Landscape
                    aspect_ratio = img.width / img.height
                    new_width = min(target_width, img.width)  # Don't upscale images
                    new_height = int(new_width / aspect_ratio)
                else:  # Portrait
                    aspect_ratio = img.height / img.width
                    new_height = min(target_height, img.height)  # Adjusted for portrait and don't upscale
                    new_width = int(new_height / aspect_ratio)

                # Resize the image
                img = img.resize((new_width, new_height), Image.LANCZOS)

                # Save the image with the initial quality
                quality = initial_quality
                img.save(image_path, quality=quality)

                # If the image file size is still above the max limit, reduce the quality iteratively
                while os.path.getsize(image_path) > max_file_size and quality > 10:
                    quality -= 2  # Reduce quality by 5 units
                    img.save(image_path, quality=quality)

                # If the image is STILL above the limit after quality reduction, downscale it to 720p
                if os.path.getsize(image_path) > max_file_size and max(new_width, new_height) > 720:
                    if new_width > new_height:
                        new_width = 720
                        new_height = int(new_width / aspect_ratio)
                    else:
                        new_height = 720
                        new_width = int(new_height / aspect_ratio)
                    
                    img = img.resize((new_width, new_height), Image.LANCZOS)
                    quality = initial_quality  # Reset to initial quality
                    img.save(image_path, quality=quality)

                    # If the image file size is still above the max limit even after resizing, reduce the quality again
                    while os.path.getsize(image_path) > max_file_size and quality > 10:
                        quality -= 5
                        img.save(image_path, quality=quality)

            print(f"Optimized {image_path}")
        except Exception as e:
            print(f"Failed to optimize {image_path}. Error: {e}")



if __name__ == "__main__":
    folder_path = input("Please enter the path to your folder: ")

    # Remove the read-only attribute
    remove_readonly(folder_path)

    # Delete files based on keywords using multiprocessing
    files_to_delete_based_on_keywords = [os.path.join(subdir, file) 
                                         for subdir, _, files in os.walk(folder_path) 
                                         for file in files]
    
    num_processes = multiprocessing.cpu_count()
    files_batched = [files_to_delete_based_on_keywords[i::num_processes] for i in range(num_processes)]

    with multiprocessing.Pool(processes=num_processes) as pool:
        pool.map(delete_files_with_keywords_batch, files_batched)

    # Delete specific file extensions using multiprocessing
    files_to_delete = [os.path.join(subdir, file) 
                       for subdir, _, files in os.walk(folder_path) 
                       for file in files 
                       if file.lower().endswith(('.mp4', '.mkv', '.flv', '.mov', '.avi', '.wmv', '.pdf', '.url', '.ts', '.txt', '.webm'))]

    num_processes = multiprocessing.cpu_count()
    files_batched = [files_to_delete[i::num_processes] for i in range(num_processes)]

    with multiprocessing.Pool(processes=num_processes) as pool:
        pool.map(delete_files_with_extension_batch, files_batched)

    # Optimize the images using multiprocessing
    image_files = [os.path.join(subdir, file) 
                    for subdir, _, files in os.walk(folder_path) 
                    for file in files 
                    if file.lower().endswith(('.png', '.jpg', '.jpeg'))]

    image_file_batches = [image_files[i::num_processes] for i in range(num_processes)]

    with multiprocessing.Pool(processes=num_processes) as pool:
        pool.map(optimize_images_in_batch, image_file_batches)

    # Remove empty folders
    remove_empty_folders(folder_path)

    print("Operations completed!")
