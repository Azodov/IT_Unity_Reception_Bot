from aiogram import types
from aiogram.types import ReplyKeyboardRemove

from data.config import CHANNELS
from keyboards.default.courses import courseList
from keyboards.default.language import language
from keyboards.inline.sendAdmin import senderMenu
from keyboards.default.time import timeList
from keyboards.default.fullInfo import familyInfo, socialmedia
from keyboards.default.sendContact import contactUz
from states.langState import langUz
from states.fullInfo import familyUz
from aiogram.dispatcher import FSMContext


from loader import dp, db


@dp.message_handler(text_contains="🇺🇿 O'zbek tili")
async def start_info(message: types.Message, state: FSMContext):
    await state.update_data(
        {"username": message.from_user.username}
    )
    await state.update_data(
        {"user_id": message.from_user.id}
    )
    lang = message.text
    await state.update_data(
        {"lang": lang}
    )

    await message.answer("✒To'liq ismingizni kiriting?", reply_markup=ReplyKeyboardRemove())
    await langUz.fullname.set()


@dp.message_handler(state=langUz.fullname)
async def answer_fullname(message: types.Message, state: FSMContext):
    fullname = message.text

    if len(fullname) < 5 or len(fullname) > 35:
        await message.answer("Iltimos ism va familyangizni to'liq yozing")
    else:
        await state.update_data(
            {"name": fullname}
        )
        await message.reply("Telefon raqamingizni kiriting", reply_markup=contactUz)
        await langUz.phoneNumber.set()


@dp.message_handler(state=langUz.phoneNumber, content_types=['contact', 'text'])
async def answer_number(message: types.Message, state: FSMContext):
    try:
        if message.content_type == 'contact':
            contact = message.contact
            await state.update_data(
                {"phoneNumber": contact.phone_number}
            )
            await message.answer(f"Yoshingizni kiriting", reply_markup=ReplyKeyboardRemove())
            await langUz.age.set()
        else:
            contact = message.text
            if len(contact) == 13 or len(contact) == 12 or len(contact) == 9:
                await state.update_data(
                    {"phoneNumber": contact}
                )
                await message.answer(f"Yoshingizni kiriting", reply_markup=ReplyKeyboardRemove())
                await langUz.age.set()
            else:
                await message.answer("telefon raqam kiritishda xatolik\n"
                                     "quydagi forma ko'rinishida yuboring +998901234567")

    except Exception:
        await message.answer("Qandaydir xatolik yuzaga keldi iltimos /start ni bosing",
                             reply_markup=ReplyKeyboardRemove())
        await state.finish()
        await state.reset_data()


@dp.message_handler(state=langUz.age)
async def answer_faminfo(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
        if age < 10 or age > 70:
            await message.answer("Kechirasiz siz yosh chegarasidan o'tgansiz\n"
                                 "yosh chegarasi 10 yoshdan 70 yoshgacha bo'lishi mumkin\n"
                                 "iltimos qayta urunib ko'ring")
        else:
            await state.update_data(
                {"age": age}
            )
            await message.answer("Oilaviy holatingiz", reply_markup=familyInfo)
            await familyUz.family.set()
    except Exception:
        await message.answer("Iltimos yoshingizni faqat raqamlar bilan kiriting")


@dp.message_handler(state=familyUz.family)
async def answer_familyinfo(message: types.Message, state: FSMContext):
    familyinfo = message.text
    await state.update_data(
        {"familyinfo": familyinfo}
    )
    await message.answer("Kursni tanlang", reply_markup=courseList)
    await familyUz.course.set()


@dp.message_handler(state=familyUz.course)
async def answer_cource(message: types.Message, state: FSMContext):
    course = message.text
    bio = db.course_detail_uz(course)[0]
    await state.update_data(
        {"course": course}
    )

    await message.answer(bio + "\n\nO'zingizga Qulay vaqtni tanlang", reply_markup=timeList)
    await familyUz.time.set()


@dp.message_handler(state=familyUz.time)
async def time_select(message: types.Message, state: FSMContext):
    time = message.text
    await state.update_data(
        {"time": time}
    )
    await message.answer("Biz haqimizda qayerdan bildingiz ?", reply_markup=socialmedia)
    await familyUz.soccialmedia.set()



@dp.message_handler(state=familyUz.soccialmedia)
async def answer_feedback(message: types.Message, state: FSMContext):
    feed = message.text
    await state.update_data(
        {"socialmedia": feed}
    )
    data = await state.get_data()
    name = data.get("name")
    phoneNumber = data.get("phoneNumber")
    course = data.get("course")
    time = data.get("time")
    socialmedia = data.get("socialmedia")
    family_Info = data.get("familyinfo")
    age = data.get("age")
    await message.answer("Ma'lumotlar jo'natish uchun tayyor", reply_markup=ReplyKeyboardRemove())
    await message.answer(f"✒ F.I.SH: {name}\n"
                         f"📞 Tel: {phoneNumber}\n"
                         f"🔶 Yoshim: {age}\n"
                         f"🕔 Qulay vaqtim: {time}\n"
                         f"💬 Oilaviy holatim: {family_Info}\n"
                         f"📚 Tanlagan kursim: {course}\n"
                         f"🌐 Markaz haqida malumotni {socialmedia}dan oldim.\n\n\n"
                         f"📡 Admin: @Developer_6797\n\n", reply_markup=senderMenu)


@dp.callback_query_handler(state=familyUz.soccialmedia, text="send")
async def accept(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    name = data.get("name")
    phoneNumber = data.get("phoneNumber")
    course = data.get("course")
    username = data.get("username")
    time = data.get("time")
    socialmedia = data.get("socialmedia")
    familyInfo = data.get("familyinfo")
    user_id = data.get("user_id")
    age = data.get("age")
    lang = data.get("lang")
    db.add_user(user_id, phoneNumber, username, name, course, lang, age, familyInfo) # bazaga malumotlarni jo'natadi
    msg = str(f"✒ F.I.O: {name}\n"
              f"📞 Tel: {phoneNumber}\n"
              f"🔶 Yoshim: {age}\n"
              f"🕔 Qulay vaqtim: {time}\n"
              f"💬 Oilaviy holatim: {familyInfo}\n"
              f"🗣 Tanlagan tili: {lang}\n"
              f"🔗 Username: {username}\n"
              f"📚 Tanlagan kursim: {course}\n"
              f"🌐 Men markaz haqida {socialmedia}dan habar topdim.\n\n\n"
              f"📡 Admin: @Developer_6797\n\n")

    message = await call.message.answer(msg)
    await message.send_copy(chat_id=CHANNELS[0])
    await call.answer(cache_time=60)
    await call.message.answer(f"Bizni tanlaganingiz uchun tashakkur\n"
                              "siz bilan tez orada bog'lanamiz", reply_markup=ReplyKeyboardRemove())
    await state.finish()
    await state.reset_data()


@dp.callback_query_handler(state=familyUz.soccialmedia, text="cancel")
async def cancel(call: types.CallbackQuery, state: FSMContext):
    message = await call.message.edit_reply_markup()
    await message.delete()
    await call.answer(cache_time=60)
    await state.finish()
    await state.reset_data()
    await call.message.answer('Siz menyuga qaytdingiz', reply_markup=language)
