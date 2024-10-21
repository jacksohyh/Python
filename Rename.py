import os
import re

# Prompt the user to input the folder path
folder_path = input("Please enter the folder path: ").strip()

# Offset to add to the current numbers in filenames
offset = 0
temp_prefix = "TEMP_"

# Check if the folder path exists
if not os.path.exists(folder_path):
    print("The specified folder path does not exist. Please try again.")
else:
    # Step 1: Add temporary prefix to all files to avoid conflicts (including subdirectories)
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith(('png', 'jpg', 'jpeg')):
                old_path = os.path.join(root, file_name)
                new_path = os.path.join(root, temp_prefix + file_name)
                os.rename(old_path, new_path)

    # Step 2: Regular expression to match the numerical part of the filename
    number_pattern = re.compile(r'^TEMP_.*?(\d+).*?\.(jpg|jpeg|png)$', re.IGNORECASE)

    # Iterate over all files in the folder after adding the temporary prefix (including subdirectories)
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            # Match the filename pattern to extract the numerical part
            match = number_pattern.match(file_name)
            if match:
                # Extract the numerical part
                number_str, extension = match.groups()
                
                # Calculate the new number with the offset
                new_number = int(number_str) + offset
                
                # Construct the new filename with only the new number
                new_file_name = f"{new_number:03d}.{extension}"
                new_path = os.path.join(root, new_file_name)
                old_path = os.path.join(root, file_name)

                # Rename the file to the new name
                os.rename(old_path, new_path)

    print('Files renamed successfully.')
