from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from app.utils.enums import AdminMenu, UmumiyButtons



menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=AdminMenu.FILE_ID.value)
        ],
        [
            KeyboardButton(text=AdminMenu.XABAR_YUBORISH.value)
        ],
        [
            KeyboardButton(text=AdminMenu.XABAR_YUBORISHNI_TOXTATISH.value)
        ]
    ],
    resize_keyboard=True
)

ortga = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text=UmumiyButtons.ORTGA.value)
    ]
], resize_keyboard=True)

bekor_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="❌ Bekor qilish")
        ]
    ], resize_keyboard=True
)

