import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from tools.logger import setup_logger

from tools.others import get_adm_user
from tools.others import get_token

from handlers import delete_client, add_cleint, client_list, change_client
from handlers.keyboards import default_keyboard
from aiogram.fsm.context import FSMContext


logger = setup_logger()
bot = Bot(token=get_token()[0])
dp = Dispatcher()


dp.include_router(add_cleint.router)
dp.include_router(client_list.router)
dp.include_router(delete_client.router)
dp.include_router(change_client.router)


@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    if message.from_user.id in get_adm_user():
        await state.clear()
        await message.answer("Выберите действие:", reply_markup=default_keyboard.default_keyboard)
    else:
        await message.answer("❌ Тебя нет в админ юзеров. Досвязи!")




async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())