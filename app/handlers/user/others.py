from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from app.data.config import settings
from app.utils.states import Sozlamalar
from app.db.models import User, Natija, Test
from app.keyboards.reply import reply_keyboards
from app.keyboards.inline import inline_keyboards
from app.utils.enums import UserMenuButtons, UmumiyButtons



router = Router()

router_none = Router()
router_none.message.filter(StateFilter(None))
router_none.callback_query.filter(StateFilter(None))
router.include_router(router_none)



# @router_none.message(F.text == UserMenuButtons.QOLLANMA)
# async def get_qollanma(msg : Message):
#     await msg.answer(
#         "📝 Qo'llanma ishlab chiqish jarayonida ... "
#     )

@router_none.message(F.text == UserMenuButtons.DOST_TAKLIF)
async def invite_friend(msg : Message):
    answer = f"Quyidagi tugmani bosing va do'stlaringizni tanlang 😊"
    await msg.answer(answer, reply_markup=inline_keyboards.dustlar(
        "Ushbu bot orqali bir necha fanlardan testlar ishlashingiz mumkin.\nUshbu botni men sizga taklif qilaman 😊"
    ))

@router_none.message(F.text == UserMenuButtons.SOZLAMALAR)
async def settingss(msg : Message, state : FSMContext):
    await msg.answer(
        f"{UserMenuButtons.SOZLAMALAR.value} :",
        reply_markup=reply_keyboards.sozlamalar
    )
    await state.set_state(Sozlamalar.sozlamalar)

@router.message(
    F.text == UmumiyButtons.ORTGA.value,
    StateFilter(Sozlamalar)
)
async def ortga(msg : Message, state : FSMContext):
    await msg.answer("📋Menu :", reply_markup=reply_keyboards.menu)
    await state.clear()
    
@router.message(F.text == UmumiyButtons.ISMNI_TAHRIRLASH.value)
async def edit_name(msg : Message, state : FSMContext):
    user = await User.filter(id = msg.from_user.id).first()
    if not user:
        user = await User.create(id=msg.from_user.id, ism=msg.from_user.first_name)
    ism = user.ism if user else msg.from_user.first_name
    await msg.answer(
        f"Hozirda ismingiz : <b>{ism}</b>\n\nYangi ism yuboring : (Belgilar soni : [3:20])",
        reply_markup=reply_keyboards.ortga
    )
    await state.set_state(Sozlamalar.get_new_name)
    
@router.message(Sozlamalar.get_new_name)
async def get_new_name(msg : Message, state : FSMContext):
    ism = msg.text
    if len(ism) > 2 and len(ism) < 21:
        await state.clear()
        await User.filter(id=msg.from_user.id).update(ism=ism)
        await msg.answer(
            f"Ismingiz <b>{ism}</b>'ga muvaffaqiyatli o'zgartirildi ✅"
        )
        await ortga(msg, state)
    else:
        await msg.answer(
            "Belgilar soni [3:20] oralig'ida bo'lishi kerak !\nQayta yuboring :",
            reply_markup=reply_keyboards.ortga
        )
    

@router_none.message(F.text == UserMenuButtons.UMUMIY_STATISTIKA)
async def get_stats(msg : Message):
    users_count = await User.all().count()
    tests_count = await Test.all().count()
    results_count = await Natija.all().count()
    
    answer = f"👤Botning foydalanuvchilari soni : <i>{users_count}</i> ta\n"
    answer += f"📂Botda mavjud testlar soni : <i>{tests_count}</i> ta\n"
    answer += f"📝Foydalanuvchilar ishlagan testlar soni : <i>{results_count}</i> ta\n\n"
    answer += f"👨‍💻Admin : @{settings.BOT_ADMIN_USERNAME}"

    await msg.answer(answer)
