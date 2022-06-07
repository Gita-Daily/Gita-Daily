import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import requests
import json

http = httplib2.Http()
    
url = 'https://www.holy-bhagavad-gita.org' + str('/chapter/1/verse/4')
response = requests.get(url)

soup = BeautifulSoup(response.content)
verses = soup.find('div', attrs={'id' : 'originalVerse'}).findAll('p')
result = ''
for verse in verses:
    for line in str(verse)[3:-4].split('<br/>'):
        result += line + '\n'

print(result)