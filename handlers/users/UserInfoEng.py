from aiogram import types
from aiogram.types import ReplyKeyboardRemove

from data.config import CHANNELS
from keyboards.default.courses import courseListEn
from keyboards.default.fullInfo import familyInfoEng, socialmediaEng
from keyboards.default.language import language
from keyboards.default.sendContact import contactEng
from keyboards.default.time import timeList
from keyboards.inline.sendAdmin import senderMenuEng
from states.langState import langEng
from states.fullInfo import familyEng
from aiogram.dispatcher import FSMContext

from loader import dp, db


@dp.message_handler(text_contains="🇺🇸 English")
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
    await message.answer("✒Enter your full name?", reply_markup=ReplyKeyboardRemove())
    await langEng.fullname.set()


@dp.message_handler(state=langEng.fullname)
async def answer_fullname(message: types.Message, state: FSMContext):
    fullname = message.text

    if len(fullname)<5 or len(fullname)>25:
        await message.answer("Please write your full name")
    else:
        await state.update_data(
            {"name": fullname}
        )
        await message.reply("Enter your phone number", reply_markup=contactEng)
        await langEng.next()


@dp.message_handler(state=langEng.phoneNumber, content_types=['contact', 'text'])
async def answer_number(message: types.Message, state: FSMContext):
    try:
        if message.content_type == 'contact':
            contact = message.contact
            await state.update_data(
                {"phoneNumber": contact.phone_number}
            )
            await message.answer(f"Enter your age", reply_markup=ReplyKeyboardRemove())
            await langEng.next()
        else:
            contact = message.text
            if len(contact) == 13 or len(contact) == 12 or len(contact) == 8:
                await state.update_data(
                    {"phoneNumber": contact}
                )
                await message.answer(f"Enter your age",reply_markup=ReplyKeyboardRemove())
                await langEng.next()
            else:
                await message.answer("Please enter the number in the form +998901234567")
    except:
        await message.answer("If something went wrong, please press /start", reply_markup=ReplyKeyboardRemove())
        await state.finish()
        await state.reset_data()


@dp.message_handler(state=langEng.age)
async def answer_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
        if age<10 or age>70:
            await message.answer("Sorry you crossed the age limit\n"
                                 "the age limit can range from 10 to 70 years\n"
                                 "please try again")
        else:
            await state.update_data(
                {"age": age}
            )
            await message.answer("Marital status", reply_markup=familyInfoEng)
            await familyEng.family.set()
    except Exception:
        await message.answer("Please enter your age in numbers only")


@dp.message_handler(state=familyEng.family)
async def answer_familyinfo(message: types.Message, state: FSMContext):
    familyinfo = message.text
    await state.update_data(
        {"family_info": familyinfo}
    )
    await message.answer("Select a course", reply_markup=courseListEn)
    await familyEng.course.set()


@dp.message_handler(state=familyEng.course)
async def answer_cource(message: types.Message, state: FSMContext):
    course = message.text
    bio = db.course_detail_en(course)[0]
    await state.update_data(
        {"course": course}
    )
    await message.answer(bio + "\n\nChoose a convenient time for you", reply_markup=timeList)
    await familyEng.time.set()


@dp.message_handler(state=familyEng.time)
async def time_select(message: types.Message, state: FSMContext):
    time = message.text
    await state.update_data(
        {"time": time}
    )
    await message.answer("How did you hear about us ?", reply_markup=socialmediaEng)
    await familyEng.socialmedia.set()


@dp.message_handler(state=familyEng.socialmedia)
async def answer_feddback(message: types.Message, state: FSMContext):
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
    familyInfo = data.get("family_info")
    age = data.get("age")
    await message.answer("Data is ready to send", reply_markup=ReplyKeyboardRemove())
    await message.answer(f"✒ Full Name: {name}\n"
                         f"📞 Phone: {phoneNumber}\n"
                         f"🔶 Age: {age}\n"
                         f"🕔 Convenient time: {time}\n"
                         f"💬 Marital status: {familyInfo}\n"
                         f"📚 Selected course: {course}\n"
                         f"🌐 I received information about the center {socialmedia}.\n\n\n"
                         f"📡 Owner: @Developer_6797\n\n", reply_markup=senderMenuEng)


@dp.callback_query_handler(state=familyEng.socialmedia, text="send")
async def accept(call: types.CallbackQuery, state: FSMContext):

    data = await state.get_data()
    user_id = data.get("user_id")
    username = data.get("username")
    name = data.get("name")
    phoneNumber = data.get("phoneNumber")
    course = data.get("course")
    time = data.get("time")
    socialmedia = data.get("socialmedia")
    familyInfo = data.get("family_info")
    age = data.get("age")
    lang = data.get("lang")
    db.add_user(user_id, phoneNumber, username, name, course, lang, age, familyInfo) # bazaga malumotlarni jo'natadi

    msg = str(f"✒ F.I.O: {name}\n"
                  f"📞 Tel: {phoneNumber}\n"
                  f"🔶 Yoshi: {age}\n"
                  f"🕔 Qulay vaqti: {time}\n"
                  f"💬 Oilaviy holati: {familyInfo}\n"
                  f"🗣 Tanlagan tili: {lang}\n"
                  f"🔗 USername: @{username}\n"
                  f"📚 Tanlagan kursi: {course}\n"
                  f"🌐 Men markaz haqida {socialmedia}dan habar topdi.\n\n\n"
                  f"📡 Admin: @Developer_6797\n\n")

    message = await call.message.answer(msg)
    await message.send_copy(chat_id=CHANNELS[0])
    await call.answer(cache_time=60)
    await call.message.answer(f"Thanks for choosing us\n"
                              "We will contact you shortly", reply_markup=ReplyKeyboardRemove())
    await state.finish()
    await state.reset_data()


@dp.callback_query_handler(state=familyEng.socialmedia, text="cancel")
async def cancel(call: types.CallbackQuery, state: FSMContext):
    message = await call.message.edit_reply_markup()
    await message.delete()
    await call.answer(cache_time=60)
    await state.finish()
    await state.reset_data()
    await call.message.answer('You are back on the menu', reply_markup=language)