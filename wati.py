from flask import Flask, request, jsonify
import requests
import json
from datetime import datetime, timedelta
import razorpay
import queue
import threading
import time
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone



client = razorpay.Client(auth=("rzp_live_QqzWC0j38jO618", "gkq6eyHCkT1pvlx2Ma9IMV2v"))

message_queue = queue.Queue(maxsize=100)

access_token = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI0ZTk0YjdmYy01MDVlLTRkZjItYjMwYy0xOTlmNWE1NDhjODIiLCJ1bmlxdWVfbmFtZSI6ImthcnRoaWtAZG8ueW9nYSIsIm5hbWVpZCI6ImthcnRoaWtAZG8ueW9nYSIsImVtYWlsIjoia2FydGhpa0Bkby55b2dhIiwiYXV0aF90aW1lIjoiMDkvMDIvMjAyMyAwNTowNDo0NyIsImRiX25hbWUiOiIxMTQ1NjMiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJBRE1JTklTVFJBVE9SIiwiZXhwIjoyNTM0MDIzMDA4MDAsImlzcyI6IkNsYXJlX0FJIiwiYXVkIjoiQ2xhcmVfQUkifQ.29IGlp4J9UKJ1G6vFxmbi2A12TRiFRCQB-lL-ew6vxQ'
api_endpoint = "https://live-server-114563.wati.io"


def save_number(number, data):
    filename = 'wati-data.json'
    try:
        with open(filename, 'r') as file:
            main_data = json.load(file)
    except FileNotFoundError:
        main_data = {}

    main_data[number] = data

    with open(filename, 'w') as file:
        json.dump(main_data, file)

def save_pmt_data(data, file_name="pmt-data.json"):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)

def load_pmt_data(file_name="pmt-data.json"):
    try:
        with open(file_name, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"phone_numbers": {}, "pmt_id_lookup": {}}
    
def add_pmt_id(phone_number, pmt_id):
    data = load_pmt_data()
    phone_numbers = data.get("phone_numbers", {})
    pmt_id_lookup = data.get("pmt_id_lookup", {})    
    if phone_number in phone_numbers:
        phone_numbers[phone_number].append(pmt_id)
    else:
        phone_numbers[phone_number] = [pmt_id]

    pmt_id_lookup[pmt_id] = phone_number
    save_pmt_data({"phone_numbers": phone_numbers, "pmt_id_lookup": pmt_id_lookup})

def process_pmt(pmt_id):
    data = load_pmt_data()
    phone_numbers = data.get("phone_numbers", {})
    pmt_id_lookup = data.get("pmt_id_lookup", {})      
    phone_number = pmt_id_lookup.get(pmt_id)
    if phone_number:
        print(f"Phone Number: {phone_number}")

        phone_numbers[phone_number].remove(pmt_id)
        del pmt_id_lookup[pmt_id]
    else:
        print("PMT ID not found.")
    
    save_pmt_data({"phone_numbers": phone_numbers, "pmt_id_lookup": pmt_id_lookup})   
    return phone_number 


def user_exists(number):
    filename = 'wati-data.json'
    try:
        with open(filename, 'r') as file:
            main_data = json.load(file)
            return number in main_data
    except FileNotFoundError:
        return False
    
chapter_shlokas = [
    47, 72, 43, 42, 29, 47, 30, 28, 34, 42, 55, 20, 34, 27, 20, 24, 28, 78,
]

def getChSh(n):
    ch = 1
    for n_schlokas in chapter_shlokas:
        if n - n_schlokas > 0:
            n = n - n_schlokas
            ch = ch + 1
        else:
            break
    return ch, n

def remove_unnecessary_spaces(s):
    lines = s.split("\r\n")
    trimmed_lines = [line.strip() for line in lines]
    return "\r\n".join(trimmed_lines)

def send_audio(waId, ch, sh):
    url = f"https://live-server-114563.wati.io/api/v1/sendSessionFile/{waId}"
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI0ZTk0YjdmYy01MDVlLTRkZjItYjMwYy0xOTlmNWE1NDhjODIiLCJ1bmlxdWVfbmFtZSI6ImthcnRoaWtAZG8ueW9nYSIsIm5hbWVpZCI6ImthcnRoaWtAZG8ueW9nYSIsImVtYWlsIjoia2FydGhpa0Bkby55b2dhIiwiYXV0aF90aW1lIjoiMDkvMDIvMjAyMyAwNTowNDo0NyIsImRiX25hbWUiOiIxMTQ1NjMiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJBRE1JTklTVFJBVE9SIiwiZXhwIjoyNTM0MDIzMDA4MDAsImlzcyI6IkNsYXJlX0FJIiwiYXVkIjoiQ2xhcmVfQUkifQ.29IGlp4J9UKJ1G6vFxmbi2A12TRiFRCQB-lL-ew6vxQ"
    }
    audio_file_path = f"Audio/{ch}_{sh}.mp3"
    with open(audio_file_path, 'rb') as f:
        file_data = f.read()

    files = {'file': ('file.mp3', file_data, 'audio/mpeg')}

    response = requests.post(url, headers=headers, files=files)

    if response.status_code != 200:
        print("Error sending audio. Sending again.")        

