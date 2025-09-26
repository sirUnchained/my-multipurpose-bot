from telebot import TeleBot, types
from .database import (
    Users_db_controller,
    Actions_db_controller,
    Translation_db_controller,
)
from .logger import Logger


def handel_change_target_translation(call: types.CallbackQuery, bot: TeleBot):
    chatid = str(call.message.chat.id)
    user = Users_db_controller.find_single_user(chatid)
    action = Actions_db_controller.find_single_action(user.actions_id)
    old_translation = Translation_db_controller.find_single_translation(
        action.translations_id
    )

    translations = {
        "source": old_translation.source,
        "target": call.data.split("_")[1],
        "engine": old_translation.engine,
    }

    Translation_db_controller.update_translation(action.id, translations)

    bot.send_message(
        chatid,
        f"خب زبان مقصد {translations.get('source')} است٬ زبان مبدا {translations.get('target')} است و موتور ترجمه {translations.get('engine')}است.",
    )


def handel_change_source_translation(call: types.CallbackQuery, bot: TeleBot):
    chatid = str(call.message.chat.id)
    user = Users_db_controller.find_single_user(chatid)
    action = Actions_db_controller.find_single_action(user.actions_id)
    old_translation = Translation_db_controller.find_single_translation(
        action.translations_id
    )

    translations = {
        "source": call.data.split("_")[1],
        "target": old_translation.target,
        "engine": old_translation.engine,
    }

    Translation_db_controller.update_translation(action.id, translations)

    bot.send_message(
        chatid,
        f"خب زبان مقصد {translations.get('source')} است٬ زبان مبدا {translations.get('target')} است و موتور ترجمه {translations.get('engine')}است.",
    )


def handel_change_engine_translation(call: types.CallbackQuery, bot: TeleBot):
    chatid = str(call.message.chat.id)
    user = Users_db_controller.find_single_user(chatid)
    action = Actions_db_controller.find_single_action(user.actions_id)
    old_translation = Translation_db_controller.find_single_translation(
        action.translations_id
    )

    translations = {
        "source": old_translation.source,
        "target": old_translation.target,
        "engine": call.data.split("_")[1],
    }

    Translation_db_controller.update_translation(action.id, translations)

    bot.send_message(
        chatid,
        f"خب زبان مقصد {translations.get('source')} است٬ زبان مبدا {translations.get('target')} است و موتور ترجمه {translations.get('engine')}است.",
    )
