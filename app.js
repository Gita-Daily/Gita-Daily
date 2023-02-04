const { Client, LocalAuth  } = require('whatsapp-web.js');
const puppeteer = require('puppeteer-core');

const client = new Client({
    puppeteer: {
      args: ['--no-sandbox']
    },
    authStrategy: new LocalAuth(),
  });
client.initialize();
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
                message_text += '\n\n\nThank you for reading today\'s shlok🙏\nYou can encourage your friends and family to also start reading the Gita by sharing this message:\n🦚🦚 To receive daily Bhagavad Gita shlokas, click this link: https://api.whatsapp.com/send/?phone=917348895108&text=Hare%20Krishna or WhatsApp "Hare Krishna" to +917348895108 🦚🦚🦚\n\nhttps://www.gitadaily.ml';
                sendMessage(uniqueID, message_text)
                data[uniqueID][1] = data[uniqueID][1] + jsonData['next shlok'] - sh;
            }
        }
        fs.writeFileSync('data.json', JSON.stringify(data, null, 2), 'utf8'); 
        let date = new Date();
        date.setUTCHours(0,0,0,0);
        let timeUntil5am = date.getTime() - Date.now();   
        console.log(timeUntil5am)                
        setTimeout(sendShlok, timeUntil5am);
    } catch (e) {
        console.error(e);
    }
}

function nextShlok(uniqueID) {
    let data = JSON.parse(fs.readFileSync('data.json', 'utf8'));
    let user_data = data[uniqueID]
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
    message_text += '\n\n\nThank you for reading the next shlok🙏\nYou can encourage your friends and family to also start reading the Gita by sharing this message:\n🦚🦚 To receive daily Bhagavad Gita shlokas, click this link: https://api.whatsapp.com/send/?phone=917348895108&text=Hare%20Krishna or WhatsApp "Hare Krishna" to +917348895108 🦚🦚🦚\n\nhttps://www.gitadaily.ml';
    sendMessage(uniqueID, message_text)
    data[uniqueID][1] = data[uniqueID][1] + jsonData['next shlok'] - sh;
    fs.writeFileSync('data.json', JSON.stringify(data, null, 2), 'utf8');            
}

function sendGeneralMessage(msg) {
    try{
        let data = JSON.parse(fs.readFileSync('data.json', 'utf8'));
        let keys = Object.keys(data);
        for (let uniqueID of keys) {
            sendMessage(uniqueID, msg)
        }
    } catch (e) {
        console.error(e);
    }
}

let secretString = "galactic-ai-wielders-of-the-force: ";
let feedbackStrings = ["feedback", "feedback:", "feedback: "];

// let date = new Date();
// date.setUTCHours(5-5.5,0,0,0);
// let timeUntil5am = date.getTime() - Date.now();
setTimeout(sendShlok, 4 * 60 * 1000);
// setTimeout(sendGeneralMessage, 240000);


client.on('message', message => {
    try{
        var data = JSON.parse(fs.readFileSync('data.json', 'utf8'));
        const userID = message.from;
        const messageBody = message.body;
        const name = message._data.notifyName;
        console.log(messageBody)
        const spellings = ["hare krishna", "hare krsna", "hare krishn", "hare krisna", "harekrishna"];
        const nxtShlok = ["next shlok", "next verse", "next slok"];


        if (messageBody.toLowerCase().startsWith(secretString)) {
            sendGeneralMessage(messageBody.replace(secretString, ""));
        } else if(feedbackStrings.some(spelling => messageBody.toLowerCase().includes(spelling))) {
            sendMessage("919108006252@c.us", messageBody + "\n\n" + name + " " + userID);
            sendMessage("917337610771@c.us", messageBody + "\n\n" + name + " " + userID);
            sendMessage(userID, "Thank you for your valuable feedback! Your thoughts and opinions help us improve and better serve our community. As the Bhagavad Gita states, \"Karmanye vadhikaraste ma phaleshu kadachana\" (2.47), which means \"In actions, do as you will, but do not be attached to their results.\" Your feedback is a reminder for us to stay humble and continue our journey towards growth and improvement. Thank you again!");
        } else if(nxtShlok.some(spelling => messageBody.toLowerCase().includes(spelling))) {
            nextShlok(userID);
        } else if (spellings.some(spelling => messageBody.toLowerCase().includes(spelling))) {
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
    } catch (e) {
        console.log(e)
    }
});