def send_main_shloka(waId, ch, sh, message_text):
    api_url = f"https://live-server-114563.wati.io/api/v1/sendInteractiveButtonsMessage?whatsappNumber={waId}"
    # payload = {
    #     "header": {
    #         "media": { "url": f"https://github.com/LOLIPOP-INTELLIGENCE/Gita-Daily-Images-New/blob/main/{ch}/{sh}.jpg?raw=true" },
    #         "type": "Image"
    #     },
    #     "buttons": [{ "text": "I finished reading" }, { "text": "Next Shloka" }],
    #     "footer": "www.gitadaily.in",
    #     "body": message_text
    # }
    payload = {
        "header": {
            "media": { "url": f"https://github.com/LOLIPOP-INTELLIGENCE/Gita-Daily-Images-New/blob/main/{ch}/{sh}.jpg?raw=true" },
            "type": "Image"
        },
        "buttons": [{ "text": "I finished reading" }],
        "footer": "www.gitadaily.in",
        "body": message_text
    }    
    headers = {
        "content-type": "text/json",
        "Authorization": access_token
    }

    response = requests.post(api_url, json=payload, headers=headers)    

    if response.status_code != 200:
        print("Error sending main shloka. Sending again.")

def send_pmt_confirmed(waId):
    msg = "Payment confirmed. You will continue receiving Gita Daily messages for the next 30 days."
    url = f"https://live-server-114563.wati.io/api/v1/sendSessionMessage/{waId}?messageText={msg}"
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI0ZTk0YjdmYy01MDVlLTRkZjItYjMwYy0xOTlmNWE1NDhjODIiLCJ1bmlxdWVfbmFtZSI6ImthcnRoaWtAZG8ueW9nYSIsIm5hbWVpZCI6ImthcnRoaWtAZG8ueW9nYSIsImVtYWlsIjoia2FydGhpa0Bkby55b2dhIiwiYXV0aF90aW1lIjoiMDkvMDIvMjAyMyAwNTowNDo0NyIsImRiX25hbWUiOiIxMTQ1NjMiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJBRE1JTklTVFJBVE9SIiwiZXhwIjoyNTM0MDIzMDA4MDAsImlzcyI6IkNsYXJlX0FJIiwiYXVkIjoiQ2xhcmVfQUkifQ.29IGlp4J9UKJ1G6vFxmbi2A12TRiFRCQB-lL-ew6vxQ"}
    response = requests.post(url, headers=headers)  

    if response.status_code != 200:
        print("Error sending payment confirmation. Sending again.")

def send_pmt_link(waId, pmt_url):
    msg = "Please pay Rs. 108 to continue receiving Gita Daily messages. Click the link below to pay. \n\n" + pmt_url
    url = f"https://live-server-114563.wati.io/api/v1/sendSessionMessage/{waId}?messageText={msg}"
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI0ZTk0YjdmYy01MDVlLTRkZjItYjMwYy0xOTlmNWE1NDhjODIiLCJ1bmlxdWVfbmFtZSI6ImthcnRoaWtAZG8ueW9nYSIsIm5hbWVpZCI6ImthcnRoaWtAZG8ueW9nYSIsImVtYWlsIjoia2FydGhpa0Bkby55b2dhIiwiYXV0aF90aW1lIjoiMDkvMDIvMjAyMyAwNTowNDo0NyIsImRiX25hbWUiOiIxMTQ1NjMiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJBRE1JTklTVFJBVE9SIiwiZXhwIjoyNTM0MDIzMDA4MDAsImlzcyI6IkNsYXJlX0FJIiwiYXVkIjoiQ2xhcmVfQUkifQ.29IGlp4J9UKJ1G6vFxmbi2A12TRiFRCQB-lL-ew6vxQ"}
    response = requests.post(url, headers=headers)  

    if response.status_code != 200:
        print("Error sending payment link. Sending again.")
    
