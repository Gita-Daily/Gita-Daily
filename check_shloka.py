import json
import os
import glob

import openai
import time

cnt = 0
total_files = 0

for folder_number in range(1, 19):
    folder_path = str(folder_number)

    json_files = glob.glob(f"{folder_path}/*.json")

    for file_path in json_files:
        try: 
            with open(file_path, 'r') as file:
                contents = json.load(file)

                total_files += 1
                
                if "newest_commentary" in contents:
                    commentary = contents["newest_commentary"]
                elif "new_commentary" in contents:
                    commentary = contents["new_commentary"]
                else:
                    print(f"No suitable commentary found in file {file_path}")
                    continue

                verse = contents.get("verse", "")
                translation = contents.get("translation", "")
                
                extra_fluff = "*Chapter 12 Verse 1*\n\n\n\n*Translation*\n\n*Commentary*\n\nCreated by www.gitadaily.in"

                remaining_length = 1024 - len(verse) - len(translation) - len(extra_fluff) - len(commentary) - 10

                if remaining_length < 0:
                    print(f'this file {file_path} has commentary length of {len(commentary)} / {remaining_length}')
                    cnt += 1
        except Exception as e:
            print(f'Error with file {file_path}: {e}')
            continue


print(f"Total files with commentary length > 1024: {cnt} / {total_files}")