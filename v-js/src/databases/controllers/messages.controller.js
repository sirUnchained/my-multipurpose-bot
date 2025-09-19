const fs = require("node:fs");
const path = require("node:path");
const dbPath = path.join(__dirname, "..", "jsons", "messages.db.json");

const insert = (chatId, content, role = "user") => {
  let db = fs.readFileSync(dbPath);
  db = JSON.parse(db);

  const chatIndex = db.findIndex((item) => item.chatId == chatId);

  if (db[chatIndex].messages.length >= 5) {
    db[chatIndex].messages.shift();
    db[chatIndex].messages.push({ role, content });
    fs.writeFileSync(dbPath, JSON.stringify([...db]));
    return db[chatIndex];
  }

  db[chatIndex].messages.push({ role, content });

  fs.writeFileSync(dbPath, JSON.stringify([...db]));
  return db[chatIndex];
};

const create = (chatId) => {
  let db = fs.readFileSync(dbPath);
  db = JSON.parse(db);

  const chatIndex = db.findIndex((item) => item.chatId == chatId);
  console.log(chatIndex);
  if (chatIndex == -1) {
    const newChat = { id: db.length + 1, chatId, messages: [] };
    fs.writeFileSync(dbPath, JSON.stringify([...db, newChat]));
    return true;
  }

  return false;
};

module.exports = { insert, create };
