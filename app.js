const qrcode = require('qrcode-terminal');
const { Client, LocalAuth } = require('whatsapp-web.js');
const client = new Client({ authStrategy: new LocalAuth() });
client.initialize();
const fs = require('fs');


client.on('qr', qr => {
    qrcode.generate(qr, {small: true});
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
                message_text = jsonData['verse'].slice(0,-1) + '\n\n*Listen to this shlok here:*\n' + shlok_data_audio + '\n\n*Transliteration*\n' + jsonData['transliteration'] + '\n\n*Word Meanings*' + jsonData['word meanings'] + '\n\n*Translation*' + jsonData['translation'] 
            } else {
                message_text = jsonData['verse'].slice(0,-1) + '\n\n*Listen to this shlok here:*\n' + shlok_data_audio + '\n\n*Transliteration*\n' + jsonData['transliteration'] + '\n\n*Word Meanings*' + jsonData['word meanings'] + '\n\n*Translation*' + jsonData['translation'] + '\n\n*Commentary*' + jsonData['commentary'] 
            }
            message_text += '\n\n\nThank you for reading today\'s shlok🙏\nYou can encourage your friends and family to also start reading the Gita by sharing this message:\n🦚🦚 To receive daily Bhagavad Gita shlokas, click this link: https://api.whatsapp.com/send/?phone=917348895108&text=Hare%20Krishna or WhatsApp "Haree Krsna" to +917348895108 🦚🦚\n\nhttps://www.gitadaily.ml';
            sendMessage(uniqueID, message_text)
            data[uniqueID][1] = data[uniqueID][1] + jsonData['next shlok'] - sh;
        }
    }
    fs.writeFileSync('data.json', JSON.stringify(data, null, 2), 'utf8');            
    setTimeout(sendShlok, 30000);
}


// let date = new Date();
// date.setUTCHours(5+5.5,0,0,0);
// let timeUntil5am = date.getTime() - Date.now();
// setTimeout(sendShlok, timeUntil5am);
sendShlok();



client.on('message', message => {
    var data = JSON.parse(fs.readFileSync('data.json', 'utf8'));
    console.log(message);
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
    }
});