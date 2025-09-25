from telebot import TeleBot, apihelper
from configs import BOT_TOKEN, PROXY
from bot_modles import start

apihelper.proxy = {"https": PROXY}
bot: TeleBot = TeleBot(BOT_TOKEN, parse_mode=None)

start.register_handlers(bot)

bot.infinity_polling()
