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
});

async function sendMessage(uniqueID, message) {
  try {
    const msg = await client.sendMessage(uniqueID, message);
  } catch (e) {
    console.error(e);
  }
}

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

function removeUnnecessarySpaces(str) {
  // Split the string by '\r\n' to get an array of strings
  let arr = str.split("\r\n");

  // Iterate over the array and trim each string
  for (let i = 0; i < arr.length; i++) {
    arr[i] = arr[i].trim();
  }

  // Join the array back into a single string with '\r\n' as the separator
  return arr.join("\r\n");
}

function checkPhoneNoExists(phoneNo, data) {
  try {
    const keys = Object.keys(data);
    return keys.includes(phoneNo);
  } catch (e) {
    console.error(e);
  }
}

function addUserToData(data, userID, name, number, booleanValue, language) {
  try {
    if (!data) {
      data = {};
    }
    data[userID] = [name, number, booleanValue, language];
    fs.writeFile("data.json", JSON.stringify(data), (err) => {
      if (err) throw err;
    });
  } catch (e) {
    console.error(e);
  }
  return "User added successfully!";
}

const chapter_shlokas = [
  47, 72, 43, 42, 29, 47, 30, 28, 34, 42, 55, 20, 34, 27, 20, 24, 28, 78,
];

function getChSh(n) {
  let ch = 1;
  for (let n_schlokas of chapter_shlokas) {
    if (n - n_schlokas > 0) {
      n = n - n_schlokas;
      ch = ch + 1;
    } else {
      break;
    }
  }
  return [ch, n];
}

async function getValidShlokNumber(n) {
  let [ch, sh] = getChSh(n);
  const path = `${ch}/${sh}.json`;
  const exists = await fs2.pathExists(path);
  if (exists) {
    return n;
  } else {
    return await getValidShlokNumber(n - 1);
  }
}

