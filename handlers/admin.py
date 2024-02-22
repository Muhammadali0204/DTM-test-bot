import os, signal

from data.config import ADMINS
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State



router = Router()
router.callback_query.filter(F.from_user.id.in_(ADMINS))
router.message.filter(F.from_user.id.in_(ADMINS))

@router.message(F.text=='/shutdown')
async def func(msg : types.Message):
    await msg.answer("<b>Bot o'chdi, xayr... 🥲</b>")
    id = os.getpid()
    os.kill(id, signal.SIGINT)



# @router.message()
# async def func(msg : types.Message):
#     await msg.answer("admin")
    