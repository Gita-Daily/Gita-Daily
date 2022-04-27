import imp
from flask import Flask, request
import datetime
import time
import pause
from apscheduler.schedulers.background import BackgroundScheduler  
import atexit
import requests
import json
import urllib.request

app = Flask(__name__)
app.app_context().push()

users = dict()
    
@app.route("/")
def hello():
    return "Hello, World!"

users = dict()

# dict_keys(['instance_id', 'event', 'data'])

@app.route("/test", methods=['POST'])
def runserver():
    # print(request.json['instance_id'])
    # print(request.json['event'])
    res_data = request.json['data']
    # print(type(res_data))

    if type(res_data) is dict:
        # print(res_data.keys())
        msg_lst = res_data['messages']
        msg = msg_lst[0]
        name = msg['pushName']
        msg_text = msg['message']['conversation']
        phone_no = msg['key']['remoteJid'][:12]

        if phone_no not in users.keys() and ( msg_text.lower().strip() == 'hare krishna' or msg_text.lower().strip() == 'hare krisna' or msg_text.lower().strip() == 'hare krsna'):
            users[phone_no] = [1, True, name]




    print(users)
    return "Hello, World!"

chapter_shlokas = [47, 72, 43, 42, 29, 47, 30, 28, 34, 42, 55, 20, 34, 27, 20, 24, 28, 78]

def getChSh(n):
    ch = 1
    for n_schlokas in chapter_shlokas:
        if(n-n_schlokas > 0):
            n = n - n_schlokas
            ch = ch + 1
    
    return (ch, n);


def print_date_time():
    for phone_no in users.keys():
        user_data = users[phone_no];
        if(user_data[1]):
            ch, sh = getChSh(user_data[0]);
            URL = 'https://bhagavadgitaapi.in/slok/{}/{}'.format(ch, sh)
            print(URL)
            page = requests.get(URL)

            result = json.loads(page.text)

            # message_text = result['slok'] + '\n\n' + result['transliteration'] + '\n\nCommentary by ' + result['sankar']['author'] + '\n\n' + result['sankar']['et'] + '\n\n' + result['sankar']['ht']
            message_text = 'hi I am samartg'
            return_webhook_url = 'https://betablaster.in/api/send.php?number={}&type=text&message={}&instance_id=62680FA67B740&access_token=f308a4f4a94bfd9ba008a559c5019d41'.format(phone_no, message_text)
            # request.post(return_webhook_url)
            ulr = urllib.quote(return_webhook_url)
            print(ulr)
            # urllib3.request.urlopen(return_webhook_url)
            # sendurl(return_webhook_url)
            # print(return_webhook_url)
            users[phone_no][0] = users[phone_no][0] + 1


def sendurl(url):
    request.post(url)

if __name__ == "__main__":
    sched = BackgroundScheduler()
    sched.start()
    sched.add_job(print_date_time, 'interval', seconds=10)
    app.run(debug=True)
    

