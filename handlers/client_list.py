from math import ceil
from contextlib import suppress

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.exceptions import TelegramBadRequest

from tools.others import get_adm_user
from db_func import dbmanager
from handlers.keyboards.default_keyboard import default_keyboard, cancel_keyboard


router = Router()

current_page = {}
all_pages = {}
clients = {}

@router.message(F.text.lower() == "❌ отменить действие")
async def cansel_user(message: types.Message, state: FSMContext):
    if message.from_user.id in get_adm_user():
        await state.clear()
        await message.reply("Отмена", reply_markup=default_keyboard)
        

class InputPage(StatesGroup):
    search = State()


def get_keyboard(from_user):
    buttons = [
        [
            types.InlineKeyboardButton(text="Назад", callback_data="num_decr"),
            types.InlineKeyboardButton(text=f"{current_page[from_user]}/{all_pages[from_user]}", callback_data="num_search"),
            types.InlineKeyboardButton(text="Дальше", callback_data="num_incr")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def display_pages(page_number, data):
    start_index = (page_number - 1) * 10
    end_index = start_index + 10

    page_data = data[start_index:end_index]

    text = f"📂 Всего в базе клиентов: {dbmanager.get_count_clients()}"

    for item in page_data:
        text += f'''
    
id: {item["id"]}
😮‍💨 Имя: {item["Имя"]}
😮‍💨 Фамилия: {item["Фамилия"]}
📞 Номер: {item["Номер"]}
🌃 Город: {item["Город"]}
🎂 ДР: {item["ДР"]}
🔗 Профиль: {item["Профиль"]}
👟 Модель: {item["Модель"]}
📏 Размер: {item["Размер"]}
💰 Сумма покупки: {item["Сумма покупки"]}
'''

    return text


@router.message(F.text.lower() == "📂 список клиентов")
async def get_list_clients(message: types.Message, state: FSMContext):
    if message.from_user.id in get_adm_user():
        await state.clear()
        current_page[message.from_user.id] = 1
        all_pages[message.from_user.id] = ceil(dbmanager.get_count_clients() / 10)
        clients[message.from_user.id] = dbmanager.get_list_clients()
        

        await message.reply(display_pages(1, clients[message.from_user.id]), disable_web_page_preview=True, reply_markup=get_keyboard(message.from_user.id))



@router.callback_query(F.data.startswith("num_"), StateFilter(None))
async def callback_num(callback: types.CallbackQuery, state: FSMContext):
    with suppress(TelegramBadRequest):
        action = callback.data.split("_")[1]
        
        if action == "incr":
            if current_page[callback.from_user.id] < all_pages[callback.from_user.id]:
                current_page[callback.from_user.id] += 1
                await callback.message.edit_text(display_pages(current_page[callback.from_user.id], clients[callback.from_user.id]), reply_markup=(get_keyboard(callback.from_user.id)), disable_web_page_preview=True)
        elif action == "decr":
            if current_page[callback.from_user.id] > 1:
                current_page[callback.from_user.id] -= 1
                await callback.message.edit_text(display_pages(current_page[callback.from_user.id], clients[callback.from_user.id]), reply_markup=(get_keyboard(callback.from_user.id)), disable_web_page_preview=True)
        elif action == "search":
            await callback.message.answer(f"Введите номер страницы от 1 до {all_pages[callback.from_user.id]}", reply_markup=cancel_keyboard)
            await callback.message.delete()
            await state.set_state(InputPage.search)



@router.message(InputPage.search, F.text)
async def search(message: types.Message, state: FSMContext):
    try:
        message_int = int(message.text)
        current_page[message.from_user.id] = message_int
        if message_int > 0 and message_int <= all_pages[message.from_user.id]:
            await message.answer(display_pages(current_page[message.from_user.id], clients[message.from_user.id]), reply_markup=(get_keyboard(message.from_user.id)), disable_web_page_preview=True)
            await message.answer('.', reply_markup=default_keyboard)
            await message.delete()
            await state.clear()
        else:
            await message.reply(f"❌ Число не должно быть меньше 1 и больше {all_pages[message.from_user.id]}", reply_markup=cancel_keyboard)
    except:
        await message.reply("❌ Введите число, а не текст!", reply_markup=cancel_keyboard)