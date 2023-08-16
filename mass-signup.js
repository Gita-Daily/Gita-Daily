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

async function sendMessageForSignup(uniqueID, message) {
    try {
      const msg = await client.sendMessage(uniqueID, message);
      console.log(`Message sent to: ${uniqueID}`);  // Logs the successful number
    } catch (e) {
      console.error(uniqueID);
    }
}

fs.readFile('do-yoga-data.csv', 'utf8', async function(err, data) {
    if (err) {
        console.error("Error reading the file:", err);
        return;
    }

    const parsedData = Papa.parse(data, {
        header: true,
        dynamicTyping: true,
        skipEmptyLines: true
    });

    let dataframe = parsedData.data;

    // Filter out valid mobile numbers, ensure uniqueness, and append "@c.us"
    const unique = new Set();
    const validMobileNumbers = dataframe.reduce((acc, row) => {
        const value = row.Mobile;
        if (String(value).length === 12 && !isNaN(value) && !unique.has(value)) {
            unique.add(value);
            acc.push(value + "@c.us");
        }
        return acc;
    }, []);

    console.log(validMobileNumbers);
    console.log(`Count of Valid Mobile Numbers: ${validMobileNumbers.length}`);
    const testMobileNumbers = ['919108006252@c.us', 'd2387838942', '917337610771@c.us', '6588646820@c.us'];
    console.log(testMobileNumbers);
    client.initialize();

    client.on("qr", (qr) => {
      console.log("QR RECEIVED", qr);
    });
    
    client.on("ready", async () => {
      console.log("Client is ready!");
      const msg = '🌟 *Introducing Gita Daily* 🌟\n\nEmbark on a profound journey of wisdom and self-discovery every day. At Do Yoga, we\'re thrilled to present the Gita Daily service for you.\n\n🔹 *What is it?*\nEvery morning, journey through the Bhagavad Gita, one shloka at a time, unfolding its wisdom seamlessly into your day.\n\n🔹 *Why join?*\nBeyond just the shloka, get a deep dive with an articulate translation, insightful commentary, and an audio rendition - all aimed to elevate your mornings. In addition to English, the content is available in Hindi, with plans underway to introduce more languages soon.\n\n🔹 *How to Join?*\nSimply reply with *\'Hare Krishna\'* to this message to opt-in.\n\nIn the bustling pace of life, let\'s reconnect with profound wisdom, every single day. Your spiritual enrichment, now just one message away. 🌅\n\nFor more details, visit our website www.gitadaily.in'
        for (let uniqueID of testMobileNumbers) {
            await sendMessageForSignup(uniqueID, msg);
        }
    });
});