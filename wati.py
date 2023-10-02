from flask import Flask, request, jsonify
import requests
import json
from datetime import datetime, timedelta
import razorpay

client = razorpay.Client(auth=("rzp_live_QqzWC0j38jO618", "gkq6eyHCkT1pvlx2Ma9IMV2v"))


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
#        send_audio(waId, ch, sh)

def send_main_shloka(waId, ch, sh, message_text):
    api_url = f"https://live-server-114563.wati.io/api/v1/sendInteractiveButtonsMessage?whatsappNumber={waId}"
    payload = {
        "header": {
            "media": { "url": f"https://github.com/LOLIPOP-INTELLIGENCE/Gita-Daily-Images/blob/main/{ch}_new/{sh}.png?raw=true" },
            "type": "Image"
        },
        "buttons": [{ "text": "Next Shloka" }],
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
#        send_main_shloka(waId, ch, sh, message_text)

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
#        send_commentary(waId, commentary_message)  

def send_message(waId):
    print('sending message to ' + waId + '...')
    try:
        with open('wati-data.json', 'r') as file:
            main_data = json.load(file)

            user_data = main_data[waId]
            if datetime.strptime(user_data[5], '%Y-%m-%d %H:%M:%S.%f') < datetime.now():
                # Create payment link
                # Send payment link
                # Check if paid
                # If yes, set user_data[5] to datetime.now() + timedelta(days=31)
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
                    "reminder_enable": False,
                })  

                url = res['short_url']
                send_pmt_link(waId, url)

            else:
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

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    return "Hello World"

@app.route('/pay', methods=['POST'])
def respond():
    try:
        print('payment received')
        ph_no = request.json['']
        return jsonify(status="received"), 200
    except Exception as e:
        print('error: ' + str(e))

@app.route('/webhook', methods=['POST'])
def respond():
    name = request.json['senderName']
    msg = request.json['text']
    waId = request.json['waId']
    print(msg)

    if user_exists(waId):
        send_message(waId)
        print('message that was received was  ' + str(msg) + ' from ' + str(name) + '...')

        return jsonify(status="received"), 200
    
    else:
        data = [name, 1, True, "english", str(datetime.now()), str(datetime.now() + timedelta(days=7))]
        save_number(waId, data)

        url = f"{api_endpoint}/api/v1/sendSessionMessage/{waId}"
        reply = "Hare Krishna " + name + "! Welcome to Gita Daily. We are an organisation aimed at sharing the knowledge of the Bhagavad Gita through easy to digest WhatsApp messages. You can read the shlokas at your own pace by clicking the \"Next Shloka\" button in our messages. Your first shloka is on its way!"
        response = requests.post(url, headers={'Authorization' : access_token}, data={'messageText': reply})
        print(response.json())
        send_message(waId)
        return jsonify(status="received"), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)