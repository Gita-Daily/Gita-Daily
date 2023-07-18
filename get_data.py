import requests
from bs4 import BeautifulSoup
import time
import json
import os

def save_specific_content(url, chapter, shloka):
    try:
        response = requests.get(url.format(chapter, shloka))
        soup = BeautifulSoup(response.text, 'html.parser')

        divs_body = soup.find_all('div', {'class': 'views-field views-field-body'})
        divs_etsiva = soup.find_all('div', {'class': 'views-field views-field-field-etsiva'})

        shloka_text = []
        for div in divs_body:
            p_tags = div.find_all('p')
            for p in p_tags:
                text = p.text.strip()
                text = text.replace("\n\n", "\n")
                shloka_text.append(text)

        translation_text = []
        for div in divs_etsiva:
            p_tags = div.find_all('p')
            for p in p_tags:
                text = p.text.strip()
                text = text.replace("\n", " ")
                translation_text.append(text)

        # Create a dictionary for JSON serialization
        data = {
            "shloka": shloka_text,
            "translation": translation_text
        }

        # Create directory if it does not exist
        os.makedirs(f'english_{chapter}', exist_ok=True)
        
        # Serialize data to JSON and save it
        with open(f'english_{chapter}/{shloka}.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# The URL has placeholders for the chapter and shloka numbers
url = "https://www.gitasupersite.iitk.ac.in/srimad?language=dv&field_chapter_value={}&field_nsutra_value={}&etsiva=1&choose=1"

# List of number of shlokas in each chapter
shlokas_in_chapter = [47, 72, 43, 42, 29, 47, 30, 28, 34, 42, 55, 20, 34, 27, 20, 24, 28, 78]

for chapter, num_shlokas in enumerate(shlokas_in_chapter, start=1):
    for shloka in range(1, num_shlokas + 1):
        save_specific_content(url, chapter, shloka)
