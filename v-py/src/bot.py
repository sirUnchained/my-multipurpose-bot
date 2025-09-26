from telebot import TeleBot, apihelper
from bot_modules.configs import BOT_TOKEN, PROXY
from bot_modules import start_msg, text_msg

apihelper.proxy = {"https": PROXY}
bot: TeleBot = TeleBot(BOT_TOKEN, parse_mode=None)

start_msg.start_handler(bot)
start_msg.callback_start_handler(bot)

text_msg.text_handler(bot)
text_msg.callback_text_handler(bot)

bot.infinity_polling()
