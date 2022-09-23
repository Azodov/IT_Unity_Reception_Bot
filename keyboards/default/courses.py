from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import dp, db, bot

courses = db.get_courses()
keyboard_uz = []
keyboard_ru = []
keyboard_en = []
for course in courses:
    keyboard_uz.append([KeyboardButton(text=course[1])])
    keyboard_ru.append([KeyboardButton(text=course[2])])
    keyboard_en.append([KeyboardButton(text=course[3])])

courseList = ReplyKeyboardMarkup(
    keyboard=keyboard_uz,
    resize_keyboard=True
)

courseListRu = ReplyKeyboardMarkup(
    keyboard=keyboard_ru,
    resize_keyboard=True
)

courseListEn = ReplyKeyboardMarkup(
    keyboard=keyboard_en,
    resize_keyboard=True
)
