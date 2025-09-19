const { sendCompileLangs } = require("./code.actions");
const actionsDB = require("./../../databases/controllers/actions.controller");

function codeEvents(bot) {
  bot.action("chose_code_lang", async (ctx) => {
    const chatId = ctx.chat.id;
    actionsDB.update(chatId, "current_status", "coding");

    await sendCompileLangs(ctx);
  });
  bot.action("js", async (ctx) => {
    const chatId = ctx.chat.id;
    actionsDB.update(chatId, "code_with", "js");

    await ctx.reply("خب حالا کدی که با جاوا اسکریپت نوشتی رو بفرست.");
  });
  bot.action("py", async (ctx) => {
    const chatId = ctx.chat.id;
    actionsDB.update(chatId, "code_with", "py");

    await ctx.reply("خب حالا کدی که با پایتون نوشتی رو بفرست.");
  });
  bot.action("cpp", async (ctx) => {
    const chatId = ctx.chat.id;
    actionsDB.update(chatId, "code_with", "cpp");

    await ctx.reply("خب حالا کدی که با سی پلاس پلاس نوشتی رو بفرست.");
  });
}

module.exports = codeEvents;
