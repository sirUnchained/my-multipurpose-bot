from telebot import TeleBot
from .actions.welcome import welcome_action


def register_handlers(bot: TeleBot):
    @bot.message_handler(commands=["start"])
    def handle_start(msg):
        welcome_action(msg, bot)
