const { Telegraf } = require("telegraf");

const actionsDB = require("./databases/controllers/actions.controller");
const usersDB = require("./databases/controllers/users.controller");

const { sendStartMsg } = require("./actions/actions");
const { sendGptResult } = require("./modules/chat_gpt/chat_gpt.actions");
const { translateText } = require("./modules/translate/translate.actions");
const { readPicSendText } = require("./modules/photo_text/photo_text.actions");
const {
  checkMessageAndBAN,
  checkCommandsAndRun,
} = require("./modules/group_administration/group_administration.actions");
const { compileCode } = require("./modules/code/code.actions");
// events
const chatGptEvents = require("./modules/chat_gpt/chat_gpt.events");
const translateEvents = require("./modules/translate/translate.events");
const photoTextEvents = require("./modules/photo_text/photo_text.events");
const codeEvents = require("./modules/code/code.events");

const bot = new Telegraf(process.env.BOT_TOKEN);

bot.start(async (ctx) => {
  await sendStartMsg(ctx);
});
bot.help(async (ctx) => {
  await ctx.react("👀");
});

chatGptEvents(bot);
translateEvents(bot);
photoTextEvents(bot);
// codeEvents(bot);

// group administration
bot.on("new_chat_members", async (ctx) => {
  if (!usersDB.findOne("chatId", ctx.chat.id)) {
    usersDB.create(ctx.chat.id, ctx.update.message?.from.first_name);
  }
  await ctx.reply(
    `خوش اومدی ${ctx.message.new_chat_members[0].first_name} عزیز.`
  );
});
bot.on("left_chat_member", async (ctx) => {
  await ctx.reply(`کاربر ${ctx.message.left_chat_member.first_name} لفت داد.`);
});

bot.on("text", async (ctx) => {
  const userText = ctx.text;
  const chatId = ctx.chat.id;
  const action = actionsDB.findOne("chatId", chatId);
  const currentUser = usersDB.findOne("chatId", chatId);
  const chatType = ctx.chat.type;

  if (chatType === "private") {
    switch (true) {
      case action.current_status === "gpt":
        await sendGptResult(ctx, chatId, userText);
        break;
      case action.current_status === "translation":
        await translateText(ctx, chatId, userText);
        break;

      case action.current_status === "coding":
        await compileCode(ctx);
        break;

      default:
        await ctx.reply("هنوز تعیین نکردی برات چیکار کنم.");
        break;
    }
  } else {
    await checkMessageAndBAN(ctx);

    if (ctx.message.reply_to_message) await checkCommandsAndRun(ctx);
  }
});
bot.on("photo", async (ctx) => {
  await readPicSendText(ctx);
});
bot.action("back", async (ctx) => {
  actionsDB.update(ctx.chat.id, "current_status", null);
  await sendStartMsg(ctx);
});

bot
  .launch()
  .then(() => {
    console.log("robot is running !");
  })
  .catch((err) => {
    console.log("error =>", err);
  });
