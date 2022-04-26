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
    return 'Hello, World!'

chapter_shlokas = [47, 72, 43, 42, 29, 47, 30, 28, 34, 42, 55, 20, 34, 27, 20, 24, 28, 78]

def send_message():
    for phone_no in users.keys():
        user_data = users[phone_no];
        if(user_data[1]):
            ch, sh = getChSh(user_data[0]);
            URL = 'https://bhagavadgitaapi.in/slok/{}/{}'.format(ch, sh)
            page = requests.get(URL)

            result = json.loads(page.text)

            message_text = result['slok'] + '\n\n' + result['transliteration'] + '\n\nCommentary by ' + result['sankar']['author'] + '\n\n' + result['sankar']['et'] + '\n\n' + result['sankar']['ht']

            return_webhook_url = 'https://betablaster.in/api/send.php?number=919606807941&type=text&message={}&instance_id=62680FA67B740&access_token=f308a4f4a94bfd9ba008a559c5019d41'.format(message_text)
            urllib.request.urlopen(return_webhook_url)



def getChSh(n):
    ch = 1
    for n_schlokas in chapter_shlokas:
        if(n-n_schlokas > 0):
            n = n - n_schlokas
            ch = ch + 1
    
    return (ch, n);


        




scheduler = BackgroundScheduler()
scheduler.add_job(func='send_message', trigger="interval", seconds=25)

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

if __name__ == "__main__":
    app.run(debug=True)

scheduler.start()
