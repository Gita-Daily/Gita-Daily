const fs = require('fs');
const Papa = require('papaparse');

const { Client, LocalAuth, MessageMedia } = require("whatsapp-web.js");

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


client.on("qr", (qr) => {
    console.log("QR RECEIVED", qr);
  });
  
  client.on("ready", async () => {
    console.log("Client is ready!");
    // for (let uniqueID of testMobileNumbers) {
    //   await sendMessage(uniqueID, msg);
    // }      
  });    