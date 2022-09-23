from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup

from keyboards.default.language import language

from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Assalom alaykum, {message.from_user.full_name}\n"
                         f"Tilni tanlang!", reply_markup=language)

    print(message.from_user.full_name)

