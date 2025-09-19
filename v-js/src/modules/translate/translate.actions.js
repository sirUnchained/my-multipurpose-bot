const { Markup } = require("telegraf");
const path = require("node:path");
const fs = require("node:fs");

const usersDB = require("./../../databases/controllers/users.controller");
const actionDB = require("./../../databases/controllers/actions.controller");

let waitList = new Set();

const sendTranslationEngine = async (ctx) => {
  try {
    await ctx.editMessageText(
      "خب با چه موتوری میخوای متن هاتو ترجمه کنم؟",
      Markup.inlineKeyboard([
        [
          Markup.button.callback("google", "google"),
          Markup.button.callback("microsoft", "microsoft"),
        ],
        [Markup.button.callback("yandex", "yandex")],
        [Markup.button.callback("back", "back")],
      ])
    );
  } catch (error) {
    await ctx.reply(
      "خب با چه موتوری میخوای متن هاتو ترجمه کنم؟",
      Markup.inlineKeyboard([
        [
          Markup.button.callback("google", "google"),
          Markup.button.callback("microsoft", "microsoft"),
        ],
        [Markup.button.callback("yandex", "yandex")],
        [Markup.button.callback("back", "back")],
      ])
    );
  }
};

const sendTargetLanguage = async (ctx) => {
  await ctx.editMessageText(
    "قطعا زبان مبدا فارسیه اما بگو زبان مقصدت چیه؟",
    Markup.inlineKeyboard([
      [
        Markup.button.callback("English", "en"),
        Markup.button.callback("French", "fr"),
      ],
      [
        Markup.button.callback("German", "de"),
        Markup.button.callback("Turkish", "tr"),
      ],
      [Markup.button.callback("back", "back")],
    ])
  );
};

const translateText = async (ctx, chatId, userText) => {
  const user = usersDB.findOne("chatId", chatId);
  if (user.role !== "admin" && waitList.has(chatId)) {
    await ctx.reply("لطفا 20 ثانیه صبر کنید .");
    return;
  }
  waitList.add(chatId);

  const action = actionDB.findOne("chatId", chatId);

  const response = await fetch(
    `https://api.one-api.ir/translate/v1/${action.translation.engine}`,
    {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "one-api-token": process.env.API_TOKEN,
      },
      body: JSON.stringify({
        source: action.translation.source,
        target: action.translation.target,
        text: userText,
      }),
    }
  );
  const result = await response.json();

  const robotMsg = result.result
    ? result.result
        .replace(/\-/g, "\\-")
        .replace(/\_/g, "\\_")
        .replace(/\*/g, "\\*")
        .replace(/\[/g, "\\[")
        .replace(/\]/g, "\\]")
        .replace(/\(/g, "\\(")
        .replace(/\)/g, "\\)")
        .replace(/\~/g, "\\~")
        .replace(/\>/g, "\\>")
        .replace(/\#/g, "\\#")
        .replace(/\+/g, "\\+")
        .replace(/\=/g, "\\=")
        .replace(/\|/g, "\\|")
        .replace(/\{/g, "\\{")
        .replace(/\}/g, "\\}")
        .replace(/\./g, "\\.")
        .replace(/\!/g, "\\!")
    : result;

  if (result.status == 200) {
    await ctx.replyWithMarkdownV2(`\`${robotMsg}\``);
  } else {
    await ctx.reply("خب انگار از سمت سرویس دهنده خطا داریم.");
  }

  setTimeout(() => {
    waitList.delete(chatId);
  }, 20 * 1000);
};

module.exports = { sendTranslationEngine, sendTargetLanguage, translateText };
