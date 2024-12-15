const { Markup } = require("telegraf");
const path = require("node:path");
const fs = require("node:fs");

const usersDB = require("./../databases/controllers/users.controller");
const actionDB = require("./../databases/controllers/actions.controller");

const sendStartMsg = async (ctx) => {
  const chatId = ctx.chat.id;
  let user = usersDB.findOne("chatId", chatId);

  if (user) {
    if (
      user.name !== ctx.update.message?.from?.first_name &&
      ctx.update.message?.from?.first_name
    ) {
      usersDB.update(chatId, "name", ctx.update.message.from.first_name);
      user = usersDB.findOne("chatId", chatId);
    }

    await ctx.reply(
      `خوش برگشتی کاربر ${user.name} !`,
      Markup.inlineKeyboard([
        [
          Markup.button.callback("چت جی پی تی", "chat_gpt"),
          Markup.button.callback("ترجمه", "chose_translation_engine"),
        ],
        [
          Markup.button.callback("عکس به متن", "photo_text"),
          Markup.button.callback("اجرای کد", "chose_code_lang"),
        ],
      ])
    );
    return;
  }

  usersDB.create(chatId, ctx.update.message?.from.first_name);
  actionDB.create(chatId);

  const welcomVidPath = path.join(
    __dirname,
    "..",
    "..",
    "public",
    "welcome",
    "so_welcome_new_user.mp4"
  );
  if (fs.existsSync(welcomVidPath)) {
    await ctx.sendVideo(
      {
        source: welcomVidPath,
      },
      {
        caption: "کاربر جدید ؟؟ خوش اومدی !!",
        reply_markup: {
          inline_keyboard: [
            [
              { text: "chat_gpt", callback_data: "chat_gpt" },
              {
                text: "translation",
                callback_data: "chose_translation_engine",
              },
            ],
            [
              { text: "عکس به متن", callback_data: "photo_text" },
              { text: "اجرای کد", callback_data: "chose_code_lang" },
            ],
          ],
        },
      }
    );
    return;
  }

  await ctx.reply(
    "خوش اومدی کاربر جدید.",
    Markup.inlineKeyboard([
      [
        Markup.button.callback("chat_gpt", "chat_gpt"),
        Markup.button.callback("translation", "chose_translation_engine"),
      ],
      [
        Markup.button.callback("عکس به متن", "photo_text"),
        Markup.button.callback("اجرای کد", "chose_code_lang"),
      ],
    ])
  );
};

module.exports = { sendStartMsg };