def send_commentary(waId, commentary_message):
    url = f"https://live-server-114563.wati.io/api/v1/sendSessionMessage/{waId}?messageText={commentary_message}"
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI0ZTk0YjdmYy01MDVlLTRkZjItYjMwYy0xOTlmNWE1NDhjODIiLCJ1bmlxdWVfbmFtZSI6ImthcnRoaWtAZG8ueW9nYSIsIm5hbWVpZCI6ImthcnRoaWtAZG8ueW9nYSIsImVtYWlsIjoia2FydGhpa0Bkby55b2dhIiwiYXV0aF90aW1lIjoiMDkvMDIvMjAyMyAwNTowNDo0NyIsImRiX25hbWUiOiIxMTQ1NjMiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJBRE1JTklTVFJBVE9SIiwiZXhwIjoyNTM0MDIzMDA4MDAsImlzcyI6IkNsYXJlX0FJIiwiYXVkIjoiQ2xhcmVfQUkifQ.29IGlp4J9UKJ1G6vFxmbi2A12TRiFRCQB-lL-ew6vxQ"}
    response = requests.post(url, headers=headers)  

    if response.status_code != 200:
        print("Error sending commentary. Sending again.")

def send_thank_you(waId, shloka_number):
    completed_percent = round((shloka_number / 700) * 100, 2)
    reply_text = f"That's great! You are now one step closer to self-realization. Thank you for reading Gita Daily. You have completed reading {completed_percent}% of the Bhagavad Gita. Keep going! You will receive your next shloka tomorrow at 7:00 AM."
    url = f"https://live-server-114563.wati.io/api/v1/sendSessionMessage/{waId}?messageText={reply_text}"
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI0ZTk0YjdmYy01MDVlLTRkZjItYjMwYy0xOTlmNWE1NDhjODIiLCJ1bmlxdWVfbmFtZSI6ImthcnRoaWtAZG8ueW9nYSIsIm5hbWVpZCI6ImthcnRoaWtAZG8ueW9nYSIsImVtYWlsIjoia2FydGhpa0Bkby55b2dhIiwiYXV0aF90aW1lIjoiMDkvMDIvMjAyMyAwNTowNDo0NyIsImRiX25hbWUiOiIxMTQ1NjMiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJBRE1JTklTVFJBVE9SIiwiZXhwIjoyNTM0MDIzMDA4MDAsImlzcyI6IkNsYXJlX0FJIiwiYXVkIjoiQ2xhcmVfQUkifQ.29IGlp4J9UKJ1G6vFxmbi2A12TRiFRCQB-lL-ew6vxQ"}
    response = requests.post(url, headers=headers)  

    if response.status_code != 200:
        print("Error sending thank you message. Sending again.")


def send_message(waId):
    print('sending message to ' + waId + '...')
    try:
        with open('wati-data.json', 'r') as file:
            main_data = json.load(file)

            user_data = main_data[waId]
            if datetime.strptime(user_data[5], '%Y-%m-%d %H:%M:%S.%f') < datetime.now():
                uid = str(time.time() * 1000)
                res = client.payment_link.create({
                    "upi_link": True,
                    "amount": 108,
                    "currency": "INR",
                    "accept_partial": False,
                    "description": "For Gita Daily 1 month subscription",
                    "customer": {
                        "name": user_data[0],
                        "contact": waId,
                    },
                    "notify": {
                        "sms": True,
                        "email": True
                    },
                    "notes": {
                        "uid": uid
                    },
                    "reminder_enable": False,
                })  

                print(res)
                add_pmt_id(waId, uid)

                url = res['short_url']
                send_pmt_link(waId, url)

            else:
                if datetime.strptime(user_data[4], '%Y-%m-%d %H:%M:%S.%f') + timedelta(days=1) > datetime.now():
                    ch, sh = getChSh(user_data[1])
                    file_shlok = str(ch) + '/' + str(sh) + '.json'
                    with open(file_shlok, 'r') as file:
                        shloka_data = json.load(file)
                        
                        verse = shloka_data["verse"][:-1]
                        translation = remove_unnecessary_spaces(shloka_data["translation"].strip('\n'))
                        newest_commentary = shloka_data.get("newest_commentary", "NONE").strip('\n')
                        
                        if len(verse) + len(translation) + len(newest_commentary) + len("*Chapter 12* Verse 12*\n\n\n\n*Translation*\n\n*Commentary*\n") > 1024:
                            commentary_message = "*Commentary*\n" + newest_commentary
                            newest_commentary = "NONE"
                        
                        if newest_commentary != "NONE":
                            message_text = f"*Chapter {ch} Verse {sh}*\n\n{verse}\n\n*Translation*\n{translation}\n*Commentary*\n{newest_commentary}"
                        else:
                            message_text = f"*Chapter {ch} Verse {sh}*\n\n{verse}\n\n*Translation*\n{translation}"

                    send_main_shloka(waId, ch, sh, message_text)
                    send_audio(waId, ch, sh)       

                    if 'commentary_message' in locals():
                        send_commentary(waId, commentary_message)

                    user_data[1] = user_data[1] + shloka_data['next shlok'] - sh
                    main_data[waId] = user_data
        with open('wati-data.json', 'w') as file:
            json.dump(main_data, file)
    
    except Exception as e:
        print('error: ' + str(e))

