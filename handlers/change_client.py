import re
from contextlib import suppress
from datetime import datetime

import pyshorteners
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter
from aiogram.exceptions import TelegramBadRequest

from handlers.keyboards.default_keyboard import default_keyboard, cancel_keyboard
from tools.others import get_adm_user
from db_func import dbmanager


router = Router()

client_id = {}

@router.message(F.text.lower() == "❌ отменить действие")
async def cansel_user(message: types.Message, state: FSMContext):
    if message.from_user.id in get_adm_user():
        await state.clear()
        await message.reply("Отмена", reply_markup=default_keyboard)


class InputUserId(StatesGroup):
    input_id = State()
    input_first_name = State()
    input_last_name = State()
    input_phone = State()
    input_city = State()
    input_birthday = State()
    input_avito_profile = State()
    input_shoe_model = State()
    input_shoe_size = State()
    input_purchase_amount = State()


act = ["click_first_name", "click_last_name", "click_number", "click_city", "click_birthday", "click_profile", "click_shoe_model", "click_shoe_size", "click_amount"]


from aiogram import types

def get_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text=f"😮‍💨 Имя", callback_data="click_first_name")
        ],
        [
            types.InlineKeyboardButton(text=f"😮‍💨 Фамилию", callback_data=act[1])
        ],
        [
            types.InlineKeyboardButton(text=f"📞 Номер", callback_data=act[2])
        ],
        [
            types.InlineKeyboardButton(text=f"🌃 Город", callback_data=act[3])
        ],
        [
            types.InlineKeyboardButton(text=f"🎂 ДР", callback_data=act[4])
        ],
        [
            types.InlineKeyboardButton(text=f"🔗 Профиль", callback_data=act[5])
        ],
        [
            types.InlineKeyboardButton(text=f"👟 Модель обуви", callback_data=act[6])
        ],
        [
            types.InlineKeyboardButton(text=f"📏 Размер обуви", callback_data=act[7])
        ],
        [
            types.InlineKeyboardButton(text=f"💰 Сумму покупки", callback_data=act[8])
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard



@router.message(StateFilter(None), F.text.lower() == "🛠 изменить клиента")
async def changeUser(message: types.Message, state: FSMContext):
    if message.from_user.id in get_adm_user():
        await state.clear()
        await message.reply("Отправьте id клиента:", reply_markup=cancel_keyboard)
        await state.set_state(InputUserId.input_id)


@router.message(StateFilter(InputUserId.input_id), F.text)
async def InputId(message: types.message):
    try:
        message_id = int(message.text)
        client_id[message.from_user.id] = message_id
        if dbmanager.find_user(message_id):
            await message.reply(f"Что вы хотите изменить у клиента {message_id}?", reply_markup=get_keyboard())
        else:
            await message.reply(f"❌ Такого клиента не существует")
    except:
        await message.reply("❌ Введите число, а не текст!")
    

@router.callback_query(F.data.startswith("click_"))
async def callback_num(callback: types.CallbackQuery, state: FSMContext):
    with suppress(TelegramBadRequest):
        action = callback.data
        
        if action == act[0]:
            await callback.message.answer("Отправьте новое имя клиента:", reply_markup=cancel_keyboard)
            await state.set_state(InputUserId.input_first_name)
        elif action == act[1]:
            await callback.message.answer("Отправьте новую фамилию клиента:", reply_markup=cancel_keyboard)
            await state.set_state(InputUserId.input_last_name)
        elif action == act[2]:
            await callback.message.answer("Отправьте новый телефон клиента:", reply_markup=cancel_keyboard)
            await state.set_state(InputUserId.input_phone)
        elif action == act[3]:
            await callback.message.answer("Отправьте новый город клиента:", reply_markup=cancel_keyboard)
            await state.set_state(InputUserId.input_city)
        elif action == act[4]:
            await callback.message.answer("Отправьте новую дату рождения клиента YYYY.MM.DD:", reply_markup=cancel_keyboard)
            await state.set_state(InputUserId.input_birthday)
        elif action == act[5]:
            await callback.message.answer("Отправьте новый Авито-профиль клиента:", reply_markup=cancel_keyboard)
            await state.set_state(InputUserId.input_avito_profile)
        elif action == act[6]:
            await callback.message.answer("Отправьте новое название обуви клиента:", reply_markup=cancel_keyboard)
            await state.set_state(InputUserId.input_shoe_model)
        elif action == act[7]:
            await callback.message.answer("Отправьте новый размер клиента в см:", reply_markup=cancel_keyboard)
            await state.set_state(InputUserId.input_shoe_size)
        elif action == act[8]:
            await callback.message.answer("Отправьте новую сумму покупки клиента:", reply_markup=cancel_keyboard)
            await state.set_state(InputUserId.input_purchase_amount)



@router.message(InputUserId.input_first_name, F.text)
async def first_name(message: types.Message, state: FSMContext):
    if (re.search(r'^[a-zA-Zа-яА-Я\s]+$', message.text) and ' ' not in message.text) or message.text.lower() == "none":
        if message.text.lower() != "none":
            dbmanager.update_client_data(client_id[message.from_user.id], "first_name", message.text)
        else:
            dbmanager.update_client_data(client_id[message.from_user.id], "first_name", None)
        await state.clear()
        await message.answer(f"✅ Успешно изменил имя клиента", reply_markup=default_keyboard)
    else:
        await message.reply("🛑 Пожалуйста, используйте только буквы в имени. Специальные символы, пробелы и цифры не допускаются.")


@router.message(InputUserId.input_last_name, F.text)
async def last_name(message: types.Message, state: FSMContext):
    if (re.search(r'^[a-zA-Zа-яА-Я\s]+$', message.text) and ' ' not in message.text) or message.text.lower() == "none":
        if message.text.lower() != "none":
            dbmanager.update_client_data(client_id[message.from_user.id], "last_name", message.text)
        else:
            dbmanager.update_client_data(client_id[message.from_user.id], "last_name", None)
        await state.clear()
        await message.answer(f"✅ Успешно изменил фамилию клиента", reply_markup=default_keyboard)
    else:
        await message.reply("🛑 Пожалуйста, используйте только буквы в имени. Специальные символы, пробелы и цифры не допускаются.")


@router.message(InputUserId.input_phone, F.text)
async def input_phone(message: types.Message, state: FSMContext):
    if re.search(r'^\+\d{1,15}$', message.text) or message.text.lower() == "none":
        if message.text.lower() != "none":
            dbmanager.update_client_data(client_id[message.from_user.id], "phone", message.text)
        else:
            dbmanager.update_client_data(client_id[message.from_user.id], "phone", None)
        await state.clear()
        await message.answer(f"✅ Успешно изменил номер клиента", reply_markup=default_keyboard)
    else:
        await message.reply("🛑 Пожалуйста, введите номер телефона в формате +79997778899.")


@router.message(InputUserId.input_city, F.text)
async def input_city(message: types.Message, state: FSMContext):
    if (re.search(r'^[a-zA-Zа-яА-Я\s]+$', message.text) and ' ' not in message.text) or message.text.lower() == "none":
        if message.text.lower() != "none":
            dbmanager.update_client_data(client_id[message.from_user.id], "city", message.text)
        else:
            dbmanager.update_client_data(client_id[message.from_user.id], "city", None)
        await state.clear()
        await message.answer(f"✅ Успешно изменил город клиента", reply_markup=default_keyboard)
    else:
        await message.reply("🛑 Пожалуйста, используйте только буквы в названии Города. Специальные символы, пробелы и цифры не допускаются.")


@router.message(InputUserId.input_birthday, F.text)
async def input_birthday(message: types.Message, state: FSMContext):
    try:
        date_obj = datetime.strptime(message.text, '%Y.%m.%d')
        if date_obj < datetime.now():
            dbmanager.update_client_data(client_id[message.from_user.id], "birthday", str(date_obj.strftime('%Y-%m-%d')))
            await state.clear()
            await message.answer(f"✅ Успешно изменил дату рождения клиента", reply_markup=default_keyboard)
        else:
            await message.reply("🛑 Дата рождения не может быть в будущем")
    except:
        if message.text.lower() != "none":
            await message.reply("🛑 Некорректный формат даты. Используйте формат YYYY.MM.DD")
        else:
            dbmanager.update_client_data(client_id[message.from_user.id], "birthday", None)
            await state.clear()
            await message.answer(f"✅ Успешно изменил дату рождения клиента", reply_markup=default_keyboard)


@router.message(InputUserId.input_avito_profile, F.text)
async def input_avito_profile(message: types.Message, state: FSMContext):
    status = False
    if message.text.lower() != "none":
        try:
            short_url = pyshorteners.Shortener().tinyurl.short(message.text)
            dbmanager.update_client_data(client_id[message.from_user.id], "avito_profile", short_url)
            status = True
        except:
            await message.reply("🛑 Отправьте настоящую ссылку")
    else:
        dbmanager.update_client_data(client_id[message.from_user.id], "avito_profile", None)
        status = True
        
    if status:
        await state.clear()
        await message.answer(f"✅ Успешно изменил ссылку на профиль клиента", reply_markup=default_keyboard)


@router.message(InputUserId.input_shoe_model, F.text)
async def input_shoe_model(message: types.Message, state: FSMContext):
    if message.text.lower() != "none":
        dbmanager.update_client_data(client_id[message.from_user.id], "shoe_model", message.text)
    else:
        dbmanager.update_client_data(client_id[message.from_user.id], "shoe_model", None)
    await state.clear()
    await message.reply(f"✅ Успешно изменил модель обуви клиента", reply_markup=default_keyboard)


@router.message(InputUserId.input_shoe_size, F.text)
async def input_shoe_size(message: types.Message, state: FSMContext):
    if re.search(r'^\d+(\.\d)?$', message.text) or message.text.lower() == "none":
        if message.text.lower() != "none":
            dbmanager.update_client_data(client_id[message.from_user.id], "shoe_size", float(message.text))
        else:
            dbmanager.update_client_data(client_id[message.from_user.id], "shoe_size", None)
        await state.clear()
        await message.reply(f"✅ Успешно изменил размер обуви клиента", reply_markup=default_keyboard)
    else:
        await message.reply("🛑 Введите корректный формат данных пример 27.5")


@router.message(InputUserId.input_purchase_amount, F.text)
async def input_purchase_amount(message: types.Message, state: FSMContext):
    if re.search(r'^\d+(\.\d+)?$', message.text) or message.text.lower() == "none":
        if message.text.lower() != "none":
            dbmanager.update_client_data(client_id[message.from_user.id], "purchase_amount", float(message.text))
        else:
            dbmanager.update_client_data(client_id[message.from_user.id], "purchase_amount", None)
        
        await state.clear()
        await message.answer(f"✅ Успешно изменил сумму покупки клиента", reply_markup=default_keyboard)
    else:
        await message.reply("🛑 Введите корректный формат данных пример 24999.99")