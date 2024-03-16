import re
from datetime import datetime
import pyshorteners

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import StatesGroup, State

from handlers.keyboards.default_keyboard import default_keyboard
from tools.others import get_adm_user
from db_func import dbmanager


router = Router()


@router.message(F.text.lower() == "❌ отменить действие")
async def cansel_user(message: types.Message, state: FSMContext):
    if message.from_user.id in get_adm_user():
        await state.clear()
        await message.reply("Отмена", reply_markup=default_keyboard)


class AddClient(StatesGroup):
    input_first_name = State()
    input_last_name = State()
    input_phone = State()
    input_city = State()
    input_birthday = State()
    input_avito_profile = State()
    input_shoe_model = State()
    input_shoe_size = State()
    input_purchase_amount = State()


@router.message(StateFilter(None), F.text.lower() == "📝 добавить клиента")
async def add_client(message: types.Message, state: FSMContext):
    if message.from_user.id in get_adm_user():
        await state.clear()
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=[
                [
                    types.KeyboardButton(text="❌ Отменить действие")
                ]
            ],
            resize_keyboard=True,
        )
        await message.reply("😮‍💨 Отправьте имя клиента:", reply_markup=keyboard)
        await state.set_state(AddClient.input_first_name)


@router.message(AddClient.input_first_name, F.text)
async def first_name(message: types.Message, state: FSMContext):
    if (re.search(r'^[a-zA-Zа-яА-Я\s]+$', message.text) and ' ' not in message.text) or message.text.lower() == "none":
        if message.text.lower() != "none":
            await state.update_data(first_name=message.text)
        else:
            await state.update_data(first_name=None)
        await message.reply("😮‍💨 Отправьте фамилию клиента:")
        await state.set_state(AddClient.input_last_name)
    else:
        await message.reply("🛑 Пожалуйста, используйте только буквы в имени. Специальные символы, пробелы и цифры не допускаются.")


@router.message(AddClient.input_last_name, F.text)
async def last_name(message: types.Message, state: FSMContext):
    if (re.search(r'^[a-zA-Zа-яА-Я\s]+$', message.text) and ' ' not in message.text) or message.text.lower() == "none":
        if message.text.lower() != "none":
            await state.update_data(last_name=message.text)
        else:
            await state.update_data(last_name=None)
        await message.reply("📞 Отправьте номер телефона клиента в формате +79997778899:")
        await state.set_state(AddClient.input_phone)
    else:
        await message.reply("🛑 Пожалуйста, используйте только буквы в имени. Специальные символы, пробелы и цифры не допускаются.")


@router.message(AddClient.input_phone, F.text)
async def input_phone(message: types.Message, state: FSMContext):
    if re.search(r'^\+\d{1,15}$', message.text) or message.text.lower() == "none":
        if message.text.lower() != "none":
            await state.update_data(phone=message.text)
        else:
            await state.update_data(phone=None)
        await message.reply("🌃 Отправьте город клиента:")
        await state.set_state(AddClient.input_city)
    else:
        await message.reply("🛑 Пожалуйста, введите номер телефона в формате +79997778899.")


@router.message(AddClient.input_city, F.text)
async def input_city(message: types.Message, state: FSMContext):
    if (re.search(r'^[a-zA-Zа-яА-Я\s]+$', message.text) and ' ' not in message.text) or message.text.lower() == "none":
        if message.text.lower() != "none":
            await state.update_data(city=message.text)
        else:
            await state.update_data(city=None)
        await message.reply("🎂 Отправьте дату рождения клиента в формате YYYY.MM.DD:")
        await state.set_state(AddClient.input_birthday)
    else:
        await message.reply("🛑 Пожалуйста, используйте только буквы в названии Города. Специальные символы, пробелы и цифры не допускаются.")


@router.message(AddClient.input_birthday, F.text)
async def input_birthday(message: types.Message, state: FSMContext):
    try:
        date_obj = datetime.strptime(message.text, '%Y.%m.%d')
        if date_obj < datetime.now():
            await state.update_data(birthday=str(date_obj.strftime('%Y-%m-%d')))
            await message.reply("🔗 Отправьте авито профиль клиента: ")
            await state.set_state(AddClient.input_avito_profile)
        else:
            await message.reply("🛑 Дата рождения не может быть в будущем")
    except:
        if message.text.lower() != "none":
            await message.reply("🛑 Некорректный формат даты. Используйте формат YYYY.MM.DD")
        else:
            await state.update_data(birthday=None)
            await message.reply("🔗 Отправьте авито профиль клиента: ")
            await state.set_state(AddClient.input_avito_profile)


@router.message(AddClient.input_avito_profile, F.text)
async def input_avito_profile(message: types.Message, state: FSMContext):
    status = False
    if message.text.lower() != "none":
        try:
            short_url = pyshorteners.Shortener().tinyurl.short(message.text)
            await state.update_data(avito_profile=short_url)
            status = True
        except:
            await message.reply("🛑 Отправьте настоящую ссылку")
    else:
        await state.update_data(avito_profile=None)
        status = True
        
    if status:
        await message.reply(f"👟 Отправьте модель обуви клиента:")
        await state.set_state(AddClient.input_shoe_model)


@router.message(AddClient.input_shoe_model, F.text)
async def input_shoe_model(message: types.Message, state: FSMContext):
    if message.text.lower() != "none":
        await state.update_data(shoe_model=message.text)
    else:
        await state.update_data(shoe_model=None)
    await message.reply(f"📏 Отправьте размер обуви клиента в см:")
    await state.set_state(AddClient.input_shoe_size)


@router.message(AddClient.input_shoe_size, F.text)
async def input_shoe_size(message: types.Message, state: FSMContext):
    if re.search(r'^\d+(\.\d)?$', message.text) or message.text.lower() == "none":
        if message.text.lower() != "none":
            await state.update_data(shoe_size=float(message.text))
        else:
            await state.update_data(shoe_size=None)
        await message.reply("💰 Отправьте сумму покупки клиента:")
        await state.set_state(AddClient.input_purchase_amount)
    else:
        await message.reply("🛑 Введите корректный формат данных пример 27.5")


@router.message(AddClient.input_purchase_amount, F.text)
async def input_purchase_amount(message: types.Message, state: FSMContext):
    if re.search(r'^\d+(\.\d+)?$', message.text) or message.text.lower() == "none":
        if message.text.lower() != "none":
            await state.update_data(purchase_amount=float(message.text))
        else:
            await state.update_data(purchase_amount=None)

        user_data = await state.get_data()
        dbmanager.add_client(user_data['first_name'], user_data['last_name'],
            user_data['phone'], user_data['city'], user_data['birthday'], user_data['avito_profile'], user_data['shoe_model'], user_data['shoe_size'], user_data['purchase_amount'])
        
        await state.clear()
        await message.answer("✅ Успешно внес в базу данных", reply_markup=default_keyboard)
    else:
        await message.reply("🛑 Введите корректный формат данных пример 24999.99")