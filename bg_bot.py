from flask import Flask, request
import datetime
import time
import pause
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

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
            users[phone_no] = [0, True, name]




    print(users)
    return "Hello, World!"

def send_message():
    print('test')



scheduler = BackgroundScheduler()
scheduler.add_job(func='send_message', trigger="interval", seconds=10)

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

if __name__ == "__main__":
    app.run(debug=True)

scheduler.start()
