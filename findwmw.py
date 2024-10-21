import os
import fnmatch

def find_non_mp4_videos(directory):
    # List to store paths of non-.mp4 files
    non_mp4_videos = []

    # Walk through directory and subdirectories
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file is not an .mp4
            if not fnmatch.fnmatch(file, '*.mp4'):
                # Get full path of the non-.mp4 file
                full_path = os.path.join(root, file)
                non_mp4_videos.append(full_path)

    return non_mp4_videos

if __name__ == "__main__":
    # Define the folder where you want to search for non-.mp4 files
    folder_to_search = input("Enter folder: ") 
    
    # Find non-.mp4 videos
    non_mp4_files = find_non_mp4_videos(folder_to_search)
    
    # Print out the found non-.mp4 video files
    if non_mp4_files:
        print("Found non-.mp4 videos:")
        for video in non_mp4_files:
            print(video)
    else:
        print("No non-.mp4 videos found.")
