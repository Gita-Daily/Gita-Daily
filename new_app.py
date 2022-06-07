import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import requests
import json

http = httplib2.Http()
# status, response = http.request('https://www.holy-bhagavad-gita.org/chapter/1')

# for link in BeautifulSoup(response, parse_only=SoupStrainer('a')):
#     if link.has_attr('href'):
#         print(link['href'])

chapter = '18'

f = open(chapter + '.txt', 'r')
sub_links = f.read().split('\n')

curr_shlok = 1

for sub_link in sub_links:
    url = 'https://www.holy-bhagavad-gita.org' + str(sub_link)
    response = requests.get(url)

    soup = BeautifulSoup(response.content)
    verses = soup.find('div', attrs={'id' : 'originalVerse'}).findAll('p')
    result = ''
    for verse in verses:
        for line in str(verse)[3:-4].split('<br/>'):
            result += line + '\n'
    verse = result
    print(verse)
    transliteration = soup.find('div', attrs={'id' : 'transliteration'}).find('p').text
    audio = 'https://www.holy-bhagavad-gita.org' + str(soup.find('div', attrs={'id' : 'verseAudio'}).find('audio').get_attribute_list('src')[0])
    word_meanings = soup.find('div', attrs={'id' : 'wordMeanings'}).text
    translation = soup.find('div', attrs={'id' : 'translation'}).text
    try:
        commentary = soup.find('div', attrs={'id' : 'commentary'}).text
    except:
        print('No commentary for ' + str(curr_shlok))
        commentary = 'NONE'
    next_shlok = int(sub_link[len(sub_link)-1]) + 1
    if((sub_link[len(sub_link)-2]).isnumeric()):
        next_shlok = int(sub_link[len(sub_link)-2:]) + 1

    data = {'verse' : verse, 'transliteration' : transliteration, 'audio' : audio, 'word meanings' : word_meanings, 'translation' : translation, 'commentary' : commentary, 'next shlok' : next_shlok}
    with open(chapter + "/" + str(curr_shlok) + '.json', "w") as outfile:
        json.dump(data, outfile)
    print(curr_shlok)
    curr_shlok = next_shlok
    


    