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

async function sendMediaMessage(uniqueID, file) {
    try {
      const msg = await client.sendMessage(
        uniqueID,
        MessageMedia.fromFilePath(file)
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

client.on("ready", async () => {
  console.log("Client is ready!");
  await sendMediaMessage("6588646820@c.us", '/home/ubuntu/Gita-Daily-Images/1/1.png')
});

