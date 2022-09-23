from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

mainMenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Orqaga")
        ],
    ],
    resize_keyboard=True
)