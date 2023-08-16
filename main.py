from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import json

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

def send_shloka(from_number):
    filename = 'main-data.json'
    try:
        with open(filename, 'r') as file:
            main_data = json.load(file)
            
            user_data = main_data[from_number]
            print(user_data)
            if user_data[2]:
                if user_data[3] == "english":
                    ch, sh = getChSh(user_data[1])
                    file_shlok = str(ch) + '/' + str(sh) + '.json'
                    with open(file_shlok, 'r') as file:
                        shloka_data = json.load(file)
                        message_text = "*Chapter " + str(ch) + " Verse " + str(sh) + "*\n\n" + shloka_data["verse"][:-1] + "\n*Translation*\n" +remove_unnecessary_spaces(shloka_data["translation"]) + "\n*Commentary*" + shloka_data["commentary"];
                
                        return message_text
                elif user_data[3] == "hindi":
                    shloka = "Hindi Shloka"

    except FileNotFoundError:
        return False    

@app.route('/main', methods=['POST'])
def main():
    incoming_message = request.values.get('Body', '').lower()
    from_number = request.values.get('From', '')
    name = request.values.get('ProfileName')

    if user_exists(from_number):
        response = MessagingResponse()
        reply = response.message()

        msg_body = send_shloka(from_number)
        print(msg_body)
        reply.body(msg_body)
        print("sent")
        print(response)
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
