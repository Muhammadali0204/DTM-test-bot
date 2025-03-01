from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ContentType

from . import get_file_id
from . import send_messages
from app.utils.states import AdminStates
from app.utils.enums import UmumiyButtons
from app.keyboards.reply import admin_reply_keys



router = Router()

router_none = Router()
router_none.message(StateFilter(None))
router_none.callback_query(StateFilter(None))

router.include_routers(
    router_none,
    get_file_id.router,
    send_messages.router
)


@router.message(
    F.text == UmumiyButtons.ORTGA,
    StateFilter(
        AdminStates.get_file
    )
)
async def ortgaa(msg : Message, state : FSMContext):
    await admin_panel(msg)
    await state.clear()


@router_none.message(F.text.lower() == 'admin')
async def admin_panel(msg : Message):
    await msg.answer(
        '<b>Admin panel :</b>',
        reply_markup=admin_reply_keys.menu
    )
