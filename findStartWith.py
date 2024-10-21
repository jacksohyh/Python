import os

def find_files_with_prefix(directory, prefix):
    matching_files = []

    # Traverse the directory and add files that match the prefix
    for root, _, files in os.walk(directory):
        for file in files:
            if file.startswith(prefix):
                matching_files.append(file)
    return matching_files

if __name__ == "__main__":
    directory_to_search = input("Enter the directory to search: ").strip()
    prefix = input("Input prefix to search: ").strip()  # Added strip for prefix input
    matching_files = find_files_with_prefix(directory_to_search, prefix)

    if matching_files:
        print(f"\nFiles starting with '{prefix}':")
        for file_name in matching_files:
            print(file_name)
    else:
        print(f"\nNo files found starting with '{prefix}'")
