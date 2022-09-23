from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

familyInfo = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="O'quvchi"),
        ],
        [
            KeyboardButton(text="Student"),
        ],
        [
            KeyboardButton(text="Ishlayman"),
        ],
        [
            KeyboardButton(text="Boshqa")
        ],
    ],
    resize_keyboard=True
)

familyInfoRu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Ученик"),
        ],
        [
            KeyboardButton(text="Студент"),
        ],
        [
            KeyboardButton(text="Я работаю"),
        ],
        [
            KeyboardButton(text="Другой")
        ],
    ],
    resize_keyboard=True
)

familyInfoEng = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Schoolboy"),
        ],
        [
            KeyboardButton(text="Student"),
        ],
        [
            KeyboardButton(text="Employee"),
        ],
        [
            KeyboardButton(text="Other")
        ],
    ],
    resize_keyboard=True
)

socialmedia = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Instagram"),
        ],
        [
            KeyboardButton(text="Telegram"),
        ],
        [
            KeyboardButton(text="Banner"),
        ],
        [
            KeyboardButton(text="Tanishim")
        ],
        [
            KeyboardButton(text="Boshqa")
        ],
    ],
    resize_keyboard=True
)
socialmediaRu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Инстаграма"),
        ],
        [
            KeyboardButton(text="Телеграма"),
        ],
        [
            KeyboardButton(text="Баннерах"),
        ],
        [
            KeyboardButton(text="знакомого")
        ],        [
            KeyboardButton(text="Другой")
        ],
    ],
    resize_keyboard=True
)
socialmediaEng = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Instagram"),
        ],
        [
            KeyboardButton(text="Telegram"),
        ],
        [
            KeyboardButton(text="Banner"),
        ],
        [
            KeyboardButton(text="a friend")
        ],        [
            KeyboardButton(text="Other")
        ],
    ],
    resize_keyboard=True
)

