import datetime, pytz, json

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message, ContentType

from app.data.config import settings
from app.keyboards.reply import reply_keyboards
from app.db.models import User, Status, Natija, Fan, Test
from app.utils.enums import UserMenuButtons, UmumiyButtons
from app.utils.others import get_pretty_time, get_pretty_timedelta, check_answer



router = Router()

router = Router()
router_none = Router()
router_none.message(StateFilter(None))
router_none.callback_query(StateFilter(None))
router.include_router(router_none)



@router_none.message(F.text == UserMenuButtons.JAVOBLARNI_TEKSHIRISH)
async def check_answers(msg : Message):
    user_id = msg.from_user.id
    user = await User.filter(id=user_id).first()
    status = await Status.filter(user__id=user_id).first()
    if status:
        now = datetime.datetime.now(pytz.timezone('Asia/Tashkent'))
        if status.finish_time < now:
            text = f"Joriy testga o'z vaqtida javob yubormadingiz 😓({get_pretty_time(status.finish_time)} gacha edi)\n\n"\
                "Ushbu test uchun ball : 0"
            await msg.answer(text)
            try:
                await Natija.create(
                    user_id = user_id,
                    ball = 0,
                    test = status.test,
                    fan = status.fan
                )
            except :
                pass
            await status.delete()
        else:
            test: Test = await status.test
            if len(test.fanlar) > 1:
                fanlar_nomlari = "📚Fanlar :\n"
                fanlar_nomlari += "\n".join(f"{i+1}. {fan_nomi}" for i, fan_nomi in enumerate(test.fanlar))
            else:
                fanlar_nomlari = f"📘 Fan nomi : {test.fanlar[0]}"
            text = f"{fanlar_nomlari}\n\n<i>{test.tarif}</i>\n\n"

            text += f"⏱️Test uchun berilgan vaqt : {get_pretty_timedelta(seconds=test.duration)}\n\n"
            now = datetime.datetime.now(pytz.timezone('Asia/Tashkent'))
            text += f"🕑Test boshlangan vaqt : {get_pretty_time(now)}\n"\
                f"🕓Test tugash vaqti : {get_pretty_time(now + datetime.timedelta(seconds=test.duration))}\n\n"\
                    f"Test javoblarini yuborish uchun quyidagi <i>{UmumiyButtons.JAVOB_YUBORISHNI_BOSHLASH.value}</i> tugmasini bosing va javoblaringizni kiriting 📬"
            
            await msg.answer(
                text=text,
                reply_markup=reply_keyboards.javob_yuborish(
                    f"https://{settings.WEBHOOK_HOST}/answer?test_id={test.id}"
                )
            )
    elif user is None:
        await User.create(
            id=msg.from_user.id,
            ism=msg.from_user.first_name
        )
        await msg.answer(
            "Hozirda sizda hech qanday faol test mavjud emas 🙁"
        )
    else:
        await msg.answer(
            "Hozirda sizda hech qanday faol test mavjud emas 🙁"
        )
        
@router_none.message(F.content_type == ContentType.WEB_APP_DATA)
async def web_app_data(msg : Message):
    web_app_data = msg.web_app_data
    if web_app_data.button_text == UmumiyButtons.JAVOB_YUBORISHNI_BOSHLASH.value:
        data: dict = json.loads(web_app_data.data)
        if data:
            test_id = data.get('test_id', None)
            javoblar = data.get('javoblar', None)
            if test_id and javoblar:
                status = await Status.filter(user__id = msg.from_user.id).first()
                if status:
                    now = datetime.datetime.now(pytz.timezone('Asia/Tashkent'))
                    if status.finish_time < now:
                        if msg:
                            text = f"Joriy testga o'z vaqtida javob yubormadingiz 😓({get_pretty_time(status.finish_time)} gacha edi)\n\n"\
                                "Ushbu test uchun ball : 0"
                            await msg.answer(text, reply_markup=reply_keyboards.menu)
                        try:
                            fan = await status.fan
                            await Natija.create(
                                user_id = msg.from_user.id,
                                ball = 0,
                                test_id = test_id,
                                fan = fan
                            )
                        except Exception as e:
                            print(e)
                        await status.delete()
                    else:
                        test = await Test.filter(id=test_id).first()
                        if test.savollar_soni == len(javoblar):
                            await check_answer(test, msg, javoblar, status)
                        else:
                            await msg.answer("Javoblar soni savollar soni bilan bir xil emas ❌")
                else:
                    await msg.answer("Siz hozirda hech qanday test ishlamayapsiz ☹️")
            
            return
        await msg.answer("Ma'lumotlar mavjud emas !", reply_markup=reply_keyboards.menu)

