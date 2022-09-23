from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


adminMenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Yangi kurs qo'shish"),
        ],
        [
            KeyboardButton(text="Admin Menudan chiqish"),
        ]
    ],
    resize_keyboard=True
)