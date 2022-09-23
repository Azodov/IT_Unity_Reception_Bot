from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from data.config import CHANNELS
from keyboards.default.courses import courseListRu
from keyboards.default.fullInfo import familyInfoRu, socialmediaRu
from keyboards.default.language import language
from keyboards.default.sendContact import contactRu
from keyboards.default.time import timeList
from keyboards.inline.sendAdmin import senderMenuRu
from states.langState import langRu
from states.fullInfo import familyRu
from aiogram.dispatcher import FSMContext

from loader import dp, db


@dp.message_handler(text_contains="🇷🇺 Русский язык")
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
    await message.answer("✒Введите свое полное имя?", reply_markup=ReplyKeyboardRemove())
    await langRu.fullname.set()


@dp.message_handler(state=langRu.fullname)
async def answer_fullname(message: types.Message, state: FSMContext):
    fullname = message.text

    if len(fullname) < 5 or len(fullname) > 25:
        await message.answer("Пожалуйста, введите только имя и фамилию")
    else:
        await state.update_data(
            {"name": fullname}
        )
        await message.reply("Введите свой номер телефона", reply_markup=contactRu)
        await langRu.phoneNumber.set()


@dp.message_handler(state=langRu.phoneNumber, content_types=['contact', 'text'])
async def answer_number(message: types.Message, state: FSMContext):
    try:
        if message.content_type == 'contact':
            contact = message.contact
            await state.update_data(
                {"phoneNumber": contact.phone_number}
            )
            await message.answer(f"Введите свой возраст", reply_markup=ReplyKeyboardRemove())
            await langRu.next()
        else:
            contact = str(message.text)
            if len(contact) == 13 or len(contact) == 12 or len(contact) == 9:
                await state.update_data(
                    {"phoneNumber": contact}
                )
                await message.answer(f"Введите свой возраст", reply_markup=ReplyKeyboardRemove())
                await langRu.next()
            else:
                await message.answer("Пожалуйста, введите номер в форму +998901234567")
    except Exception:
        await message.answer(f"Если что-то пошло не так, пожалуйста, нажмите /start ")
        await state.finish()
        await state.reset_data()


@dp.message_handler(state=langRu.age)
async def answer_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
        if age<10 or age>70:
            await message.answer("Извините, вы превысили возрастное ограничение.\n"
                                 "Пожалуйста, введите еще раз")
        else:
            await state.update_data(
                {"age": age}
            )
            await message.answer("Семейное положение", reply_markup=familyInfoRu)
            await familyRu.family.set()
    except:
        await message.answer("Пожалуйста, пишите свой возраст только цифрами")

@dp.message_handler(state=familyRu.family)
async def answer_familyinfo(message: types.Message, state: FSMContext):
    familyinfo = message.text
    await state.update_data(
        {"family_info": familyinfo}
    )
    await message.answer("Выберите курс", reply_markup=courseListRu)
    await familyRu.course.set()


@dp.message_handler(state=familyRu.course)
async def answer_cource(message: types.Message, state: FSMContext):
    course = message.text
    bio = db.course_detail_ru(course)[0]
    await state.update_data(
        {"course": course}
    )
    await message.answer(bio + "\n\nВыберите удобное время для вас", reply_markup=timeList)
    await familyRu.time.set()


@dp.message_handler(state=familyRu.time)
async def time_select(message: types.Message, state: FSMContext):
    time = message.text
    await state.update_data(
        {"time": time}
    )
    await message.answer("Как вы узнали о нас ?", reply_markup=socialmediaRu)
    await familyRu.socialmedia.set()


@dp.message_handler(state=familyRu.socialmedia)
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
    await message.answer("Данные готовы к отправке", reply_markup=ReplyKeyboardRemove())
    await message.answer(f"✒ Имя: {name}\n"
                         f"📞 Тел: {phoneNumber}\n"
                         f"🔶 Возраст: {age}\n"
                         f"🕔 Удобное время: {time}\n"
                         f"💬 Семейное положение: {familyInfo}\n"
                         f"📚 Ваш курс: {course}\n"
                         f"🌐 Я получил информацию о центре от {socialmedia}.\n\n\n"
                         f"📡 Админ: @Developer_6797\n\n", reply_markup=senderMenuRu)


@dp.callback_query_handler(state=familyRu.socialmedia, text="send")
async def accept(call: types.CallbackQuery, state: FSMContext):

    data = await state.get_data()
    name = data.get("name")
    phoneNumber = data.get("phoneNumber")
    course = data.get("course")
    username = data.get("username")
    time = data.get("time")
    socialmedia = data.get("socialmedia")
    familyInfo = data.get("family_info")
    user_id = data.get("user_id")
    age = data.get("age")
    lang = data.get("lang")
    db.add_user(user_id, phoneNumber, username, name, course, lang, age, familyInfo) # bazaga malumotlarni jo'natadi
    msg = str(f"✒ F.I.O: {name}\n"
               f"📞 Tel: {phoneNumber}\n"
               f"🔶 Yoshim: {age}\n"
               f"🕔 Qulay vaqtim: {time}\n"
               f"💬 Oilaviy holatim: {familyInfo}\n"
               f"🗣 Tanlagan tilim: {lang}\n"
               f"📚 Tanlagan kursim: {course}\n"
               f"🌐 Men markaz haqida {socialmedia}dan habar topdim.\n\n\n"
               f"📡 Admin: @Developer_6797\n\n")

    message = await call.message.answer(msg)
    await message.send_copy(chat_id=CHANNELS[0])


    await call.answer(cache_time=60)
    await call.message.answer(f"Спасибо, что выбрали нас\n"
                              "мы свяжемся с вами в ближайшее время", reply_markup=ReplyKeyboardRemove())
    await state.finish()
    await state.reset_data()


@dp.callback_query_handler(state=familyRu.socialmedia, text="cancel")
async def cancel(call: types.CallbackQuery, state: FSMContext):
    message = await call.message.edit_reply_markup()
    await call.answer(cache_time=60)
    await message.delete()
    await state.finish()
    await state.reset_data()
    await call.message.answer('Вы снова в меню', reply_markup=language)
