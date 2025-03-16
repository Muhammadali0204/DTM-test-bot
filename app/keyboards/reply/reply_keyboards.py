from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

from app.utils.enums import TestTuriButtons, UserMenuButtons, UmumiyButtons


menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=UserMenuButtons.TEST_ISHLASH.value)
        ],
        [
            KeyboardButton(text=UserMenuButtons.JAVOBLARNI_TEKSHIRISH.value)
        ],
        [
            KeyboardButton(text=UserMenuButtons.SOZLAMALAR.value),
            KeyboardButton(text=UserMenuButtons.DOST_TAKLIF.value),
        ],
        [
            # KeyboardButton(text=UserMenuButtons.QOLLANMA.value),
            KeyboardButton(text=UserMenuButtons.UMUMIY_STATISTIKA.value),
        ],
    ],
    resize_keyboard=True,
)

def test_turi():
    keyboard = ReplyKeyboardBuilder()
    
    for button in TestTuriButtons:
        keyboard.add(
            KeyboardButton(text=button.value)
        )
    keyboard.button(text=UmumiyButtons.ORTGA.value)
    keyboard.adjust(2)
    
    return keyboard.as_markup(resize_keyboard=True)

sozlamalar = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=UmumiyButtons.ISMNI_TAHRIRLASH.value), KeyboardButton(text=UmumiyButtons.ORTGA.value)]
    ],
    resize_keyboard=True,
)

ortga = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text=UmumiyButtons.ORTGA.value)
    ]
], resize_keyboard=True)

def javob_yuborish(url: str):
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=UmumiyButtons.JAVOB_YUBORISHNI_BOSHLASH.value, web_app=WebAppInfo(url=url))
            ],
            [
                KeyboardButton(text=UmumiyButtons.ORTGA.value)
            ]
        ], resize_keyboard=True
    )
