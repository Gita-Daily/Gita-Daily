const { Client, LocalAuth, MessageMedia, Buttons, List } = require('whatsapp-web.js');
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

client.on('message', async msg => {
    // console.log('MESSAGE RECEIVED', msg);
    if (msg.body === '!buttons') {
        console.log('BUTTONS');
        let button = new Buttons('Button body', [{ body: 'bt1' }, { body: 'bt2' }, { body: 'bt3' }], 'title', 'footer');
        client.sendMessage(msg.from, button);
        let sections = [{ title: 'sectionTitle', rows: [{ title: 'ListItem1', description: 'desc' }, { title: 'ListItem2' }] }];
        let list = new List('List body', 'btnText', sections, 'Title', 'footer');
        client.sendMessage(msg.from, list);
    }
});