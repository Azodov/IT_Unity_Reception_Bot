from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

senderMenu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅Tasdiqlash", callback_data="send"),
            InlineKeyboardButton(text="❌Bekor qilish", callback_data="cancel"),
        ],
    ])
senderMenuRu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅Подтвердить", callback_data="send"),
            InlineKeyboardButton(text="❌Отмена", callback_data="cancel"),
        ],
    ])

senderMenuEng = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅Approve", callback_data="send"),
            InlineKeyboardButton(text="❌Cancel", callback_data="cancel"),
        ],
    ])

