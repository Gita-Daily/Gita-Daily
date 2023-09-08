from flask import Flask, request, jsonify
import requests
import json
from datetime import datetime


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
        send_audio(waId, ch, sh)

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
        send_main_shloka(waId, ch, sh, message_text)
    
def send_commentary(waId, commentary_message):
    url = f"https://live-server-114563.wati.io/api/v1/sendSessionMessage/{waId}?messageText={commentary_message}"
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI0ZTk0YjdmYy01MDVlLTRkZjItYjMwYy0xOTlmNWE1NDhjODIiLCJ1bmlxdWVfbmFtZSI6ImthcnRoaWtAZG8ueW9nYSIsIm5hbWVpZCI6ImthcnRoaWtAZG8ueW9nYSIsImVtYWlsIjoia2FydGhpa0Bkby55b2dhIiwiYXV0aF90aW1lIjoiMDkvMDIvMjAyMyAwNTowNDo0NyIsImRiX25hbWUiOiIxMTQ1NjMiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJBRE1JTklTVFJBVE9SIiwiZXhwIjoyNTM0MDIzMDA4MDAsImlzcyI6IkNsYXJlX0FJIiwiYXVkIjoiQ2xhcmVfQUkifQ.29IGlp4J9UKJ1G6vFxmbi2A12TRiFRCQB-lL-ew6vxQ"}
    response = requests.post(url, headers=headers)  

    if response.status_code != 200:
        print("Error sending commentary. Sending again.")
        send_commentary(waId, commentary_message)  

def send_shloka(waId):
    try:
        with open('wati-data.json', 'r') as file:
            main_data = json.load(file)

            user_data = main_data[waId]
            if user_data[2]:
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

@app.route('/webhook', methods=['POST'])
def respond():
    name = request.json['senderName']
    msg = request.json['text']
    waId = request.json['waId']

    if user_exists(waId):
        send_shloka(waId)   

        return jsonify(status="received"), 200
    
    else:
        data = [name, 1, True, "english", str(datetime.now())]
        save_number(waId, data)

        url = f"{api_endpoint}/api/v1/sendSessionMessage/{waId}"
        reply = "Hare Krishna " + name + "! Welcome to Gita Daily. You are now subscribed to receive daily Bhagavad Gita shlokas."
        response = requests.post(url, headers={'Authorization' : access_token}, data={'messageText': reply})
        print(response.json())
    return jsonify(status="received"), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)