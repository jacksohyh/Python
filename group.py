import os
import shutil

# Prompt the user to input the folder path
base_folder_path = input("Please enter the base folder path containing the numbered folders: ").strip()

# Extract the last folder name from the base folder path
destination_folder_name = os.path.basename(base_folder_path)

# Check if the base folder path exists
if not os.path.exists(base_folder_path):
    print("The specified folder path does not exist. Please try again.")
else:
    # Create the destination folder inside the base folder path
    dest_folder_path = os.path.join(base_folder_path, destination_folder_name)
    os.makedirs(dest_folder_path, exist_ok=True)

    current_index = 0  # To keep track of the sequential number

    # Get the sorted list of folders by their numeric name
    folders = sorted([f for f in os.listdir(base_folder_path) if os.path.isdir(os.path.join(base_folder_path, f)) and f.isdigit()], key=lambda x: int(x))

    # Iterate through each folder and copy/rename the files
    for folder in folders:
        folder_path = os.path.join(base_folder_path, folder)

        # Get the list of files in the folder
        files = sorted([f for f in os.listdir(folder_path) if f.endswith(('png', 'jpg', 'jpeg'))])

        for file_name in files:
            # Construct the source file path
            src_path = os.path.join(folder_path, file_name)

            # Construct the destination file path with the new sequential name
            dest_file_name = f"{current_index:03d}.jpg"  # Change extension if needed
            dest_path = os.path.join(dest_folder_path, dest_file_name)

            # Copy the file to the destination folder with the new name
            shutil.copy(src_path, dest_path)

            # Increment the index for the next file
            current_index += 1

    print(f"Files have been successfully copied and renamed in the '{destination_folder_name}' folder.")
