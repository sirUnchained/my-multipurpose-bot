from telebot import types

# main menu buttons
ais_btn = types.InlineKeyboardButton(text="هوش مصنوعی", callback_data="openai")
translate_btn = types.InlineKeyboardButton(text="ترجمه", callback_data="translate")
text_voice_btn = types.InlineKeyboardButton(
    text="متن به ویس", callback_data="text_voice"
)
control_my_pc_btn = types.InlineKeyboardButton(
    text="کنترل ویندوز", callback_data="control_my_pc"
)
main_menu_keyboard = types.InlineKeyboardMarkup(row_width=2)
main_menu_keyboard.add(ais_btn, translate_btn, text_voice_btn, control_my_pc_btn)

# chose source translation buttons
source_lang_fa = types.InlineKeyboardButton(text="fa", callback_data="source_fa")
source_lang_en = types.InlineKeyboardButton(text="en", callback_data="source_en")
source_lang_de = types.InlineKeyboardButton(text="de", callback_data="source_de")
source_lang_tr = types.InlineKeyboardButton(text="tr", callback_data="source_tr")
source_lang_ru = types.InlineKeyboardButton(text="ru", callback_data="source_ru")
source_translation_menu = types.InlineKeyboardMarkup(row_width=2)
source_translation_menu.add(
    source_lang_fa, source_lang_en, source_lang_de, source_lang_tr, source_lang_ru
)
# chose target translation buttons
target_lang_fa = types.InlineKeyboardButton(text="fa", callback_data="target_fa")
target_lang_en = types.InlineKeyboardButton(text="en", callback_data="target_en")
target_lang_de = types.InlineKeyboardButton(text="de", callback_data="target_de")
target_lang_tr = types.InlineKeyboardButton(text="tr", callback_data="target_tr")
target_lang_ru = types.InlineKeyboardButton(text="ru", callback_data="target_ru")
target_translation_menu = types.InlineKeyboardMarkup(row_width=2)
target_translation_menu.add(
    target_lang_fa, target_lang_en, target_lang_de, target_lang_tr, target_lang_ru
)
# chose translation engine
google = types.InlineKeyboardButton(text="google", callback_data="engine_google")
microsoft = types.InlineKeyboardButton(
    text="microsoft", callback_data="engine_microsoft"
)
yandex = types.InlineKeyboardButton(text="yandex", callback_data="engine_yandex")
engine_translation_menu = types.InlineKeyboardMarkup(row_width=2)
engine_translation_menu.add(google, microsoft, yandex)
# chose translation action
change_source = types.InlineKeyboardButton(
    text="تغییر زبان مقصد", callback_data="change_lang_source"
)
change_target = types.InlineKeyboardButton(
    text="تغییر زبان مبدا", callback_data="change_lang_target"
)
change_engine = types.InlineKeyboardButton(
    text="تغییر موتور ترجمه", callback_data="change_lang_engine"
)
select_translation_option = types.InlineKeyboardMarkup(row_width=2)
select_translation_option.add(change_source, change_target, change_engine)
