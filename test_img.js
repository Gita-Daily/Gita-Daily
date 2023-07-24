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
client.initialize();
const fs = require("fs");

client.on("qr", (qr) => {
  console.log("QR RECEIVED", qr);
});

client.on("ready", () => {
  console.log("Client is ready!");
  sendMediaMessage("6588646820@c.us", 'https://www.w3schools.com/w3css/img_lights.jpg')
});

async function sendMediaMessage(uniqueID, url) {
    try {
      const msg = await client.sendMessage(
        uniqueID,
        MessageMedia.fromUrl(url)
      );
    } catch (e) {
      console.error(e);
    }
  }

//sendMediaMessage("6588646820@c.us", 'https://www.w3schools.com/w3css/img_lights.jpg')
