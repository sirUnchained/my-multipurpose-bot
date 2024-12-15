const {
  sendTranslationEngine,
  sendTargetLanguage,
} = require("./translate.actions");
const actionsDB = require("./../../databases/controllers/actions.controller");

function translateEvents(bot) {
  bot.action("chose_translation_engine", async (ctx) => {
    actionsDB.update(ctx.chat.id, "current_status", "translation");

    await sendTranslationEngine(ctx);
  });
  bot.action("google", async (ctx) => {
    actionsDB.update(ctx.chat.id, "t_engine", "google");

    await sendTargetLanguage(ctx);
  });
  bot.action("microsoft", async (ctx) => {
    actionsDB.update(ctx.chat.id, "t_engine", "microsoft");

    await sendTargetLanguage(ctx);
  });
  bot.action("yandex", async (ctx) => {
    actionsDB.update(ctx.chat.id, "t_engine", "yandex");

    await sendTargetLanguage(ctx);
  });
  bot.action("en", async (ctx) => {
    actionsDB.update(ctx.chat.id, "t_lang", "en");

    await ctx.reply("خب حالا متن فارسی رو بده ببینیم چه میکنم .");
  });
  bot.action("fr", async (ctx) => {
    actionsDB.update(ctx.chat.id, "t_lang", "fr");

    await ctx.reply("خب حالا متن فارسی رو بده ببینیم چه میکنم .");
  });
  bot.action("de", async (ctx) => {
    actionsDB.update(ctx.chat.id, "t_lang", "de");

    await ctx.reply("خب حالا متن فارسی رو بده ببینیم چه میکنم .");
  });
  bot.action("tr", async (ctx) => {
    actionsDB.update(ctx.chat.id, "t_lang", "tr");

    await ctx.reply("خب حالا متن فارسی رو بده ببینیم چه میکنم .");
  });
}

module.exports = translateEvents;
