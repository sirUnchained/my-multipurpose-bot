const badWords = require("./../../databases/jsons/persian_swear.json");
const usersDB = require("./../../databases/controllers/users.controller");

async function checkMessageAndBAN(ctx) {
  const currentUser = usersDB.findOne("chatId", ctx.chat.id);
  const message = ctx.message.text;
  const isBad = badWords.some((text) => text === message?.trim());

  if (isBad) {
    if (currentUser.warn >= 5 && currentUser.role !== "admin") {
      await ctx.banChatMember(chatId);
      usersDB.update(chatId, "warn", 0);
    } else if (currentUser.role !== "admin") {
      await ctx.deleteMessage();
      await ctx.reply("به عصابت مسلسل باش خوشگله.");
      usersDB.update(chatId, "warn", currentUser.warn + 1);
    }
  }
}

async function checkCommandsAndRun(ctx) {
  const currentUser = usersDB.findOne("chatId", ctx.chat.id);
  const userId = ctx.message.reply_to_message.from.id;
  const message = ctx.message.text;

  switch (true) {
    case message === "/mute" && currentUser !== "admin":
      await ctx.restrictChatMember(userId, {
        permissions: {
          can_send_messages: false,
          can_send_documents: false,
          can_send_photos: false,
          can_send_audios: false,
          can_send_videos: false,
        },
      });
      break;
    case message === "/unmute" && currentUser !== "admin":
      await ctx.restrictChatMember(userId, {
        permissions: {
          can_send_messages: true,
          can_send_documents: true,
          can_send_photos: true,
          can_send_audios: true,
          can_send_videos: true,
        },
      });
      break;
    case message === "/ban" && currentUser !== "admin":
      await ctx.banChatMember(userId);
      break;
    case message === "/unban" && currentUser !== "admin":
      await ctx.unbanChatMember(userId);
      break;
    default:
      await ctx.reply("چی؟ دستورتو نفهمیدم.");
      break;
  }
}

module.exports = { checkMessageAndBAN, checkCommandsAndRun };
