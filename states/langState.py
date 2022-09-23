from aiogram.dispatcher.filters.state import StatesGroup, State

class langUz(StatesGroup):
    fullname = State()
    phoneNumber = State()
    age = State()

class langRu(StatesGroup):
    fullname = State()
    phoneNumber = State()
    age = State()

class langEng(StatesGroup):
    fullname = State()
    phoneNumber = State()
    age = State()