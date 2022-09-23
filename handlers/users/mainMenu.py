from aiogram import types

from keyboards.default.language import language
from keyboards.default.mainKeyboards import mainMenu


from loader import dp

@dp.message_handler(text_contains="Orqaga")
async def main_menu(message: types.Message):
    await message.answer("Tilni tanlang!", reply_markup=language)