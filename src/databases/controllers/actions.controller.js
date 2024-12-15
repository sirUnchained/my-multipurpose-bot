const fs = require("node:fs");
const path = require("node:path");
const dbPath = path.join(__dirname, "..", "jsons", "action.db.json");
let db = null;

const findOne = (key, value, index = false) => {
  db = fs.readFileSync(dbPath);
  db = JSON.parse(db);

  if (index) {
    const result = db.findIndex((item) => {
      return item[key] == value;
    });
    return result;
  }
  const result = db.find((item) => {
    return item[key] == value;
  });
  return result !== undefined ? result : false;
};

const remove = (key, value) => {
  db = fs.readFileSync(dbPath);
  db = JSON.parse(db);

  const itemIndex = findOne(key, value, true);
  if (itemIndex == -1) return false;

  db.splice(itemIndex, 1);

  fs.writeFileSync(dbPath, JSON.stringify([...db]));
  return true;
};

const update = (chatId, key, value) => {
  db = fs.readFileSync(dbPath);
  db = JSON.parse(db);

  const itemIndex = findOne("chatId", chatId, true);
  if (itemIndex == -1) return false;

  if (key === "t_lang") {
    db[itemIndex].translation.target = value;
    fs.writeFileSync(dbPath, JSON.stringify([...db]));
    return true;
  } else if (key === "t_engine") {
    db[itemIndex].translation.engine = value;
    fs.writeFileSync(dbPath, JSON.stringify([...db]));
    return true;
  }

  db[itemIndex][key] = value;

  fs.writeFileSync(dbPath, JSON.stringify([...db]));
  return true;
};

const create = (chatId) => {
  db = fs.readFileSync(dbPath);
  db = JSON.parse(db);

  const checkExist = findOne("chatId", chatId);
  if (checkExist) return false;

  const newData = {
    id: crypto.randomUUID(),
    chatId,
    createdAt: new Date(),
    gpt: "gpt3.5-turbo",
    translation: {
      engine: "google",
      source: "fa",
      target: "en",
    },
    pic_lang: "eng",
    code_with: "py",
    current_status: null,
  };

  fs.writeFileSync(dbPath, JSON.stringify([...db, newData]));
  return newData;
};

module.exports = { findOne, create, remove, update };
