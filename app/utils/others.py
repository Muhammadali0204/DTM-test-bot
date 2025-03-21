import datetime, pytz

from fastapi import Request
from fastapi.templating import Jinja2Templates

from aiogram.types import Message, CallbackQuery

from app.keyboards.reply import reply_keyboards
from app.db.models import Status, Fan, Natija, Test
from app.utils.enums import TestTuri, UserMenuButtons, KITOBLAR, STICKERS, MAQTOV



async def check_status(msg: Message = None, call: CallbackQuery = None):
    user_id = call.from_user.id if call else msg.from_user.id
    status = await Status.filter(user__id=user_id).first()
    if status:
        now = datetime.datetime.now(pytz.timezone('Asia/Tashkent'))
        if status.finish_time < now:
            if msg:
                text = f"Joriy testga o'z vaqtida javob yubormadingiz 😓({get_pretty_time(status.finish_time)} gacha edi)\n\n"\
                    "Ushbu test uchun ball : 0"
                await msg.answer(text)
            elif call:
                text = f"Joriy testga o'z vaqtida javob yubormadingiz 😓({get_pretty_time(status.finish_time)} gacha edi). "\
                    "Ushbu test uchun ball : 0"
                await call.answer(text)
            
            try:
                test = await status.test
                fan = await status.fan
                await Natija.create(
                    user_id = user_id,
                    ball = 0,
                    test = test,
                    fan = fan
                )
            except:
                pass
            await status.delete()
        else:
            fan: Fan = await status.fan
            if fan.tur == TestTuri.ASOSIY:
                text = f"🤷‍♂️ Siz hozirda {fan.nom} fanidan test ishlamoqdasiz !"
            elif fan.tur == TestTuri.BLOK:
                text = f"🤷‍♂️ Siz hozirda {fan.nom} fanlar yo'nalishidan test ishlamoqdasiz !"

            if call:
                await call.answer(text, True)
                await call.message.delete()
            elif msg:
                text += f"\n\n<i>{UserMenuButtons.JAVOBLARNI_TEKSHIRISH.value}</i> bo'limi orqali joriy {get_pretty_time(status.finish_time)} gacha testni yakunlang, so'ngra yangi testni boshlay olasiz 🙂"
                await msg.answer(text, reply_markup=reply_keyboards.menu)
            return False
    return True

def get_pretty_timedelta(seconds: int = None):
    if isinstance(seconds, int) and seconds > 0:
        soat = seconds // 3600
        if soat != 0:
            text = f"{soat} soat "
        seconds = seconds - 3600*soat
        if seconds > 0:
            text += f"{seconds} daqiqa"
        return text
    else:
        raise ValueError("Sekundlar musbat bo'lishi kerak !")
    
def get_pretty_time(time: datetime.datetime):
    return time.strftime("%H:%M %d.%m.%Y")

async def send_answer_page(
    templates: Jinja2Templates, test_id: int, request: Request,
    
):
    test = await Test.filter(id=test_id).first()
    if test:
        data = test.data
        return templates.TemplateResponse(
            request,
            'get_answer.html',
            {'data': data, "test_id": test_id},
            status_code=200
        )
    else:
        return templates.TemplateResponse(
            request,
            'error.html',
            {'message': "Bunday test topilmadi ❌"},
            status_code=404
        )
        
async def check_answer(test: Test, msg: Message, javoblar: str, status: Status):
    answer = "🧑‍🎓Natijangiz :\n\n"
    i = 1
    umumiy_ball = 0
    for idx, fan in enumerate(test.data):
        current_answer = ""
        correct_answers = 0
        ball = fan['ball']
        current_answer += f"{KITOBLAR[idx % 4]} {idx+1}. <b>{fan['fan']}</b> :\n"
        togri_javoblar = fan['javoblar']
        berilgan_javoblar = javoblar[:len(togri_javoblar)]
        javoblar = javoblar[len(togri_javoblar):]
        for javob_index, togri_javob in enumerate(togri_javoblar):
            if togri_javob == berilgan_javoblar[javob_index]:
                sticker = STICKERS[1]
                correct_answers += 1
            else:
                sticker = f"{STICKERS[0]} ({togri_javob.upper()})"
            current_answer += f"{i}. {berilgan_javoblar[javob_index].upper()} {sticker}  "
            i += 1
            if javob_index % 5 == 4:
                current_answer += "\n"
        current_answer += f"\nBall: {correct_answers} ta * {ball} = {round(correct_answers*ball, 1)} ball\n\n"
        umumiy_ball += round(correct_answers*ball, 1)
        if len(answer + current_answer) > 4096:
            await msg.answer(answer)
            answer = ""
        else:
            answer += current_answer
    await msg.answer(answer)
    
    answer = f"<b>Umumiy ball : {round(umumiy_ball, 1)} ball</b>\n\n"
    if umumiy_ball / float(test.umumiy_ball) <= 0.6:
        answer += MAQTOV[0]
    elif umumiy_ball / float(test.umumiy_ball) <= 0.8:
        answer += MAQTOV[1]
    else:
        answer += MAQTOV[2]
    await msg.answer(answer, reply_markup=reply_keyboards.menu)
    
    try:
        fan = await status.fan
        await Natija.create(
            user_id = msg.from_user.id,
            ball = umumiy_ball,
            test = test,
            fan = fan
        )
    except:
        pass
    
    await status.delete()