def sendMessageToAllUsers():
    try:
        with open('wati-data.json', 'r') as file:
            users_data = json.load(file)
            for waId in users_data.keys():
                message_queue.put(waId)
                print(f"Queued message for user: {waId}")
    except Exception as e:
        print(f"Error in sendMessageToAllUsers: {e}")

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    return "Hello World"

@app.route('/pay', methods=['POST'])
def payment_handle():
    try:
        print('payment received')
        res = (request.json)
        print(res)
        pmt_id = str(res['payload']['payment']['entity']['notes']['uid'])
        waId = process_pmt(pmt_id)

        if waId:
            with open('wati-data.json', 'r') as file:
                main_data = json.load(file)
                user_data = main_data[waId]
                user_data[5] = str(datetime.now() + timedelta(days=3))
                main_data[waId] = user_data
            with open('wati-data.json', 'w') as file:
                json.dump(main_data, file)
            send_pmt_confirmed(waId)
        return jsonify(status="received"), 200
    except Exception as e:
        print('error: ' + str(e))
        return jsonify(status="not handled", message=str(e)), 200

def process_queue():
    print("Queue processing thread started")
    while True:
        try:
            waId = message_queue.get(block=True)
            print(f"Processing message for waId: {waId}")
            send_message(waId)
            message_queue.task_done()
        except Exception as e:
            print(f"Error processing message: {e}")


@app.route('/webhook', methods=['POST'])
def respond():
    try:
        name = request.json['senderName']
        msg = request.json['text']
        waId = request.json['waId']
        print("the message is " + str(msg) + " from " + str(name) + "...")

        if user_exists(waId):
            print("user exists")
            if msg.lower().strip() == "i finished reading":
                print("user finished reading")
                with open('wati-data.json', 'r') as file:
                    main_data = json.load(file)
                    user_data = main_data[waId]
                    user_data[4] = str(datetime.now())
                    main_data[waId] = user_data
                with open('wati-data.json', 'w') as file:
                    json.dump(main_data, file)                                     
                send_thank_you(waId, user_data[1])
                
            # if msg.lower().strip() == "next shloka":
            #     print("user wants next shloka")
            #     send_message(waId)
        
        else:
            if msg.lower().strip() == "hare krishna":
                data = [name, 1, True, "english", str(datetime.now()), str(datetime.now() + timedelta(days=2))]
                save_number(waId, data)

                url = f"{api_endpoint}/api/v1/sendSessionMessage/{waId}"
                reply = "Hare Krishna " + name + """! Welcome to Gita Daily. We are delighted to offer you the enriching wisdom of the Bhagavad Gita through easy-to-digest WhatsApp messages. As part of our commitment to quality service, please note that this is a paid subscription, primarily due to the costs associated with using WhatsApp for daily message delivery. However, to get you started, you are on a complimentary 7-day trial.

                Here's how our service works:

                1. *Daily Shloka:* You'll receive a shloka every day.
                2. *Completion Confirmation:* After reading, click the 'I finished reading' button.
                3. *Reminder:* If a shloka is not read, you'll receive a reminder to ensure you don't miss out.                

                Your first shloka is already on its way! Embark on this spiritual journey at your own pace and immerse yourself in the timeless teachings of the Bhagavad Gita.
                """
                response = requests.post(url, headers={'Authorization' : access_token}, data={'messageText': reply})
                print(response.json())
                send_message(waId)
    
    except Exception as e:
        print('error: ' + str(e))

    return jsonify(status="received"), 200
        


if __name__ == '__main__':
    processing_thread = threading.Thread(target=process_queue, daemon=True)
    processing_thread.start()

    scheduler = BackgroundScheduler()
    scheduler.configure(timezone=timezone('Asia/Kolkata'))
    scheduler.add_job(sendMessageToAllUsers, 'cron', hour=7, minute=0)
    scheduler.start()

    app.run(host='0.0.0.0', port=5001, debug=False)    
