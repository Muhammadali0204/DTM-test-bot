import pytz, datetime

from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from tortoise.expressions import Subquery, Case, When, Q

from app.loader import bot
from app.data.config import settings
from app.keyboards.reply import reply_keyboards
from app.utils.states import TestIshlash
from app.keyboards.inline import inline_keyboards
from app.db.models import User, Fan, Test, Natija, Status
from app.utils.others import check_status, get_pretty_timedelta, get_pretty_time
from app.utils.enums import TestTuri, TestTuriButtons, UmumiyButtons, UserMenuButtons


router = Router()
router_none = Router()
router_none.message(StateFilter(None))
router_none.callback_query(StateFilter(None))
router.include_router(router_none)



async def show_menu(message : Message):
    await message.answer("📋Menu :", reply_markup=reply_keyboards.menu) 

@router_none.message(F.text == UserMenuButtons.TEST_ISHLASH)
async def test_ishlash(msg : Message, state : FSMContext):
    status = await check_status(msg=msg)
    if status:
        await msg.answer(
            "Qanday turdagi test ishlamoqchisiz ❓",
            reply_markup=reply_keyboards.test_turi(),
        )
        await state.set_state(TestIshlash.test_turi)
    
    user = await User.filter(id=msg.from_user.id).first()
    if user is None:
        await User.create(msg.from_user.id, msg.from_user.first_name)
    
@router.message(TestIshlash.test_turi)
async def test_tur(msg : Message, state : FSMContext):
    status = await check_status(msg=msg)
    if status:
        text = msg.text
        if text in TestTuriButtons or text == UmumiyButtons.ORTGA:
            await state.clear()
            await show_menu(msg)
            if text == TestTuriButtons.MAJBURIY_FANLAR.value:
                testlar = await Test.filter(fan=None).exists()
                if testlar:
                    await send_tests_msg(msg)
                else:
                    await msg.answer(
                        "Hozirda majburiy fanlar bo'yicha testlar mavjud emas ❌"
                    )

            elif text == TestTuriButtons.BLOK_TEST.value:
                fanlar = await Fan.filter(tur=TestTuri.BLOK).all()
                if fanlar != []:
                    await msg.answer(
                        "Quyidagi yo'nalishlardan birini tanlang :",
                        reply_markup=inline_keyboards.fanlar_list(fanlar)
                    )
                else:
                    await msg.answer("Hozirda blok testlar mavjud emas ❌")

            elif text == TestTuriButtons.ASOSIY_FANLAR.value:
                fanlar = await Fan.filter(tur = TestTuri.ASOSIY).all()
                if fanlar != []:
                    await msg.answer(
                        "Quyidagi fanlardan birini tanlang :",
                        reply_markup=inline_keyboards.fanlar_list(fanlar)
                    )
                else:
                    await msg.answer("Hozirda asosiy fanlar uchun testlar mavjud emas ❌")
        else:
            await msg.answer(
                "Iltimos, quyidagi tugmalardan foydalaning 👇",
                reply_markup=reply_keyboards.test_turi()
            )
    else:
        await state.clear()
        
@router_none.callback_query(F.data.startswith('fanlarga:'))
async def to_subjects(call : CallbackQuery):
    tur = call.data.split(':')[1]
    if tur == TestTuri.BLOK:
        fanlar = await Fan.filter(tur=TestTuri.BLOK).all()
        await call.message.edit_text(
            "Quyidagi yo'nalishlardan birini tanlang :",
            reply_markup=inline_keyboards.fanlar_list(fanlar)
        )

    elif tur == TestTuri.ASOSIY:
        fanlar = await Fan.filter(tur = TestTuri.ASOSIY).all()
        await call.message.edit_text(
            "Quyidagi fanlardan birini tanlang :",
            reply_markup=inline_keyboards.fanlar_list(fanlar)
        )
        
