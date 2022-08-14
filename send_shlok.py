# coding=utf-8

from datetime import datetime
import requests
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import urllib
from pytz import timezone 
import time

cred = credentials.Certificate('gita-daily-ee5f6-25032c526a9d.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

def italify(result):
    slok_r = result.split('\n')
    slok=''
    for s in slok_r:
        slok = slok + '_' + str(s) + '_\n'
    return slok

chapter_shlokas = [47, 72, 43, 42, 29, 47, 30, 28, 34, 42, 55, 20, 34, 27, 20, 24, 28, 78]

def getChSh(n):
    ch = 1
    for n_schlokas in chapter_shlokas:
        if(n-n_schlokas > 0):
            n = n - n_schlokas
            ch = ch + 1
        else:
            break
    
    return (ch, n); 

def send_shlok():
    data = {}
    with open('data.json') as json_file:
        data = json.load(json_file) 
    for phone_no in data.keys():
        user_data = data[phone_no];
        if(user_data[2]):
            ch, sh = getChSh(user_data[1]);
            with open(str(ch) + '/' + str(sh) + '.json') as json_file:
                shlok_data = json.load(json_file) 

            message_text = ''
            shlok_data_audio = shlok_data['audio']
            shlok_data_audio = 'https://www.gitadaily.ml/' + shlok_data_audio[shlok_data_audio.index('audio'):]
            if(shlok_data['commentary'] == 'NONE'):
                message_text = italify(shlok_data['verse'][:-1]) + '\n\n*Listen to this shlok here:*\n' + shlok_data_audio + '\n\n*Transliteration*\n' + shlok_data['transliteration'] + '\n\n*Word Meanings*' + shlok_data['word meanings'] + '\n\n*Translation*' + shlok_data['translation'] 
            else:
                message_text = italify(shlok_data['verse'][:-1]) + '\n\n*Listen to this shlok here:*\n' + shlok_data_audio + '\n\n*Transliteration*\n' + shlok_data['transliteration'] + '\n\n*Word Meanings*' + shlok_data['word meanings'] + '\n\n*Translation*' + shlok_data['translation'] + '\n\n*Commentary*' + shlok_data['commentary'] 
            

            message_text += '\n\n\nThank you for reading today\'s shlok🙏\nYou can encourage your friends and family to also start reading the Gita by sharing this message:\n🦚🦚 To receive daily Bhagavad Gita shlokas, click this link: https://api.whatsapp.com/send/?phone=917348895108&text=Hare%20Krishna or WhatsApp "Ha​re Krsna" to +917348895108 🦚🦚\n\nhttps://www.gitadaily.ml'
            print(message_text)
            encoded_msg = urllib.parse.quote(message_text)
            return_webhook_url = 'https://betablaster.in/api/send.php?number={}&type=text&message={}&instance_id=62F4BD3B3D6C9&access_token=c35e340ec7db479e682bf99e5b3d1463'.format(phone_no, encoded_msg)
            requests.get(return_webhook_url, verify=False)
            data[phone_no][1] = data[phone_no][1] + shlok_data['next shlok'] - sh

    with open("data.json", "w") as outfile:
        json.dump(data, outfile)
    doc_ref = db.collection(u'json').document('data.json')
    doc_ref.set({
        u'data' : data
    })
    with open("data_r.json", "w") as outfile:
        json.dump(data, outfile)
    doc_ref = db.collection(u'json').document('data_r.json')
    doc_ref.set({
        u'data' : data
    })        
    
while True:
    if(datetime.now(timezone("Asia/Kolkata")).hour == 5):
        send_shlok()
        time.sleep((24 * 60 * 60))