function sendShlok() {
  try {
    let count = 0;
    fs.readFile("data.json", "utf8", async (err, content) => {
      if (err) throw err;
      let data = JSON.parse(content);
      let keys = Object.keys(data);
      for (let uniqueID of keys) {
        let user_data = data[uniqueID];
        if (user_data[2]) {
          if (user_data[3] == "english") {
            let [ch, sh] = getChSh(user_data[1]);
            let jsonData = JSON.parse(
              fs.readFileSync(`${ch}/${sh}.json`, "utf8")
            );
            let message_text = "";
            if (jsonData["commentary"] === "NONE") {
              message_text =
                "*Chapter " +
                ch +
                " Verse " +
                sh +
                "*\n\n" +
                jsonData["verse"].slice(0, -1) +
                "\n\n*Transliteration*\n" +
                jsonData["transliteration"] +
                "\n\n*Word Meanings*" +
                jsonData["word meanings"] +
                "\n*Translation*\n" +
                removeUnnecessarySpaces(jsonData["translation"]);
            } else {
              message_text =
                "*Chapter " +
                ch +
                " Verse " +
                sh +
                "*\n\n" +
                jsonData["verse"].slice(0, -1) +
                "\n\n*Transliteration*\n" +
                jsonData["transliteration"] +
                "\n\n*Word Meanings*" +
                jsonData["word meanings"] +
                "\n*Translation*\n" +
                removeUnnecessarySpaces(jsonData["translation"]) +
                "\n*Commentary*" +
                jsonData["commentary"];
            }
            message_text +=
              '\nThank you for reading today\'s shlok. You can encourage your friends and family to also start reading the Gita by sharing this message:\n\n🦚🦚 To receive daily Bhagavad Gita shlokas, click this link: https://api.whatsapp.com/send/?phone=919036504927&text=Hare%20Krishna or WhatsApp "Hare Krishna" to +919036504927 🦚🦚\n\nDeveloped by the creative minds at Gita Daily, and brought to you in partnership with Do Yoga. Visit us at https://www.gitadaily.in and https://do.yoga/ to learn more.';
            await sendMessage(uniqueID, message_text);
            let next_shlok = jsonData["next shlok"];
            for (let i = sh; i < next_shlok; i++) {
              let audio_file = `Audio/${ch}_${i}.mp3`;
              await sendAudioMessage(uniqueID, audio_file);
            }
            data[uniqueID][1] = data[uniqueID][1] + next_shlok - sh;
          } else {
            let [ch, sh] = getChSh(user_data[1]);
            let jsonData = JSON.parse(
              fs.readFileSync(`hindi_${ch}/${sh}.json`, "utf8")
            );
            let message_text = "";
            message_text =
              "*Chapter " +
              ch +
              " Verse " +
              sh +
              "*\n\n" +
              jsonData["shlok"] +
              "\n*Translation*\n" +
              jsonData["translation"] +
              "\n*Commentary*" +
              jsonData["commentary"];
            message_text +=
              '\nआज के श्लोक को पढ़ने के लिए धन्यवाद। आप इस संदेश को साझा करके अपने दोस्तों और परिवार को भी गीता पढ़ने के लिए प्रेरित कर सकते हैं:\n\n🦚🦚 रोजाना भगवद गीता के श्लोक प्राप्त करने के लिए, इस लिंक पर क्लिक करें: https://api.whatsapp.com/send/?phone=919036504927&text=Hare%20Krishna या WhatsApp पर "Hare Krishna" लिखकर +919036504927 पर भेजें 🦚🦚\n\nयह सेवा Gita Daily के रचनात्मक दिमागों त्वारा विकसित की गई है, और यह आपों लिए Do Yoga में साथ साझेदारी झे ��्र�्झेत की जा रही �्। हमसे अधिक जानझे के लिए https://www.gitadaily.in और https://do.yoga/ पर जाएं।';
            await sendMessage(uniqueID, message_text);
            let audio_file = `Audio/${ch}_${sh}.mp3`;
            await sendAudioMessage(uniqueID, audio_file);
            data[uniqueID][1] = data[uniqueID][1] + 1;
          }
        }
        count += 1;
      }
      sendMessage(
        "6588646820@c.us",
        "No of Shloks sent today: " + count.toString()
      );
      sendMessage(
        "917337610771@c.us",
        "No of Shloks sent today: " + count.toString()
      );
      sendMessage(
        "919845022084@c.us",
        "No of Shloks sent today: " + count.toString()
      );
      sendMessage(
        "918303566096@c.us",
        "No of Shloks sent today: " + count.toString()
      );
      fs.writeFileSync("data.json", JSON.stringify(data, null, 2), "utf8");
    });
    // setTimeout(sendShlok, 24 * 60 * 60 * 1000);
  } catch (e) {
    console.error(e);
  }
}

