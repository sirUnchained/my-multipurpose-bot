from telebot import TeleBot, apihelper
from bot_modules.configs import BOT_TOKEN, PROXY
from bot_modules import handler_msg, handler_callback

apihelper.proxy = {"https": PROXY}
bot: TeleBot = TeleBot(BOT_TOKEN, parse_mode=None)

handler_msg.start_handler(bot)
handler_callback.callback_start_handler(bot)

handler_msg.text_handler(bot)
handler_callback.callback_translation_setting(bot)

handler_callback.callback_change_translation_setting(bot)
handler_callback.callback_change_voice_lang(bot)

bot.infinity_polling()
