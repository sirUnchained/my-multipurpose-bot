const actionsDB = require("./../../databases/controllers/actions.controller");
const { sendGptOptions } = require("./chat_gpt.actions");

const sayHello = [
  "سلام عزیزم چه کمکی از من ساخته است؟",
  "درود برتو کاربر گرامی چطور کمکت کنم؟",
  "وقت بخیر چطور میتونم کمکت کنم؟",
  "سلام امیدوارم حالت عالی باشه چه کمکی از من بر میاد؟",
  "Hello user, how can i help you?",
  "Howdy doody, how can i help you?",
  "سلام عزیزم چه کمکی از من ساخته است؟",
  "سلام جیگر چه کاری ازم برمیاد؟",
  "hallo mein Freund, wie kann ich dir helfen?",
  "مرحباً صديقي، كيف يمكنني مساعدتك؟",
];
function chatGptEvents(bot) {
  bot.action("chat_gpt", async (ctx) => {
    actionsDB.update(ctx.chat.id, "current_status", "gpt");

    await sendGptOptions(ctx);
  });
  bot.action("turbo", async (ctx) => {
    actionsDB.update(ctx.chat.id, "gpt", "gpt3.5-turbo");

    try {
      await ctx.editMessageText(sayHello[Math.floor(Math.random() * 10)]);
    } catch (error) {
      await ctx.reply(sayHello[Math.floor(Math.random() * 10)]);
    }
  });
  bot.action("gpt4o", async (ctx) => {
    actionsDB.update(ctx.chat.id, "gpt", "gpt4o");

    try {
      await ctx.editMessageText(sayHello[Math.floor(Math.random() * 10)]);
    } catch (error) {
      await ctx.reply(sayHello[Math.floor(Math.random() * 10)]);
    }
  });
}

module.exports = chatGptEvents;
