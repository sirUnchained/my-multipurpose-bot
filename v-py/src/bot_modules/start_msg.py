from telebot import TeleBot, types
from .handler_start import welcome_handler, handle_main_menu_callback


def start_handler(bot: TeleBot):
    @bot.message_handler(commands=["start"])
    def handle_start(msg: types.Message):
        welcome_handler(msg, bot)


def callback_start_handler(bot: TeleBot):
    @bot.callback_query_handler(func=lambda call: True)
    def main_menu_cb(call: types.CallbackQuery):
        handle_main_menu_callback(call, bot)
