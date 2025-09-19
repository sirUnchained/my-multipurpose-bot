const fs = require("node:fs");
const path = require("node:path");

const dbPath = path.join(__dirname, "..", "jsons", "users.db.json");
let db = null;

const findOne = (key, value, index = false) => {
  db = fs.readFileSync(dbPath);
  db = JSON.parse(db);

  if (index) {
    const result = db.findIndex((item) => {
      return item[key] === value;
    });
    return result;
  }
  const result = db.find((item) => {
    return item[key] === value;
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

  db[itemIndex][key] = value;

  fs.writeFileSync(dbPath, JSON.stringify([...db]));
  return true;
};

const create = (chatId, name) => {
  db = fs.readFileSync(dbPath);
  db = JSON.parse(db);

  const checkExist = findOne("chatId", chatId);
  if (checkExist) return false;

  const dbDocs = db.length;

  const newData = {
    id: dbDocs ? dbDocs + 1 : 1,
    name,
    chatId,
    role: dbDocs ? "user" : "admin",
    used_count: 0,
    warn: 0,
    createdAt: new Date(),
  };

  fs.writeFileSync(dbPath, JSON.stringify([...db, newData]));
  return newData;
};

module.exports = { findOne, create, remove, update };
