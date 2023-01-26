const { Client } = require('whatsapp-web.js');
const puppeteer = require('puppeteer-core');

const client = new Client({
    puppeteer: {
      args: ['--no-sandbox']
    },
  });client.initialize();
const fs = require('fs');

client.on('qr', (qr) => {
    console.log('QR RECEIVED', qr);
});

client.on('ready', () => {
    console.log('Client is ready!');
});

async function sendMessage(uniqueID, message) {
    try {
        const msg = await client.sendMessage(uniqueID, message);
    } catch (e) {
        console.error(e);
    }
}

function checkPhoneNoExists(phoneNo, data) {
    const keys = Object.keys(data);
    return keys.includes(phoneNo);
}

function addUserToData(data, userID, name, number, booleanValue) {
    if(!data) {
        data = {};
    }
    data[userID] = [name, number, booleanValue];
    fs.writeFile('data.json', JSON.stringify(data), (err) => {
      if (err) throw err;
      console.log('Data written to file');
    });
    return "User added successfully!"
}

const chapter_shlokas = [47, 72, 43, 42, 29, 47, 30, 28, 34, 42, 55, 20, 34, 27, 20, 24, 28, 78];

function getChSh(n) {
    let ch = 1;
    for(let n_schlokas of chapter_shlokas) {
        if(n-n_schlokas > 0) {
            n = n - n_schlokas;
            ch = ch + 1;
        } else {
            break;
        }
    }
    return [ch, n];
}

function sendShlok() {
    try {
        let data = JSON.parse(fs.readFileSync('data.json', 'utf8'));
        let keys = Object.keys(data);
        for (let uniqueID of keys) {
            let user_data = data[uniqueID]
            if(user_data[2]){
                let [ch, sh] = getChSh(user_data[1]);
                let jsonData = JSON.parse(fs.readFileSync(`${ch}/${sh}.json`, 'utf8'));
                let message_text = '';
                let shlok_data_audio = jsonData['audio'];
                shlok_data_audio = 'https://www.gitadaily.ml/' + shlok_data_audio.slice(shlok_data_audio.indexOf('audio'));
                if(jsonData['commentary'] === 'NONE') {
                    message_text = jsonData['verse'].slice(0,-1) + '\n\n*Listen to this shlok here:*\n' + shlok_data_audio + '\n\n*Transliteration*\n' + jsonData['transliteration'] + '\n\n*Translation*' + jsonData['translation'] 
                } else {
                    message_text = jsonData['verse'].slice(0,-1) + '\n\n*Listen to this shlok here:*\n' + shlok_data_audio + '\n\n*Transliteration*\n' + jsonData['transliteration'] + '\n\n*Translation*' + jsonData['translation'] + '\n\n*Commentary*' + jsonData['commentary'] 
                }
                message_text += '\n\n\nThank you for reading today\'s shlok🙏\nYou can encourage your friends and family to also start reading the Gita by sharing this message:\n🦚🦚 To receive daily Bhagavad Gita shlokas, click this link: https://api.whatsapp.com/send/?phone=917348895108&text=Hare%20Krishna or WhatsApp "Haree Krsna" to +917348895108 ��🦚\n\nhttps://www.gitadaily.ml';
                sendMessage(uniqueID, message_text)
                data[uniqueID][1] = data[uniqueID][1] + jsonData['next shlok'] - sh;
            }
        }
        fs.writeFileSync('data.json', JSON.stringify(data, null, 2), 'utf8');            
        setTimeout(sendShlok, 24 * 60 * 60 * 1000);
    } catch (e) {
        console.error(e);
    }
}

function sendGeneralMessage() {
    try{
        let data = JSON.parse(fs.readFileSync('data.json', 'utf8'));
        let keys = Object.keys(data);
        for (let uniqueID of keys) {
            message_text = 'Dear Gita Daily community,\n\nWe apologize for the radio silence, but as the Bhagavad Gita says "Just as a snake sheds its skin, the soul sheds its body." And just like that, we have shed our old servers for newer, better ones.\n\nWe are thrilled to announce that starting today, we will be sending you daily messages of wisdom and inspiration at 5am sharp, continuing from the last shlok you received. But, if you prefer to start fresh, just drop us a message saying "shlok 1" and we\'ll make sure your profile is updated accordingly.\n\nThank you for being on this journey with us, and for your unwavering support. We hope these messages will bring positivity and guidance to your lives.\n\nWarm regards,\nGita Daily Team\n\nP.S. We would be thrilled if you could reply to this message with "hare krishna" to confirm receipt and show your excitement for our restarted service.'
            sendMessage(uniqueID, message_text)
        }
    } catch (e) {
        console.error(e);
    }
}


let date = new Date();
date.setUTCHours(5+5.5,0,0,0);
let timeUntil5am = date.getTime() - Date.now();
setTimeout(sendShlok, timeUntil5am);
setTimeout(sendGeneralMessage, 240000);


client.on('message', message => {
    var data = JSON.parse(fs.readFileSync('data.json', 'utf8'));
    const userID = message.from;
    const messageBody = message.body;
    const name = message._data.notifyName;

    const spellings = ["hare krishna", "hare krsna", "hare krishn", "hare krisna", "harekrishna"];
    if (spellings.some(spelling => messageBody.toLowerCase().includes(spelling))) {
        if(!checkPhoneNoExists(userID, data)) {
            addUserToData(data, userID, name, 1, true);
        } else {
            addUserToData(data, userID, name, data[userID][1], true);
        }
        client.sendMessage(message.from, '*🦚Hare Krishna ' + name + '!🦚* \n\nYou are now subscribed to receive daily *Bhagvad Gita* shlokas ✅ \n\nYou will receive a message every day at *5:00 AM* ⏰ \n\nYou can unsubscribe anytime by sending \"unsubscribe\" to this number. \n\nYour journey of self realisation starts now 🙏\n\nhttps://www.gitadaily.ml');
    } else if(messageBody.toLowerCase().includes("unsubscribe")) {
        addUserToData(data, userID, name, data[userID][1], false);
        client.sendMessage(message.from, "You have been unsubscribed from Bhagavad Gita notifications.\n\nYou can resubscribe anytime by sending \"hare krishna\" to this number.\n\nWe thank you for taking the time in starting your journey of self realisation and we hope you will come back soon 🙏 \n\nPlease help us by sharing your feedback here 👇\nhttps://forms.gle/pLm2fczXNfKXk8dn7");
    } else if(messageBody.toLowerCase().includes("shlok 1")) {
        addUserToData(data, userID, name, 1, true);
        message_text = 'Great choice! You have decided to start fresh from the beginning of the Bhagavad Gita. Your profile has been updated and you will now receive daily messages starting from Shlok 1. We hope that this journey through the Bhagavad Gita will bring you wisdom, inspiration, and guidance in your life. If you have any questions or concerns, please do not hesitate to reach out to us at manasbam.com or samarth.ml . Thank you for choosing to embark on this journey with us. Hare Krishna!'
        client.sendMessage(message.from, message_text);
    }
});