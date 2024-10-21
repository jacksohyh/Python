import os
import pandas as pd

def rename_files_from_excel(input_folder, excel_file):
    # Load the Excel file
    df = pd.read_excel(excel_file, usecols=[0, 1], header=None, engine='openpyxl')
    df.columns = ['Old Name', 'New Name']

    # Iterate over all files in the input folder and subfolders
    for root, _, files in os.walk(input_folder):
        for file in files:
            # Check if the current file matches any in column A (Old Name)
            old_name = df['Old Name']
            if file in old_name.values:
                # Find the corresponding new name from column B
                new_name = df.loc[df['Old Name'] == file, 'New Name'].values[0]

                # Ensure new name has the .mp4 extension
                if not new_name.lower().endswith('.mp4'):
                    new_name += '.mp4'

                # Construct the old and new file paths
                old_path = os.path.join(root, file)
                new_path = os.path.join(root, new_name)

                # Rename the file
                os.rename(old_path, new_path)
                print(f"Renamed: {old_path} -> {new_path}")

if __name__ == "__main__":
    # Prompt user for input folder and Excel file paths
    input_folder = input("Enter the input folder path: ").strip()
    excel_file = "mapfile.xlsx"

    # Rename files based on the Excel file
    rename_files_from_excel(input_folder, excel_file)
    print("File renaming completed.")
