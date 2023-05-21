import json
import os

def split_json(file_path, split_size):
    print("begining")
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    print("loaded")
    total_items = len(data)
    items_per_split = total_items // split_size

    for i in range(split_size):
        start_index = i * items_per_split
        end_index = (i + 1) * items_per_split
        split_data = data[start_index:end_index]

        split_file_path = f'split_{i}.json'
        with open(split_file_path, 'w') as split_file:
            json.dump(split_data, split_file, indent=2)

        print(f'Saved {split_file_path}')

    print('Splitting complete.')

# Usage
file_path = '/Users/jackmelleuish/Documents/GitHub/CCC2023_A2_Team_51/twitter-huge.json.zip'
split_size = 10  # Number of splits desired
split_json(file_path, split_size)
