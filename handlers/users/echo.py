from aiogram import types

from loader import dp


# Echo bot
@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    await message.answer("Kechirasiz siz kiritgan buyruqni bizning bot bajara olmaydi.\n"
                         "pastdagi menyudan birini tanlang")
