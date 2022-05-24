# coding=utf-8

from flask import Flask, request
import requests
import json
import urllib.request
import urllib.parse
import urllib3

app = Flask(__name__)
app.app_context().push()

users = dict()

http = urllib3.PoolManager()
requests.packages.urllib3.disable_warnings()


def italify(result):
    slok_r = result['slok'].split('\n')
    slok=''
    for s in slok_r:
        slok = slok + '_' + str(s) + '_\n'
    return slok



@app.route("/")
def hello():
    return "Hello, World!"

# dict_keys(['instance_id', 'event', 'data'])

@app.route("/test", methods=['POST'])
def runserver():
    # print(request.json['instance_id'])
    # print(request.json['event'])
    res_data = request.json['data']
    # print(type(res_data))

    try:
        if type(res_data) is dict:
            # print(res_data.keys())
            msg_lst = res_data['messages']
            msg = msg_lst[0]
            name = msg['pushName']
            msg_text = msg['message']['conversation']
            phone_no = msg['key']['remoteJid'][:12]

            data = {}
            with open('data.json') as json_file:
                data = json.load(json_file)

            if phone_no not in data.keys() and ( msg_text.lower().strip() == 'hare krishna' or msg_text.lower().strip() == 'hare krisna' or msg_text.lower().strip() == 'hare krsna'):
                data[phone_no] = [name, 1, True]
                encoded_msg = urllib.parse.quote('🦚*Hare Krishna {}!*🦚 \n\nYou are now subscribed to receive daily *Bhagvad Gita* shlokas ✅ \n\nYou will receive a message every day at *5:00 AM* ⏰ \n\nYou can unsubscribe anytime by sending "unsubscribe" to this number. \n\nYour journey of self realisation starts now 🙏'.format(name))
                return_webhook_url = 'https://betablaster.in/api/send.php?number={}&type=text&message={}&instance_id=628BC501C0151&access_token=444a724cf48b16b83aff3d7fada6270a'.format(phone_no, encoded_msg)
                r=http.request('GET', return_webhook_url)
                print(r.data)
                with open("data.json", "w") as outfile:
                        json.dump(data, outfile)
                        
            elif phone_no in data.keys() and ( msg_text.lower().strip() == 'hare krishna' or msg_text.lower().strip() == 'hare krisna' or msg_text.lower().strip() == 'hare krsna'):
                data[phone_no] = [name, data[phone_no][1], True]
                encoded_msg = urllib.parse.quote('🦚*Hare Krishna {}!*🦚 \n\nYou are now subscribed to receive daily *Bhagvad Gita* shlokas ✅ \n\nYou will receive a message every day at *5:00 AM* ⏰ \n\nYou can unsubscribe anytime by sending "unsubscribe" to this number. \n\nYour journey of self realisation starts now 🙏'.format(name))
                return_webhook_url = 'https://betablaster.in/api/send.php?number={}&type=text&message={}&instance_id=628BC501C0151&access_token=444a724cf48b16b83aff3d7fada6270a'.format(phone_no, encoded_msg)
                r=http.request('GET', return_webhook_url)
                print(r.data)
                with open("data.json", "w") as outfile:
                        json.dump(data, outfile)

            elif phone_no in data.keys() and msg_text.lower().strip() == 'unsubscribe':
                data[phone_no][2] = False
                encoded_msg = urllib.parse.quote('You have been unsubscribed from Bhagavad Gita notifications. \n\nYou can resubscribe anytime by sending "hare krishna" to this number. \n\n We thank you for taking the time in starting your journey of self realisation and we hope you will come back soon 🙏 \n\n Please help us by sharing your feedback here 👉  https://forms.gle/pLm2fczXNfKXk8dn7')
                return_webhook_url = 'https://betablaster.in/api/send.php?number={}&type=text&message={}&instance_id=628BC501C0151&access_token=444a724cf48b16b83aff3d7fada6270a'.format(phone_no, encoded_msg)
                r=http.request('GET', return_webhook_url)
                print(r.data)
                with open("data.json", "w") as outfile:
                        json.dump(data, outfile)
    except:
        pass



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

@app.route("/init", methods=['GET'])
def print_date_time():
    data = {}
    with open('data.json') as json_file:
        data = json.load(json_file)    
    for phone_no in data.keys():
        user_data = data[phone_no];
        if(user_data[2]):
            ch, sh = getChSh(user_data[1]);
            URL = 'https://bhagavadgitaapi.in/slok/{}/{}'.format(ch, sh)
            print(URL)
            page = requests.get(URL)

            result = json.loads(page.text)

            wrd_by_wrd_translation = ''
            commentary = ''
            message_text = ''
            if('No Commentary' in result['siva']['ec']):
                wrd_by_wrd_translation = result['siva']['ec'][:(result['siva']['ec'].find('No Commentary'))].replace('?', '')   
                message_text = italify(result) + '\n\n*Transliteration:* ' + result['transliteration'] + '\n\nCommentary by ' + result['siva']['author'] + '\n\n*Translation:* ' + result['siva']['et'] + '\n\n*Word By Word Meaning:* ' + wrd_by_wrd_translation

                
            else:
                wrd_by_wrd_translation = result['siva']['ec'][:(result['siva']['ec'].find('Commentary'))].replace('?', '')                
                commentary =  result['siva']['ec'][(result['siva']['ec'].find('Commentary')) + (11) : ].replace('?', '')   
                message_text = italify(result) + '\n\n*Transliteration:* ' + result['transliteration'] + '\n\nCommentary by ' + result['siva']['author'] + '\n\n*Translation:* ' + result['siva']['et'] + '\n\n*Word By Word Meaning:* ' + wrd_by_wrd_translation + '\n\n*Commentary* : ' + commentary

            message_text += '\n\n\nThank you for reading today\'s shlok🙏\nYou can encourage your friends and family to also start reading the Gita by sharing this message:\n🦚🦚 To receive daily Bhagavad Gita shlokas, message "Hare Krsna" to +917348895108 🦚🦚'
            encoded_msg = urllib.parse.quote(message_text)
            return_webhook_url = 'https://betablaster.in/api/send.php?number={}&type=text&message={}&instance_id=628BC501C0151&access_token=444a724cf48b16b83aff3d7fada6270a'.format(phone_no, encoded_msg)
            print(return_webhook_url)
            r=http.request('GET', return_webhook_url)
            print(r.data)
            data[phone_no][1] = data[phone_no][1] + 1

    with open("data.json", "w") as outfile:
        json.dump(data, outfile)
    return ""


if __name__ == "__main__":
    # sched = BackgroundScheduler()
    # sched.start()
    # sched.add_job(print_date_time, 'interval', seconds=40)
    app.run(debug=True)