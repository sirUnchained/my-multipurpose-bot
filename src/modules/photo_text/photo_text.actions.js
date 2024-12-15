const { Markup } = require("telegraf");

const fs = require("node:fs");
const path = require("node:path");
const { default: axios } = require("axios");
const Tesseract = require("tesseract.js");

const actionsDB = require("./../../databases/controllers/actions.controller");
const usersDB = require("./../../databases/controllers/users.controller");

const watingList = new Set();

const readPicSendText = async (ctx) => {
  const chatId = ctx.chat.id;
  const user = usersDB.findOne("chatId", chatId);
  if (user.role !== "admin" && watingList.has(chatId)) {
    await ctx.reply("لطفا ۲۰ ثانیه دیگر دوباره عکس بفرستید.");
    return;
  }

  const actions = actionsDB.findOne("chatId", chatId);
  const fileId = ctx.message.photo[ctx.message.photo.length - 1].file_id;
  const fileLink = await ctx.telegram.getFileLink(fileId);

  const response = await axios({
    url: fileLink,
    responseType: "arraybuffer",
  });
  if (response.status != 200) {
    ctx.reply("از سمت تلگرام مشکلی برای گرفتن عکس پیش اومده.");
    return;
  }

  const imagePath = path.join(
    __dirname,
    "..",
    "..",
    "..",
    "public",
    "temp.png"
  );
  fs.writeFileSync(imagePath, response.data);

  const result = await scanPic(imagePath, actions.pic_lang, 5000);

  fs.unlinkSync(imagePath);

  try {
    const robotMsg = result.data?.text ? result.data.text : result;

    await ctx.replyWithMarkdownV2(`\`${robotMsg}\``);
  } catch (error) {
    await ctx.reply(error.message);
  }

  setTimeout(() => {
    watingList.delete(chatId);
  }, 20 * 1000);
};

const selectPicLang = async (ctx) => {
  try {
    await ctx.editMessageText(
      "یکی از گزینه هارو انتخاب کن:",
      Markup.inlineKeyboard([
        [
          Markup.button.callback("English", "eng"),
          Markup.button.callback("French", "fra"),
        ],
        [
          Markup.button.callback("German", "deu"),
          Markup.button.callback("Turkish", "tur"),
        ],
        [
          Markup.button.callback("فارسی", "fas"),
          Markup.button.callback("back", "back"),
        ],
      ])
    );
  } catch (error) {
    await ctx.reply(
      "یکی از گزینه هارو انتخاب کن:",
      Markup.inlineKeyboard([
        [
          Markup.button.callback("English", "eng"),
          Markup.button.callback("French", "fra"),
        ],
        [
          Markup.button.callback("German", "deu"),
          Markup.button.callback("Turkish", "tur"),
        ],
        [
          Markup.button.callback("فارسی", "fas"),
          Markup.button.callback("back", "back"),
        ],
      ])
    );
  }
};

async function scanPic(imagePath, lang, time) {
  const tesseractPromise = Tesseract.recognize(imagePath, lang);
  const timerPromise = new Promise((resolve) => {
    setTimeout(
      () => resolve("تبدیل بیش از حد طول کشید به خاطر همین پروسه رو لغو کردم."),
      time
    );
  });

  try {
    const result = await Promise.race([tesseractPromise, timerPromise]);
    return result;
  } catch (error) {
    console.log("pic err =>", error);
  }
}

module.exports = { readPicSendText, selectPicLang };
