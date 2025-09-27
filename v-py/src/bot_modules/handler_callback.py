from telebot import TeleBot, types
from .database import (
    Users_db_controller,
    Actions_db_controller,
    Translation_db_controller,
)
from .logger import Logger
from .keyboards import (
    select_translation_option,
    source_translation_menu,
    target_translation_menu,
    engine_translation_menu,
)


def callback_translation_setting(bot: TeleBot):
    @bot.callback_query_handler(
        func=lambda call: (
            call.data.find("source") == 0
            or call.data.find("target") == 0
            or call.data.find("engine") == 0
        )
    )
    def translation_menu_cb(call: types.CallbackQuery):
        callback_id = call.id
        chatid = str(call.message.chat.id)
        user = Users_db_controller.find_single_user(chatid)
        action = Actions_db_controller.find_single_action(user.actions_id)  # type: ignore
        old_translation = Translation_db_controller.find_single_translation(
            action.translations_id  # type: ignore
        )

        if call.data.find("source") != -1:  # type: ignore
            translations = {
                "source": call.data.split("_")[1],  # type: ignore
                "target": old_translation.target,  # type: ignore
                "engine": old_translation.engine,  # type: ignore
            }

            if translations.get("source") == old_translation.source:  # type: ignore
                bot.answer_callback_query(
                    callback_id,
                    text=f"زبان مبدا و مقصد نباید یکی باشه.",
                )
                return

            Translation_db_controller.update_translation(action.id, translations)  # type: ignore

            bot.answer_callback_query(
                callback_id,
                text=f"خب زبان مقصد {translations.get('source')} است٬ زبان مبدا {translations.get('target')} است و موتور ترجمه {translations.get('engine')} است.",
            )
            bot.delete_message(chatid, call.message.id)  # type: ignore
        elif call.data.find("target") != -1:  # type: ignore
            translations = {
                "source": old_translation.source,  # type: ignore
                "target": call.data.split("_")[1],  # type: ignore
                "engine": old_translation.engine,  # type: ignore
            }

            if translations.get("source") == old_translation.target:  # type: ignore
                bot.answer_callback_query(
                    callback_id,
                    text=f"زبان مبدا و مقصد نباید یکی باشه.",
                )
                return

            Translation_db_controller.update_translation(action.id, translations)  # type: ignore

            bot.answer_callback_query(
                callback_id,
                f"خب زبان مقصد {translations.get('source')} است٬ زبان مبدا {translations.get('target')} است و موتور ترجمه {translations.get('engine')} است.",
            )
            bot.delete_message(chatid, call.message.id)  # type: ignore

        elif call.data.find("engine") != -1:  # type: ignore
            translations = {
                "source": old_translation.source,  # type: ignore
                "target": old_translation.target,  # type: ignore
                "engine": call.data.split("_")[1],  # type: ignore
            }

            if translations.get("source") == old_translation.engine:  # type: ignore
                bot.answer_callback_query(
                    callback_id,
                    text=f"زبان مبدا و مقصد نباید یکی باشه.",
                )
                return

            Translation_db_controller.update_translation(action.id, translations)  # type: ignore

            bot.answer_callback_query(
                callback_id,
                f"خب زبان مقصد {translations.get('source')} است٬ زبان مبدا {translations.get('target')} است و موتور ترجمه {translations.get('engine')} است.",
            )
            bot.delete_message(chatid, call.message.id)  # type: ignore


def callback_change_translation_setting(bot: TeleBot):
    @bot.callback_query_handler(
        func=lambda call: call.data
        in ["change_lang_source", "change_lang_target", "change_lang_engine"]
    )
    def send_change_translation_setting_menu(call: types.CallbackQuery):
        chatid = str(call.message.chat.id)

        if call.data == "change_lang_source":  # type: ignore
            bot.send_message(
                chatid,
                text="خب زبان منبع رو انتخاب کن:",
                reply_markup=source_translation_menu,
            )
        elif call.data == "change_lang_target":  # type: ignore
            bot.send_message(
                chatid,
                text="خب زبان مبدا رو انتخاب کن:",
                reply_markup=target_translation_menu,
            )
        elif call.data == "change_lang_engine":  # type: ignore
            bot.send_message(
                chatid,
                text="خب موتور ترجمه رو انتخاب کن:",
                reply_markup=engine_translation_menu,
            )


def callback_start_handler(bot: TeleBot):
    @bot.callback_query_handler(
        func=lambda call: call.data
        in [
            "openai",
            "translate",
            "control_my_pc",
            "text_voice",
        ]
    )
    def handle_main_menu_callback(call: types.CallbackQuery):
        chatid = str(call.message.chat.id)
        user = Users_db_controller.find_single_user(chatid)

        if call.data == "openai":
            Actions_db_controller.update_action(user.actions_id, "current_action", "ais")  # type: ignore
            bot.send_message(chatid, "خب پیاماتو از این به بعد چت جی پی تی می بینه.")
        elif call.data == "translate":
            Actions_db_controller.update_action(
                user.actions_id, "current_action", "translate"  # type: ignore
            )
            bot.send_message(
                chatid,
                "فهمیدم از الان به بعد پیام هاتو ترجمه میکنم٬ میتونی تنظیمات رو از منو زیر تغییر بدی.",
                reply_markup=select_translation_option,
            )

            # bot.edit_message_text(
            #     "فهمیدم از الان به بعد پیام هاتو ترجمه میکنم٬ میتونی تنظیمات رو از منو زیر تغییر بدی.",
            #     chat_id=chatid,
            #     message_id=call.message.message_id,
            #     reply_markup=select_translation_option,
            # )
        elif call.data == "control_my_pc":
            Actions_db_controller.update_action(
                user.actions_id, "current_action", "pc_control"  # type: ignore
            )
            bot.send_message(chatid, "هنوز زوده شیطون.")
        elif call.data == "text_voice":
            Actions_db_controller.update_action(
                user.actions_id, "current_action", "text_voice"  # type: ignore
            )
            bot.send_message(chatid, "خب الان هر متنی بدی بهت ویس میدم.")
