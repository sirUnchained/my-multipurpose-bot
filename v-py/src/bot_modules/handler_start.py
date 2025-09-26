from telebot import TeleBot, types
from .database import Users_db_controller, Actions_db_controller
from .keyboards import main_menu_keyboard, 
from .logger import Logger


def welcome_handler(msg: types.Message, bot: TeleBot):
    chatid = str(msg.chat.id)
    username = (
        msg.from_user.username
        if msg.from_user.full_name is None
        else msg.from_user.username
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


def handle_main_menu_callback(call: types.CallbackQuery, bot: TeleBot):
    chatid = str(call.message.chat.id)
    user = Users_db_controller.find_single_user(chatid)

    if user is None:
        Logger.error_log("handle_main_menu_callback user not found.")
        return

    if call.data == "openai":
        Actions_db_controller.update_action(user.actions_id, "current_action", "ais")
        bot.send_message(chatid, "خب پیاماتو از این به بعد چت جی پی تی می بینه.")
    elif call.data == "translate":
        Actions_db_controller.update_action(
            user.actions_id, "current_action", "translate"
        )
        bot.send_message(chatid, "خب بگو ببینم چه زبونی رو به چه زبونی ترجمه کنم؟", reply_markup=)
    elif call.data == "control_my_pc":
        Actions_db_controller.update_action(
            user.actions_id, "current_action", "pc_control"
        )
        bot.send_message(chatid, "هنوز زوده شیطون.")
    elif call.data == "text_voice":
        Actions_db_controller.update_action(
            user.actions_id, "current_action", "text_voice"
        )
        bot.send_message(chatid, "خب الان هر متنی بدی بهت ویس میدم.")
