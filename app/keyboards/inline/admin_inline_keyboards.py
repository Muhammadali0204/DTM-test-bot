from typing import List
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



def send_message_keyboard(inline_buttons : List):
    keyboard = []
    if inline_buttons:
        for index, inline_button in enumerate(inline_buttons):
            keyboard.append([InlineKeyboardButton(text=inline_button['name'], url=inline_button['url']),InlineKeyboardButton(text='❌', callback_data=f'remove_inline:{index}')])
    keyboard.append([InlineKeyboardButton(text='➕Tugma qo\'shish', callback_data='add_inline')])
    keyboard.append([InlineKeyboardButton(text='❇️Xabar yuborishni boshlash', callback_data='start_send_message')])
    keyboard.append([InlineKeyboardButton(text='❌Bekor qilish', callback_data='cancel_message')])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
    
    return keyboard
