from aiogram import types


default_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text="📂 Список клиентов"),
        ],
        [
            types.KeyboardButton(text="📝 Добавить клиента"),
        ],
        [
            types.KeyboardButton(text="🛠 Изменить клиента"),
        ],
        [
            types.KeyboardButton(text="🗑 Удалить клиента"),
        ]
    ],
    resize_keyboard=True,
)

cancel_keyboard = types.ReplyKeyboardMarkup(
            keyboard=[
                [
                    types.KeyboardButton(text="❌ Отменить действие")
                ]
            ],
            resize_keyboard=True,
        )