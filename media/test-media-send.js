const { Client, LocalAuth, MessageMedia } = require("whatsapp-web.js");
const puppeteer = require("puppeteer-core");
const fs2 = require('fs-extra');

const client = new Client({
  puppeteer: {
    headless: true,
    args: [
      "--no-sandbox",
      "--disable-gpu",
      "--disable-dev-shm-usage",
      "--disable-software-rasterizer",
      "--disable-extensions",
      "--single-process",
    ],
  },
  authStrategy: new LocalAuth(),
});

async function sendAudioMessage(uniqueID, filePath) {
    try {
      const msg = await client.sendMessage(
        uniqueID,
        MessageMedia.fromFilePath(filePath)
      );
      
    } catch (e) {
      console.error(e);
    }
  }



client.initialize();
const fs = require("fs");

client.on("qr", (qr) => {
  console.log("QR RECEIVED", qr);
});

client.on("ready", () => {
  console.log("Client is ready!");
  sendAudioMessage('919108006252@c.us','/Users/blackhole/Desktop/VS_Code.nosync/Python/Gita-Daily/media/000003.jpg');
});


client.on("message", (message) => {
        console.log(message.body);
        console.log(message.from);
          client.sendMessage(
            message.from,
            'sup'
          );            
    }
);