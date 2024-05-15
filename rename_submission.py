import os
import pandas as pd
import argparse

def rename_files(folder_path, roster_file):
    # Load the roster file
    roster = pd.read_csv(roster_file)
    id_to_fname_map = dict(zip(roster['ID'], roster['Integration ID']))
    
    # Loop through each file in the directory
    for filename in os.listdir(folder_path):
        # Extract the ID from the filename
        parts = filename.split('_')
        if len(parts) > 1:
            if parts[1] == "LATE":
                id_part = int(parts[2])
            else:
                id_part = int(parts[1])
            if id_part in id_to_fname_map:
                # Build new filename using the ID and the original file extension
                file_extension = os.path.splitext(filename)[1]
                new_filename = f"{id_to_fname_map[id_part]}{file_extension}"
                old_file_path = os.path.join(folder_path, filename)
                new_file_path = os.path.join(folder_path, new_filename)
                
                # Rename the file
                os.rename(old_file_path, new_file_path)
                print(f"Renamed {filename} to {new_filename}")
            else:
                print(f"No School ID found for Canvas ID {id_part} in file {filename}")
        else:
            print(f"Filename format is incorrect: {filename}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rename the submission files to School ID.')
    parser.add_argument('folder', type=str, help='Path to the final grade sheet.')
    parser.add_argument('roster', type=str, help='Path to the roster CSV file.')
    args = parser.parse_args()

    rename_files(args.folder, args.roster)