from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

contactUz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Telefon raqamni jo'natish.",
                           request_contact=True)
        ],
    ],
    resize_keyboard=True
)
contactRu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отправить номер телефона.",
                           request_contact=True)
        ],
    ],
    resize_keyboard=True
)
contactEng = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Send my contact",
                           request_contact=True)
        ],
    ],
    resize_keyboard=True
)