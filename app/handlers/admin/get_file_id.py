from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ContentType

from app.utils.enums import AdminMenu
from app.utils.states import AdminStates
from app.keyboards.reply import admin_reply_keys



router = Router()

    
@router.message(F.text == AdminMenu.FILE_ID)
async def get_file(msg : Message, state : FSMContext):
    await msg.answer(
        "<b>Fayl yuboring :</b>",
        reply_markup=admin_reply_keys.ortga
    )
    await state.set_state(AdminStates.get_file)
    
@router.message(F.content_type == ContentType.DOCUMENT)
async def send_file_id(msg : Message, state : FSMContext):
    if msg.document:
        await msg.answer(
            f"<code>{msg.document.file_id}</code>"
        )
    await msg.answer(
        '<b>Admin panel :</b>',
        reply_markup=admin_reply_keys.menu
    )
    await state.clear()
