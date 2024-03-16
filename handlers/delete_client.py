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

class DeleteClientCl(StatesGroup):
    input_user = State()


@router.message(StateFilter(None), F.text.lower() == "🗑 удалить клиента")
async def delete_client(message: types.Message, state: FSMContext):
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
        await message.reply("Отправьте id клиента:", reply_markup=keyboard)
        await state.set_state(DeleteClientCl.input_user)


@router.message(StateFilter(DeleteClientCl.input_user), F.text)
async def DeleteClient(message: types.Message, state: FSMContext):
    try:
        message_int = int(message.text)
        
        result = dbmanager.delete_client(message_int)
        if result == 1:
            await state.clear()
            await message.reply(f"✅ Успешно удалил клиента с id: {message_int}", reply_markup=default_keyboard)
        else:
            await state.clear()
            await message.answer("❌ Такого клиента нет", reply_markup=default_keyboard)
    except:
        await message.reply("❌ Введите число!")