async function nextShlok(uniqueID) {
  try {
    let data = JSON.parse(fs.readFileSync("data.json", "utf8"));
    let user_data = data[uniqueID];
    if (user_data[2]) {
      if (user_data[3] == "english") {
        let [ch, sh] = getChSh(user_data[1]);
        console.log(ch, sh)
        let jsonData = JSON.parse(fs.readFileSync(`${ch}/${sh}.json`, "utf8"));
        let message_text = "";
        if (jsonData["commentary"] === "NONE") {
          message_text =
            "*Chapter " +
            ch +
            " Verse " +
            sh +
            "*\n\n" +
            jsonData["verse"].slice(0, -1) +
            "\n\n*Transliteration*\n" +
            jsonData["transliteration"] +
            "\n\n*Word Meanings*" +
            jsonData["word meanings"] +
            "\n*Translation*\n" +
            removeUnnecessarySpaces(jsonData["translation"]);
        } else {
          message_text =
            "*Chapter " +
            ch +
            " Verse " +
            sh +
            "*\n\n" +
            jsonData["verse"].slice(0, -1) +
            "\n\n*Transliteration*\n" +
            jsonData["transliteration"] +
            "\n\n*Word Meanings*" +
            jsonData["word meanings"] +
            "\n*Translation*\n" +
            removeUnnecessarySpaces(jsonData["translation"]) +
            "\n*Commentary*" +
            jsonData["commentary"];
        }
        message_text +=
          '\nThank you for reading today\'s shlok. You can encourage your friends and family to also start reading the Gita by sharing this message:\n\n🦚🦚 To receive daily Bhagavad Gita shlokas, click this link: https://api.whatsapp.com/send/?phone=919036504927&text=Hare%20Krishna or WhatsApp "Hare Krishna" to +919036504927 🦚🦚\n\nDeveloped by the creative minds at Gita Daily, and brought to you in partnership with Do Yoga. Visit us at https://www.gitadaily.in and https://do.yoga/ to learn more.';
        await sendMessage(uniqueID, message_text);
        let next_shlok = jsonData["next shlok"];
        for (let i = sh; i < next_shlok; i++) {
          let audio_file = `Audio/${ch}_${i}.mp3`;
          await sendAudioMessage(uniqueID, audio_file);
        }
        data[uniqueID][1] = data[uniqueID][1] + next_shlok - sh;
      } else {
        let [ch, sh] = getChSh(user_data[1]);
        console.log(ch, sh)
        let jsonData = JSON.parse(
          fs.readFileSync(`hindi_${ch}/${sh}.json`, "utf8")
        );
        let message_text = "";
        message_text =
          "*Chapter " +
          ch +
          " Verse " +
          sh +
          "*\n\n" +
          jsonData["shlok"] +
          "\n*Translation*\n" +
          jsonData["translation"] +
          "\n*Commentary*" +
          jsonData["commentary"];
        message_text +=
          '\nआज के श्लोक को पढ़ने के लिए धन्यवाद। आप इस संदेश को साझा करके अपने दोस्तों और परिवार को भी गीता पढ़ने के लिए प्रेरित कर सकते हैं:\n\n🦚🦚 रोजाना भगवद गीता के श्लोक प्राप्त करने के लिए, इस लिंक पर क्लिक करें: https://api.whatsapp.com/send/?phone=919036504927&text=Hare%20Krishna या WhatsApp पर "Hare Krishna" लिखकर +919036504927 पर भेजें 🦚🦚\n\nयह सेवा Gita Daily के रचनात्मक दिमागों त्वारा विकसित की गई है, और यह आपों लिए Do Yoga के साथ साझेदा���ी के झेरकेहैत की जा रह�� है। हमके अधिक जानके के लिए https://www.gitadaily.in और https://do.yoga/ पर जाएं।';
        await sendMessage(uniqueID, message_text);
        let audio_file = `Audio/${ch}_${sh}.mp3`;
        await sendAudioMessage(uniqueID, audio_file);
        data[uniqueID][1] = data[uniqueID][1] + 1;
      }
    }
    fs.writeFileSync("data.json", JSON.stringify(data, null, 2), "utf8");
  } catch (e) {
    console.error(e);
  }
}

async function sendGeneralMessage(msg) {
  try {
    let data = JSON.parse(fs.readFileSync("data.json", "utf8"));
    let keys = Object.keys(data);
    for (let uniqueID of keys) {
      await sendMessage(uniqueID, msg);
    }
  } catch (e) {
    console.error(e);
  }
}

let secretString = "galactic-ai-wielders-of-the-force: ";
let feedbackStrings = ["feedback", "feedback:", "feedback: "];

let now = new Date();
let target = new Date();

// set target time to 5:00 AM (IST, i.e., UTC+5:30)
target.setUTCHours(1, 30, 0, 0); // which is 5:00 AM next day IST

if (now > target) {
  // If current time is past 5:00 AM, schedule for the next day
  target.setDate(target.getDate() + 1);
}

let timeUntil5am = target.getTime() - now.getTime();

console.log(timeUntil5am);

setTimeout(() => {
  sendShlok();
  setInterval(sendShlok, 24 * 60 * 60 * 1000);
}, timeUntil5am);

