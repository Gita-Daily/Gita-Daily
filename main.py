from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import json
from twilio.rest import Client

app = Flask(__name__)

def save_number(number, data):
    filename = 'main-data.json'
    try:
        with open(filename, 'r') as file:
            main_data = json.load(file)
    except FileNotFoundError:
        main_data = {}

    main_data[number] = data

    with open(filename, 'w') as file:
        json.dump(main_data, file)

def user_exists(number):
    filename = 'main-data.json'
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

def send_shloka():
    account_sid = "AC4520b0754de8c21ed79789a37f9d49ec"
    auth_token  = "c1e6f856e2655cc2bbd9d0bbf9dd5254"

    client = Client(account_sid, auth_token)

    try:

        with open('main-data.json', 'r') as file:
            main_data = json.load(file)

        for number in main_data:
            user_data = main_data[number]
            if user_data[2]:
                ch, sh = getChSh(user_data[1])
                file_shlok = str(ch) + '/' + str(sh) + '.json'
                with open(file_shlok, 'r') as file:
                    shloka_data = json.load(file)
                    if shloka_data["new_commentary"] != "NONE":
                        message_text = "*Chapter " + str(ch) + " Verse " + str(sh) + "*\n\n" + shloka_data["verse"][:-1] + "\n\n*Translation*\n" +remove_unnecessary_spaces(shloka_data["translation"].strip('\n')) + "\n*Commentary*\n" + shloka_data["new_commentary"].strip('\n');
                    else:
                        message_text = "*Chapter " + str(ch) + " Verse " + str(sh) + "*\n\n" + shloka_data["verse"][:-1] + "\n\n*Translation*\n" +remove_unnecessary_spaces(shloka_data["translation"].strip('\n'));
                
                message_image = client.messages.create(
                    body=message_text,
                    media_url=f"https://raw.githubusercontent.com/LOLIPOP-INTELLIGENCE/Gita-Daily-Images/main/{ch}/{sh}.png",
                    from_="whatsapp:+14155238886",
                    to=number
                )

                user_data[1] = user_data[1] + shloka_data['next shlok'] - sh
                main_data[number] = user_data

        with open('main-data.json', 'w') as file:
            json.dump(main_data, file)
    
    except Exception as e:
        print(e)

@app.route('/main', methods=['POST'])
def main():
    incoming_message = request.values.get('Body', '').lower()
    from_number = request.values.get('From', '')
    name = request.values.get('ProfileName')

    if incoming_message == "send all":
        send_shloka()

        return "Done"
    else:
        if user_exists(from_number):
            response = MessagingResponse()
            
            reply_text = response.message()
            msg_body = "Thank you for contacting Gita Daily. You will receive a shloka everyday. If you want to reach out to us, message us on +91xxxxxxxxxx"
            reply_text.body(msg_body)

            return str(response)
        
        else:
            data = [name, 1, True, "english"]
            save_number(from_number, data)

            response = MessagingResponse()
            reply = response.message()

            reply.body("Thanks for contacting")
            return str(response)

if __name__ == '__main__':
    app.run(debug=True)