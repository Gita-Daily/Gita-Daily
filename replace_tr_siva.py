import os
import json
import re

# Number of files in each directory
chapter_shlokas = [
    47, 72, 43, 42, 29, 47, 30, 28, 34, 42, 55, 20, 34, 27, 20, 24, 28, 78
]


# Iterate through each directory
for dir_num in range(1, 19):
    dir_path = f'{dir_num}/'

    # Check if the directory exists
    if os.path.exists(dir_path):
        # Iterate over the specific number of files in the directory
        for file_num in range(1, chapter_shlokas[dir_num-1] + 1):
            file_path = os.path.join(dir_path, f'{file_num}.json')

            # Open and read the JSON file
            try:
                with open(file_path, 'r') as json_file:
                    data = json.load(json_file)
                    next_shloka = data['next shlok']
                    final_tr = ''
                    for i in range(file_num, next_shloka):
                        siva_path = 'Sivananda/' + dir_path + f'{i}.json'
                        with open(siva_path, 'r') as siva_file:
                            siva_data = json.load(siva_file)
                            s_tr = siva_data['translation']
                            extracted_text = s_tr.split(' ', 1)[1]
                            final_tr = final_tr + extracted_text

                with open(file_path, 'r') as json_file:
                    data = json.load(json_file)
                    data['translation'] = final_tr
                    with open(file_path, 'w') as json_file:
                        json.dump(data, json_file, indent=4)




            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
    else:
        print(f"Directory {dir_path} does not exist.")
