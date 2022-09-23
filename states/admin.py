from aiogram.dispatcher.filters.state import StatesGroup, State


class admin(StatesGroup):

    ask_course_ru = State()
    ask_course_en = State()
    answer_course_uz = State()
    answer_course_ru = State()
    answer_course_en = State()
    answer_bio_uz = State()
    answer_bio_ru = State()
    answer_bio_en = State()
