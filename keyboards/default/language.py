from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

language = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🇺🇿 O'zbek tili")
        ],
        [
            KeyboardButton(text="🇷🇺 Русский язык"),
            KeyboardButton(text="🇺🇸 English")
        ],
    ],
    resize_keyboard=True
)