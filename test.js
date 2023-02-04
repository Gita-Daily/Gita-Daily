let date = new Date();
date.setUTCHours(5-5.5,0,0,0);
let timeUntil5am = date.getTime() - Date.now();
console.log(timeUntil5am)



// const fs = require('fs');

// const chapter_shlokas = [47, 72, 43, 42, 29, 47, 30, 28, 34, 42, 55, 20, 34, 27, 20, 24, 28, 78];

// function getChSh(n) {
//     let ch = 1;
//     for(let n_schlokas of chapter_shlokas) {
//         if(n-n_schlokas > 0) {
//             n = n - n_schlokas;
//             ch = ch + 1;
//         } else {
//             break;
//         }
//     }
//     return [ch, n];
// }

// async function checkShlokExists(data) {
//   for (const [user, userData] of Object.entries(data)) {
//     const [ch, sh] = getChSh(userData[1]);
//     const filePath = `${ch}/${sh}.json`;
//     try {
//       await fs.promises.readFile(filePath, 'utf-8');
//     } catch (err) {
//       console.log(`File not found for user ${user}: ${filePath}`);
//     }
//   }
// }

// data = JSON.parse(fs.readFileSync('data.json', 'utf8'));
// checkShlokExists(data);

// function getPrevShlok(shlokNum) {
//     let [ch, sh] = getChSh(shlokNum);
//     sh = sh - 1;
//     if (sh === 0) {
//         ch = ch - 1;
//         sh = chapter_shlokas[ch - 1];
//     }
//     return [ch, sh];
// }

// fs.readFile('./data.json', (err, data) => {
//     if (err) throw err;

//     const users = JSON.parse(data);
//     for (let user of Object.keys(users)) {
//         let [userName, shlokNum, isSubscribed] = users[user];
//         const prevShlok = getPrevShlok(shlokNum);
//         if (prevShlok) {
//             const [ch, sh] = prevShlok;
//             const filePath = path.join(__dirname, `${ch}/${sh}.json`);
//             try {
//                 fs.accessSync(filePath, fs.constants.F_OK);
//                 users[user][1] = shlokNum - 1;
//                 // console.log(`Previous shlok for ${userName} (${user}) is ${ch}:${sh}.`);
//             } catch (error) {
//                 console.log(`File ${filePath} does not exist for user ${userName} (${user}).`);
//                 // setPrevShlok(user, sh + 1);
//             }
//         }
//     }
//     // console.log(users)
//     fs.writeFileSync('data.json', JSON.stringify(users, null, 2), 'utf8'); 
// });

// const fs = require('fs');

// async function setPrevShlok() {
//     const users = JSON.parse(await fs.promises.readFile('./data.json', 'utf-8'));
//     for (let user of Object.keys(users)) {
//         console.log(user)
//         let prevToPrev = 1;
//         let prev = 2;
//         outer:
//         for (let i = 1; i <= 18; i++) {
//             for (let j = 3; j <= chapter_shlokas[i-1]; j++) {
//             const filePath = `${i}/${j}.json`;
//             try {
//                 const fileData = JSON.parse(await fs.promises.readFile(filePath, 'utf-8'));
//                 if (j === users[user][1]) {
//                 users[user][1] = prevToPrev;
//                 break outer;
//                 }
//                 prevToPrev = prev;
//                 prev = fileData['next shlok'];
//             } catch (err) {
//                 // console.log(`Failed to read file: ${filePath}`);
//             }
//             }
//         }
//     }
//     await fs.promises.writeFile('./data.json', JSON.stringify(users));
// }

// setPrevShlok();