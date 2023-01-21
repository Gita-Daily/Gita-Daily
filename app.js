const qrcode = require('qrcode-terminal');

const { Client, LocalAuth } = require('whatsapp-web.js');

const client = new Client({
    authStrategy: new LocalAuth()
});


client.on('qr', qr => {
    qrcode.generate(qr, {small: true});
});

client.on('ready', () => {
    console.log('Client is ready!');
});


// ================================================================ //
const fs = require('fs');
var data = fs.readFileSync('data.json');
var myObject= JSON.parse(data);

client.on('message', message => {
	console.log(message);
    const user = message.notifyName;
    const userID = message.from
    const messageContent = message.body;

    if (!(userID in myObject) && (messageContent === "hare krishna")){
        console.log(myObject)
        myObject[userID] = user;
        fs.writeFileSync('data.json', JSON.stringify(myObject));
    }
});


client.initialize();
