from telebot import TeleBot, types
from .database import Users_db_controller, Actions_db_controller
from .keyboards import main_menu_keyboard
from .logger import Logger


def start_handler(bot: TeleBot):
    @bot.message_handler(commands=["start"])
    def welcome_handler(msg: types.Message):
        chatid = str(msg.chat.id)
        username = (
            msg.from_user.username  # type: ignore
            if msg.from_user.full_name is None  # type: ignore
            else msg.from_user.username  # type: ignore
        )
        check_user = Users_db_controller.find_single_user(chatid)

        if check_user is None:
            Users_db_controller.create_user(chatid, username)
            bot.send_message(
                msg.chat.id, "کاربر جدید! خوش اومدی!!", reply_markup=main_menu_keyboard
            )
        else:
            bot.send_message(
                msg.chat.id,
                f"خوش برگشتی {username} عزیز! چطور میتونم کمکت بکنم؟",
                reply_markup=main_menu_keyboard,
            )


def text_handler(bot: TeleBot):
    @bot.message_handler(content_types=["text"])
    def handle_text(msg: types.Message):
        chatid = str(msg.chat.id)
        user = Users_db_controller.find_single_user(chatid)
        user_action = Actions_db_controller.find_single_action(user.actions_id)  # type: ignore

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
