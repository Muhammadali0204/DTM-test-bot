from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.enums.chat_type import ChatType
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter, CommandStart

from . import others
from . import test_ishlash
from app.loader import bot
from app.db.models import User
from app.utils.states import SignUp
from . import javoblarni_tekshirish
from app.data.config import settings
from app.utils.enums import UmumiyButtons
from app.keyboards.reply import reply_keyboards
from app.keyboards.inline import inline_keyboards



router = Router()
router.message(F.chat.type == ChatType.PRIVATE)
router.callback_query(F.message.chat.type == ChatType.PRIVATE)

router_none = Router()
router_none.message(StateFilter(None))
router_none.callback_query(StateFilter(None))


router.include_routers(
    router_none,
    test_ishlash.router,
    others.router,
    javoblarni_tekshirish.router
)



async def show_menu(message : Message):
    await message.answer("📋Menu :", reply_markup=reply_keyboards.menu)

@router_none.message(F.text == UmumiyButtons.ORTGA.value)
@router.message(F.text == "/menu")
async def menu(msg : Message, state : FSMContext):
    await state.clear()
    await show_menu(msg)
    
@router_none.message(CommandStart())
async def start(msg : Message, state : FSMContext):
    if (await User.filter(id=msg.from_user.id).exists()):
        await show_menu(msg)
    else:
        await User.create(id=msg.from_user.id, ism=msg.from_user.first_name)
        await msg.answer(
            text=f'Assalomu alaykum, <b>{msg.from_user.mention_html(msg.from_user.first_name)}</b>'
        )
        await msg.answer(
            "Ismingizni yuboring : "
        )
        await state.set_state(SignUp.ism_yuborish)
        for admin in settings.ADMINS:
            try:
                await bot.send_message(
                    admin,
                    f"<b>➕Yangi foydalanuvchi qo'shildi, {msg.from_user.mention_html(msg.from_user.first_name)}</b>",
                )
            except:
                pass

@router.message(SignUp.ism_yuborish)
async def get_name(msg : Message, state : FSMContext):
    ism = msg.text
    if len(ism) > 2 and len(ism) < 21:
        await state.clear()
        await User.filter(id=msg.from_user.id).update(ism=ism)
        await msg.answer(
            # "Botimizga xush kelibsiz 😊\nUshbu bot sizga yoqadi degan umiddamiz 💌\n\nFoydalanish uchun qo'llanma 👇",
            "Botimizga xush kelibsiz 😊\nUshbu bot sizga yoqadi degan umiddamiz 💌"
            # reply_markup=inline_keyboards.qollanma
        )
        await show_menu(msg)
    else:
        await msg.answer(
            "Belgilar soni [3:20] oralig'ida bo'lishi kerak !\nQayta yuboring :"
        )
        
@router.callback_query(F.data == "yopish")
async def menu(call : CallbackQuery):
    await call.answer("Yopildi ✅")
    await call.message.delete()
