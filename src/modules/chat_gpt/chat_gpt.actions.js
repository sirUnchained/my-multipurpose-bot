const usersDB = require("./../../databases/controllers/users.controller");
const actionDB = require("./../../databases/controllers/actions.controller");
const { Markup } = require("telegraf");
const { insert } = require("../../databases/controllers/messages.controller");

const waitList = new Set();
const maxFreeUser = 20;

const sendGptResult = async (ctx, chatId, userText) => {

  const user = usersDB.findOne("chatId", chatId);

  if (user.used_count >= maxFreeUser && user.role !== "admin") {

    await ctx.reply("عزیزم شرمنده محدودیت ۲۰ درخواست در هفته شما فعلا پر شده.");

    return;

  }

  if (user.role !== "admin" && waitList.has(chatId)) {

    await ctx.reply("لطفا بعد از ده ثانیه دوباره پیام دهید.");

    return;

  }

  waitList.add(chatId);



  const actions = actionDB.findOne("chatId", chatId);

  if (actions?.gpt) {

    const pleasWaitMsg = await ctx.reply("لطفا کمی صبر کنید ...");



    const chat = insert(chatId, userText, "user");



    const response = await fetch(

      `https://api.one-api.ir/chatbot/v1/${actions.gpt}`,

      {

        method: "POST",

        headers: {

          "content-type": "application/json",

          "one-api-token": process.env.API_TOKEN,

        },

        body: JSON.stringify(chat.messages),

      }

    );



    const result = await response.json();

    const robotMsg = result.result

      ? result.result[0]

          .replaceAll(/\\/g, "")

          .replace(/\-/g, "\\-")

          .replace(/\_/g, "\\_")

          // .replace(/\*/g, "\\*")

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



    if (result.status === 200) {

      await ctx.deleteMessage(pleasWaitMsg.message_id);



      let sendingResult = "";

      for (let i = 0; i < robotMsg.length; i += 4090) {

        sendingResult = robotMsg.slice(i, i + 4090);
        try{
            await ctx.replyWithMarkdownV2(sendingResult);
        } catch(err) {
            await ctx.reply(result.result[0].slice(i, i + 4090));
        }
      }
      usersDB.update(chatId, "used_count", user.used_count + 1);
      insert(chatId, result.result[0], "assistant");

    } else {

      await ctx.deleteMessage(pleasWaitMsg.message_id);

      await ctx.reply("مشکلی از سمت سرویس پیش امده.");

    }

  } else {

    await ctx.reply("مثل اینکه کزینه های ربات رو انتخاب نکردی ...");

  }



  setTimeout(() => {

    waitList.delete(chatId);

  }, 10 * 1000);

};



const sendGptOptions = async (ctx) => {

  try {

    await ctx.editMessageText(

      "یکی از گزینه هارو انتخاب کن:",

      Markup.inlineKeyboard([

        [

          Markup.button.callback("gpt4o", "gpt4o"),

          Markup.button.callback("gpt3-turbo", "turbo"),

        ],

        [Markup.button.callback("back", "back")],

      ])

    );

  } catch (error) {
    await ctx.reply(
      "یکی از گزینه هارو انتخاب کن:",
      Markup.inlineKeyboard([
        [
          Markup.button.callback("gpt4o", "gpt4o"),
          Markup.button.callback("gpt3-turbo", "turbo"),
        ],
        [Markup.button.callback("back", "back")],
      ])
    );
  }
};

module.exports = { sendGptResult, sendGptOptions };            