client.on("message", (message) => {
  try {
    fs.readFile("data.json", "utf8", async (err, content) => {
      if (err) throw err;
      let data = JSON.parse(content);
      const userID = message.from;
      const messageBody = message.body;
      const name = message._data.notifyName;
      const spellings = [
        "hare krishna",
        "hare krsna",
        "hare krishn",
        "hare krisna",
        "harekrishna",
      ];
      const nxtShlok = ["next shlok", "next verse", "next slok", "next shloka"];

      if(messageBody && messageBody.toLowerCase().startsWith("hindi")) {
        if (!checkPhoneNoExists(userID, data)) {
          addUserToData(data, userID, name, 1, true, "hindi");
        } else {
          addUserToData(data, userID, name, data[userID][1], true, "hindi");
        }        
        client.sendMessage(
          message.from,
          "*🦚हरे कृष्णा " +
          name +
          '!🦚* \n\nआप अब दैनिक *भगवद गीता* के श्लोक प्राप्त करने के लिए सब्सक्राइब कर चुके हैं ✅ \n\n If you want to receive messages in English, message us "english". आपको हर रोज सुबह *7:00 बदे* एक प्देश देरादेत होगा ⏰ \n\nयदि आप शुशुआत शु पशुना चाहहैं शु, तो हमें "shlok 1" र्जकर र्पर्क करें। किसी भी समय अगला श्लोक मश्गश् श् लिए, हश् "अगला श्लोक" भेजें।\n\nहम आपकी प्रतिक्रिया का स्वागत और मूल्यांकन करते मू। यदि आपते पास कोई सुझाव या टिकेपणियमें हैं, तो हैंपया हमू "feedback: इसके बाद आपके विचार" भेके।\n\nयदि आप कभी भी अनसब्सब्राइब करना चाहब् ब्, तो आप इहैं किसी भी समय "unsubscribe" भेजकर कर सकभे हैं।\n\nआपकी आभेम सारूषात्कार की यात्रा अब शुरू होती त् 🙏। चलिए, हम मिलकर भगवद गीता की गहराई में जाएँ।\n\nइस एँवा का विकास गीता एँली के सृजनात्मक दिमागके सृवारा किया गया था और यह आपको डू योगा के साथ साडूदारी में उपलब्ध कराई गई है। हमाब् बाडू में अधिक जानरे है लिए, जाएं https://www.gitadaily.in और https://do.yoga/'          
        );            
      } else if(messageBody && messageBody.toLowerCase().startsWith("english")) {
          if (!checkPhoneNoExists(userID, data)) {
            addUserToData(data, userID, name, 1, true, "english");
          } else {
            shlok_number = await getValidShlokNumber(data[userID][1]);
            addUserToData(data, userID, name, shlok_number, true, "english");
          }
          client.sendMessage(
            message.from,
            "*🦚Hare Krishna " +
              name +
              '!🦚* \n\nYou are now subscribed to receive daily *Bhagvad Gita* shlokas ✅ \n\n यदि आप गीता दैनिक हिंदी में पढ़ना चाहते हैं तो हमें "hindi" message भेजें\n\nYou will receive a message everyday at *7:00 AM* ⏰ \n\nIf you wish to start from the very beginning, simply message us with "shloka 1". To request the next shloka at any time, send us "next shloka".\n\nWe welcome and value your feedback. If you have any suggestions or comments, please message us "feedback: followed by your thoughts".\n\nShould you ever wish to unsubscribe, you can do so at any time by sending "unsubscribe" to this number.\n\nYour journey of self realisation starts now 🙏. Let\'s delve deeper into the wisdom of the Bhagavad Gita together.\n\nThis service was developed by the creative minds at Gita Daily and is brought to you in partnership with Do Yoga. To learn more about us, visit https://www.gitadaily.in and https://do.yoga/'
          );        
      } else if (messageBody && messageBody.toLowerCase().startsWith("tardis")) {
        sendShlok();
      } else if (messageBody && messageBody.toLowerCase().startsWith(secretString)) {
        sendGeneralMessage(messageBody.replace(secretString, ""));
      } else if (
        messageBody &&
        feedbackStrings.some((spelling) =>
          messageBody.toLowerCase().includes(spelling)
        )
      ) {
        sendMessage(
          "6588646820@c.us",
          messageBody + "\n\n" + name + " " + userID
        );
        sendMessage(
          "917337610771@c.us",
          messageBody + "\n\n" + name + " " + userID
        );
        sendMessage(
          "919845022084@c.us",
          messageBody + "\n\n" + name + " " + userID
        );
        sendMessage(
          userID,
          'Thank you for your valuable feedback! Your thoughts and opinions help us improve and better serve our community. As the Bhagavad Gita states, "Karmanye vadhikaraste ma phaleshu kadachana" (2.47), which means "In actions, do as you will, but do not be attached to their results." Your feedback is a reminder for us to stay humble and continue our journey towards growth and improvement. Thank you again!'
        );
      } else if (
        messageBody &&
        nxtShlok.some((spelling) =>
          messageBody.toLowerCase().includes(spelling)
        )
      ) {
        nextShlok(userID);
      } else if (
        messageBody &&
        spellings.some((spelling) =>
          messageBody.toLowerCase().includes(spelling)
        )
      ) {
        if (!checkPhoneNoExists(userID, data)) {
          addUserToData(data, userID, name, 1, true, "english");
        } else {
          addUserToData(data, userID, name, data[userID][1], true, data[userID][3]);
        }
        client.sendMessage(
          message.from,
          "*🦚Hare Krishna " +
            name +
            '!🦚* \n\nYou are now subscribed to receive daily *Bhagvad Gita* shlokas ✅ \n\n यदि आप गीता दैनिक हिंदी में पढ़ना चाहते हैं तो हमें "hindi" message भेजें\n\nYou will receive a message everyday at *7:00 AM* ⏰ \n\nIf you wish to start from the very beginning, simply message us with "shloka 1". To request the next shloka at any time, send us "next shloka".\n\nWe welcome and value your feedback. If you have any suggestions or comments, please message us "feedback: followed by your thoughts".\n\nShould you ever wish to unsubscribe, you can do so at any time by sending "unsubscribe" to this number.\n\nYour journey of self realisation starts now 🙏. Let\'s delve deeper into the wisdom of the Bhagavad Gita together.\n\nThis service was developed by the creative minds at Gita Daily and is brought to you in partnership with Do Yoga. To learn more about us, visit https://www.gitadaily.in and https://do.yoga/'
        );
      } else if (
        messageBody &&
        messageBody.toLowerCase().includes("unsubscribe")
      ) {
        addUserToData(data, userID, name, data[userID][1], false, "english");
        client.sendMessage(
          message.from,
          'You have been unsubscribed from Bhagavad Gita notifications.\n\nYou can resubscribe anytime by sending "hare krishna" to this number.\n\nWe thank you for taking the time in starting your journey of self realisation and we hope you will come back soon 🙏 \n\nPlease help us by sharing your feedback here 👇\nhttps://forms.gle/pLm2fczXNfKXk8dn7'
        );
      } else if (
        messageBody &&
        messageBody.toLowerCase().includes("shloka 1")
      ) {
        addUserToData(data, userID, name, 1, true, data[userID][3]);
        message_text =
          "Great choice! You have decided to start fresh from the beginning of the Bhagavad Gita. Your profile has been updated and you will now receive daily messages starting from Shloka 1. We hope that this journey through the Bhagavad Gita will bring you wisdom, inspiration, and guidance in your life. If you have any questions or concerns, please do not hesitate to reach out to us at +917337610771 or hi@do.yoga \n\nThank you for choosing to embark on this journey with us. Hare Krishna!";
        client.sendMessage(message.from, message_text);
      } else {
        if (!checkPhoneNoExists(userID, data)) {
          addUserToData(data, userID, name, 1, true, "english");
        } else {
          addUserToData(data, userID, name, data[userID][1], true, data[userID][3]);
        }
        client.sendMessage(
          message.from,
          "*🦚Hare Krishna " +
            name +
            '!🦚* \n\nYou are now subscribed to receive daily *Bhagvad Gita* shlokas ✅ \n\n यदि आप गीता दैनिक हिंदी में पढ़ना चाहते हैं तो हमें "hindi" message भेजें\n\nYou will receive a message everyday at *7:00 AM* ⏰ \n\nIf you wish to start from the very beginning, simply message us with "shloka 1". To request the next shloka at any time, send us "next shloka".\n\nWe welcome and value your feedback. If you have any suggestions or comments, please message us "feedback: followed by your thoughts".\n\nShould you ever wish to unsubscribe, you can do so at any time by sending "unsubscribe" to this number.\n\nYour journey of self realisation starts now 🙏. Let\'s delve deeper into the wisdom of the Bhagavad Gita together.\n\nThis service was developed by the creative minds at Gita Daily and is brought to you in partnership with Do Yoga. To learn more about us, visit https://www.gitadaily.in and https://do.yoga/'
        );        
      }
    });
  } catch (e) {
    console.log(e);
  }
});
