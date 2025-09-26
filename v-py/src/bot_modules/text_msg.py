from telebot import TeleBot, types
from .database import Users_db_controller, Actions_db_controller
from .logger import Logger
from .handler_translation import (
    handel_change_engine_translation,
    handel_change_source_translation,
    handel_change_target_translation,
)


def text_handler(bot: TeleBot):
    @bot.message_handler(content_types=["text"])
    def handle_text(msg: types.Message):
        chatid = str(msg.chat.id)
        user = Users_db_controller.find_single_user(chatid)
        user_action = Actions_db_controller.find_single_action(user.actions_id)

        if user is None or user_action is None:
            Logger.error_log("we couldnt find user to find its actions.")
            return

        # bot.send_message(msg.chat.id, f"You said: {msg.text}")
        # print(msg.chat.id)

        if user_action.current_action == "translate":
            pass
        elif user_action.current_action == "ais":
            pass
        elif user_action.current_action == "pc_control":
            pass
        elif user_action.current_action == "text_voice":
            pass


def callback_text_handler(bot: TeleBot):
    @bot.callback_query_handler(func=lambda call: True)
    def translation_menu_menu_cb(call: types.CallbackQuery):
        if call.data.find("source") != -1:
            handel_change_source_translation(call, bot)
            return
        if call.data.find("target") != -1:
            handel_change_target_translation(call, bot)
            return
        if call.data.find("engine") != -1:
            handel_change_engine_translation(call, bot)
            return
