# coding=utf-8

from flask import Flask, request
import requests
import json
import urllib.request
import urllib.parse
import urllib3
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from apscheduler.schedulers.background import BackgroundScheduler  
import time


app = Flask(__name__)
app.app_context().push()

http = urllib3.PoolManager()
requests.packages.urllib3.disable_warnings()

cred = credentials.Certificate('gita-daily-ee5f6-25032c526a9d.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


#Adds whatsapp format of italics to shlok
def italify(result):
    slok_r = result.split('\n')
    slok=''
    for s in slok_r:
        slok = slok + '_' + str(s) + '_\n'
    return slok

@app.route("/")
def hello():
    return "Hello, World!"

# data.json: key - Phone Number, value - [Name, Shlok, Subscribed]

@app.route("/startserver", methods=['POST'])
def runserver():
    res_data = request.json['data']
    # try:
            

    msg_lst = res_data['messages']
    msg = msg_lst[0]
    name = msg['pushName']
    try:
        msg_text = msg['message']['conversation']
    except:
        msg_text = msg['message']['extendedTextMessage']['text']
    phone_no = msg['key']['remoteJid'][:12]

    data = {}
    with open('data.json') as json_file:
        data = json.load(json_file)
    # print(phone_no)

    #New user not in data.json => add user
    if msg_text.lower().strip() == 'buyrbyur76457ur74y7':
        print('sending shlok')
        send_shlok()

    if phone_no not in data.keys() and ( 'hare krishna' in msg_text.lower().strip() or 'hare krsna' in msg_text.lower().strip() or 'hare krisna' in msg_text.lower().strip() or 'harekrishna' in msg_text.lower().strip()):
        data[phone_no] = [name, 1, True]
        encoded_msg = urllib.parse.quote('*🦚Hare​ Krishna {}!🦚* \n\nYou are now subscribed to receive daily *Bhagvad Gita* shlokas ✅ \n\nYou will receive a message every day at *5:00 AM* ⏰ \n\nYou can unsubscribe anytime by sending "unsubscribe" to this number. \n\nYour journey of self realisation starts now 🙏\n\nhttps://www.gitadaily.ml'.format(name))
        return_webhook_url = 'https://apibuddy.in/api/send.php?number={}&type=text&message={}&instance_id=633334FC32C17&access_token=6a9bf714c31f21ef0c5522bd6465e759'.format(phone_no, encoded_msg)
        requests.get(return_webhook_url, verify=False)
        # r=http.request('GET', return_webhook_url)
        # print(r.data)
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

                
    #User in data.json => resubscribe
    elif phone_no in data.keys() and ('harekrishna' in msg_text.lower().strip() or 'hare krishna' in msg_text.lower().strip() or 'hare krsna' in msg_text.lower().strip() or 'hare krisna' in msg_text.lower().strip()) and data[phone_no][2] == False:
        data[phone_no] = [name, data[phone_no][1], True]
        encoded_msg = urllib.parse.quote('*🦚Hare​ Krishna {}!🦚* \n\nYou are now subscribed to receive daily *Bhagvad Gita* shlokas ✅ \n\nYou will receive a message every day at *5:00 AM* ⏰ \n\nYou can unsubscribe anytime by sending "unsubscribe" to this number. \n\nYour journey of self realisation starts now 🙏\n\nhttps://www.gitadaily.ml'.format(name))
        return_webhook_url = 'https://apibuddy.in/api/send.php?number={}&type=text&message={}&instance_id=633334FC32C17&access_token=6a9bf714c31f21ef0c5522bd6465e759'.format(phone_no, encoded_msg)
        requests.get(return_webhook_url, verify=False)
        # print(r.data)
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

    #unsubscribe user
    elif phone_no in data.keys() and msg_text.lower().strip() == 'unsubscribe':
        data[phone_no][2] = False
        encoded_msg = urllib.parse.quote('You have been unsubscribed from Bhagavad Gita notifications.\n\nYou can resubscribe anytime by sending "hare​ krishna" to this number.\n\nWe thank you for taking the time in starting your journey of self realisation and we hope you will come back soon 🙏 \n\nPlease help us by sharing your feedback here 👇\nhttps://forms.gle/pLm2fczXNfKXk8dn7')
        return_webhook_url = 'https://apibuddy.in/api/send.php?number={}&type=text&message={}&instance_id=633334FC32C17&access_token=6a9bf714c31f21ef0c5522bd6465e759'.format(phone_no, encoded_msg)
        requests.get(return_webhook_url, verify=False)
        # print(r.data)
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
                     
    # except Exception as e:
    #     print(e)
    #     return "Error"
        



    return ""

#Number of Shlokas in each chapter
chapter_shlokas = [47, 72, 43, 42, 29, 47, 30, 28, 34, 42, 55, 20, 34, 27, 20, 24, 28, 78]

#Returns ch and shloka in the chapter from overall shlok number
def getChSh(n):
    ch = 1
    for n_schlokas in chapter_shlokas:
        if(n-n_schlokas > 0):
            n = n - n_schlokas
            ch = ch + 1
        else:
            break
    
    return (ch, n); 


# @app.route("/sendshlok", methods=['GET'])
def send_shlok():
    data = {}
    with open('data.json') as json_file:
        data = json.load(json_file) 
    # print(data)
    #iterate through all users and send them shlokas   
    for phone_no in data.keys():
        user_data = data[phone_no];
        print(user_data)
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
            return_webhook_url = 'https://apibuddy.in/api/send.php?number={}&type=text&message={}&instance_id=633334FC32C17&access_token=6a9bf714c31f21ef0c5522bd6465e759'.format(phone_no, encoded_msg)

            # print(return_webhook_url)
            requests.get(return_webhook_url, verify=False)
            # print(r.data)

            #Append user shlok number by 1
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
     
    return ""

def bringOnline():
    return_webhook_url = 'https://apibuddy.in/api/reconnect.php?instance_id=633334FC32C17&access_token=6a9bf714c31f21ef0c5522bd6465e759'
    requests.get(return_webhook_url, verify=False)
    # print(r.data)


if __name__ == "__main__":
   # time.sleep((16 * 60 * 60) + (11 * 60))
    sched = BackgroundScheduler()
    sched.start()
    sched.add_job(bringOnline, 'interval', seconds=120)
    app.run(host='0.0.0.0', port=5000)

# https://apibuddy.in/api/setwebhook.php?webhook_url=http://3.109.31.196:5000/startserver&enable=true&instance_id=633334FC32C17&access_token=6a9bf714c31f21ef0c5522bd6465e759
