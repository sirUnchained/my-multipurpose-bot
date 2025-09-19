const { selectPicLang } = require("./photo_text.actions");
const actionsDB = require("./../../databases/controllers/actions.controller");

function photoTextEvents(bot) {
  bot.action("photo_text", async (ctx) => {
    await selectPicLang(ctx);
  });
  bot.action("eng", async (ctx) => {
    const chatId = ctx.chat.id;
    actionsDB.update(chatId, "pic_lang", "eng");

    await ctx.reply("خب حالا عکسو بده ببینم چه میکنم.");
  });
  bot.action("fra", async (ctx) => {
    const chatId = ctx.chat.id;
    actionsDB.update(chatId, "pic_lang", "fra");

    await ctx.reply("خب حالا عکسو بده ببینم چه میکنم.");
  });
  bot.action("deu", async (ctx) => {
    const chatId = ctx.chat.id;
    actionsDB.update(chatId, "pic_lang", "deu");

    await ctx.reply("خب حالا عکسو بده ببینم چه میکنم.");
  });
  bot.action("tur", async (ctx) => {
    const chatId = ctx.chat.id;
    actionsDB.update(chatId, "pic_lang", "tur");

    await ctx.reply("خب حالا عکسو بده ببینم چه میکنم.");
  });
  bot.action("fas", async (ctx) => {
    const chatId = ctx.chat.id;
    actionsDB.update(chatId, "pic_lang", "fas");

    await ctx.reply("خب حالا عکسو بده ببینم چه میکنم.");
  });
}

module.exports = photoTextEvents;
