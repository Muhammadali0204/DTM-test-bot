from typing import List
from itertools import zip_longest

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.db.models import Fan, Test
from app.data.config import settings
from app.utils.enums import UmumiyButtons



def fanlar_list(fanlar):
    keyboard = []
    
    for fan1, fan2 in zip_longest(fanlar[::2], fanlar[1::2], fillvalue=None):
        fan1: Fan
        fan2: Fan
        temp = [InlineKeyboardButton(text=fan1.nom, callback_data=f"fan:{fan1.id}"),]
        if fan2 is not None:
            temp.append(InlineKeyboardButton(text=fan2.nom, callback_data=f"fan:{fan2.id}"))
            
        keyboard.append(temp)
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def testlar_list(testlar, tur):
    keyboard = []
    i = 1
    for test1, test2 in zip_longest(testlar[::2], testlar[1::2], fillvalue=None):
        temp = [get_button(i, test1)]
        if test2 is not None:
            temp.append(get_button(i+1, test2))
        i += 2
        keyboard.append(temp)
    if tur is not None:
        keyboard.append([InlineKeyboardButton(text=UmumiyButtons.ORTGA.value, callback_data=f'fanlarga:{tur}')])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_button(i: int, test: Test):
    if test.status == '1':
        text = f"{i}-test ✔️"
    else:
        text = f"{i}-test"
    return InlineKeyboardButton(text=text, callback_data=f"test:{test.id}")


qollanma = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=UmumiyButtons.QOLLANMANI_OCHISH.value, url=settings.QOLLANMA_LINK)
        ]
    ]
)

def boshlash(test_id):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=UmumiyButtons.TESTNI_BOSHLASH.value,
                    callback_data=f"start_test:{test_id}",
                )
            ],
            [
                InlineKeyboardButton(text=UmumiyButtons.YOPISH.value, callback_data='yopish')
            ]
        ]
    )

    return keyboard


def dustlar(text : str):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=UmumiyButtons.YUBORISH.value,
                    switch_inline_query=text,
                )
            ]
        ]
    )
    
    return keyboard

def send_message_keyboard(inline_buttons : List):
    keyboard = []
    if inline_buttons:
        for inline_button in inline_buttons:
            keyboard.append([InlineKeyboardButton(text=inline_button['name'], url=inline_button['url'])])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
    
    return keyboard
