from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from loader import bot


router = Router()

@router.message()
async def func(msg : types.Message):
    pass