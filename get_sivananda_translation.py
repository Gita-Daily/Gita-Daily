import requests
import json
import os

# The base URL for the API
base_url = "https://bhagavadgitaapi.in/slok/"

# Number of verses in each chapter of the Bhagavad Gita
chapter_shlokas = [
    47, 72, 43, 42, 29, 47, 30, 28, 34, 42, 55, 20, 34, 27, 20, 24, 28, 78,
]

# Function to fetch data and save it to files
def fetch_gita_data():
    base_dir = "Sivananda"
    os.makedirs(base_dir, exist_ok=True)

    for chapter, num_verses in enumerate(chapter_shlokas, start=1):
        chapter_dir = os.path.join(base_dir, str(chapter))
        os.makedirs(chapter_dir, exist_ok=True)
        print(f"Chapter {chapter}:")

        for verse in range(1, num_verses + 1):
            url = f"{base_url}{chapter}/{verse}/"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                verse_text = data['siva']['et']
                print(f"  Verse {verse}: {verse_text}")

                # Saving the verse text to a file
                file_path = os.path.join(chapter_dir, f"{verse}.json")
                with open(file_path, 'w') as file:
                    json.dump({'translation' : verse_text}, file)
            else:
                print(f"  Error fetching verse {verse} of chapter {chapter}")
        print()

# Fetching data and saving to files
fetch_gita_data()