@router_none.callback_query(F.data.startswith('fan:'))
async def send_tests(call : CallbackQuery):
    status = await check_status(call=call)
    if status:
        fan_id = call.data.split(':')[1]
        fan = await Fan.filter(id=fan_id).first()
        if fan:
            subquery = Natija.filter(
                fan_id=fan_id,
                user_id = call.from_user.id
            ).values('test_id')
            
            testlar = await Test.annotate(
                status=Case(
                    When(Q(id__in=Subquery(subquery)), then='1'),
                    default='0'
                )
            ).filter(fan=fan).all()
            
            if testlar == []:
                if fan.tur == TestTuri.BLOK:
                    text = "Hozirda ushbu yo'nalish bo'yicha testlar mavjud emas ❌"
                elif fan.tur == TestTuri.ASOSIY:
                    text = "Hozirda ushbu fan bo'yicha testlar mavjud emas ❌"
                await call.answer(
                    text, True
                )
                
                return
            
            await call.message.edit_text(
                text="Quyidagi testlardan birini tanlang :",
                reply_markup=inline_keyboards.testlar_list(testlar, fan.tur.value)
            )
        else:
            await call.answer("Ushbu fan topilmadi !", True)
            await call.message.delete()
            await call.message.answer("📋Menu :", reply_markup=reply_keyboards.menu)
            
async def send_tests_msg(msg : Message):
    status = await check_status(msg=msg)
    if status:
        subquery = Natija.filter(
            fan_id=None,
            user_id = msg.from_user.id
        ).values('test_id')
        
        testlar = await Test.annotate(
            status=Case(
                When(Q(id__in=Subquery(subquery)), then='1'),
                default='0'
            )
        ).filter(fan=None).all()
        
        await msg.answer(
            text="Quyidagi testlardan birini tanlang :",
            reply_markup=inline_keyboards.testlar_list(testlar, None)
        )

        
@router_none.callback_query(F.data.startswith('test:'))
async def send_test_description(call : CallbackQuery):
    status = await check_status(call=call)
    if status:
        test_id = call.data.split(':')[1]
        test = await Test.filter(id=test_id).first()
        
        if len(test.fanlar) > 1:
            fanlar_nomlari = "📚Fanlar :\n"
            fanlar_nomlari += "\n".join(f"{i+1}. {fan_nomi}" for i, fan_nomi in enumerate(test.fanlar))
        else:
            fanlar_nomlari = f"📘 Fan nomi : {test.fanlar[0]}"
        text = f"{fanlar_nomlari}\n\n<i>{test.tarif}</i>\n\n"
        
        natija = await Natija.filter(test=test, user__id=call.from_user.id).first()
        if natija:
            text += f"\n\nUshbu testni ishlagansiz ❗️\nNatijangiz : {natija.ball} ball ({round(natija.ball/test.umumiy_ball*100, 1)}%)\n\n"
        
        text += "Ushbu testni boshlash uchun <code>🟢Testni boshlash</code> tugmasini bosing❗️"
        
        await call.message.edit_text(
            text=text,
            reply_markup=inline_keyboards.boshlash(test_id)
        )
    
@router_none.callback_query(F.data.startswith('start_test:'))
async def send_test(call : CallbackQuery):
    status = await check_status(call=call)
    if status:
        test_id = call.data.split(':')[1]
        test = await Test.filter(id=test_id).first()
        caption = f"⏱️Test uchun berilgan vaqt : {get_pretty_timedelta(seconds=test.duration)}\n\n"
        now = datetime.datetime.now(pytz.timezone('Asia/Tashkent'))
        caption += f"🕑Test boshlanish vaqti : {get_pretty_time(now)}\n"\
            f"🕓Test tugash vaqti : {get_pretty_time(now + datetime.timedelta(seconds=test.duration))}\n\n"\
                f"👨‍🏫Test muallifi : {test.owner}"
        
        await call.answer("Test boshlandi 🙋‍♂️", True)
        await call.message.delete()
        msg = await call.message.answer_document(
            test.file,
            caption=caption,
            reply_markup=reply_keyboards.menu
        )
        await bot.pin_chat_message(msg.chat.id, msg.message_id, disable_notification=True)
        await Status.create(
            user_id = call.from_user.id,
            test = test,
            fan = (await test.fan),
            finish_time = now + datetime.timedelta(seconds=test.duration)
        )
