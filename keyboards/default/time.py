from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

timeList = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="11:00-13:00"),
        ],
        [
            KeyboardButton(text="14:00-16:00"),
        ],
        [
            KeyboardButton(text="16:00-18:00"),
        ],
        [
            KeyboardButton(text="18:00-20:00")
        ],
    ],
    resize_keyboard=True
)
