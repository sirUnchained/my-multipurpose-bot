from telebot import TeleBot, types
from .database import (
    Users_db_controller,
    Actions_db_controller,
    Translation_db_controller,
)
from .keyboards import main_menu_keyboard
from .configs import API_TOKEN, API_URL
from .logger import Logger
import requests


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
        action = Actions_db_controller.find_single_action(user.actions_id)  # type: ignore
        translation = Translation_db_controller.find_single_translation(
            action.translations_id  # type: ignore
        )

        # bot.send_message(msg.chat.id, f"You said: {msg.text}")
        # print(msg.chat.id)

        if action.current_action == "translate":  # type: ignore
            url = API_URL + "/openai/v1/"
            payload = {
                "source": translation.source,  # type: ignore
                "target": translation.target,  # type: ignore
                "text": msg.text,
            }
            headers = {"one-api-token": API_TOKEN}
            try:
                response = requests.post(url, json=payload, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    translated_text = data.get("result", "ترجمه‌ای یافت نشد.")
                    print(translated_text, data)
                    bot.send_message(msg.chat.id, translated_text)
                else:
                    bot.send_message(
                        msg.chat.id, "خطا در ترجمه. لطفا دوباره امتحان کنید."
                    )
            except Exception as e:
                Logger.error_log(f"Translation error: {e}")
                bot.send_message(msg.chat.id, "خطا در ترجمه. لطفا دوباره امتحان کنید.")
        elif action.current_action == "ais":  # type: ignore
            url = API_URL + "/openai/v1/chat/completions"  # type: ignore
            payload = {
                "model": "gpt-4",
                "messages": [{"role": "system", "content": msg.text}],
                "temperature": 1,
                "max_tokens": 100,
            }
            headers = {"one-api-token": API_TOKEN}
            try:
                response = requests.post(url, json=payload, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    ai_msg = (
                        data.get("result", {})
                        .get("choices", [{}])[0]
                        .get("message", {})
                        .get("content", "پاسخی یافت نشد.")
                    )
                    print(ai_msg, data)
                    bot.send_message(msg.chat.id, ai_msg)
                else:
                    bot.send_message(
                        msg.chat.id, "خطا در ارتباط با چت بات. لطفا دوباره امتحان کنید."
                    )
            except Exception as e:
                Logger.error_log(f"Translation error: {e}")
                bot.send_message(
                    msg.chat.id, "خطا در ارتباط با چت بات. لطفا دوباره امتحان کنید."
                )
        elif action.current_action == "pc_control":  # type: ignore
            pass
        elif action.current_action == "text_voice":  # type: ignore
            url = API_URL + "/tts/v1/google"  # type: ignore
            payload = {"lang": action.voice_lang, "text": msg.text}  # type: ignore
            headers = {"one-api-token": API_TOKEN}
            try:
                response = requests.post(url, json=payload, headers=headers)
                if response.status_code == 200:
                    audio_bytes = response.content
                    bot.send_voice(msg.chat.id, audio_bytes)
                else:
                    bot.send_message(
                        msg.chat.id, "خطا در تبدیل متن به صدا. لطفا دوباره امتحان کنید."
                    )
            except Exception as e:
                Logger.error_log(f"TTS error: {e}")
                bot.send_message(
                    msg.chat.id, "خطا در تبدیل متن به صدا. لطفا دوباره امتحان کنید."
                )
