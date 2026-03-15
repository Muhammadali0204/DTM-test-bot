import datetime, pytz
from html import escape

from fastapi import Request
from fastapi.templating import Jinja2Templates

from aiogram.types import Message, CallbackQuery

from app.keyboards.reply import reply_keyboards
from app.db.models import Status, Fan, Natija, Test
from app.utils.enums import TestTuri, UserMenuButtons, KITOBLAR, MAQTOV


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
            elif msg:
                text += f"\n\n<i>{UserMenuButtons.JAVOBLARNI_TEKSHIRISH.value}</i> bo'limi orqali joriy {get_pretty_time(status.finish_time)} gacha testni yakunlang, so'ngra yangi testni boshlay olasiz 🙂"
                await msg.answer(text, reply_markup=reply_keyboards.menu)
            return False
    return True


def get_pretty_timedelta(seconds: int = None):
    if isinstance(seconds, int) and seconds > 0:
        text = ""
        soat = seconds // 3600
        if soat != 0:
            text = f"{soat} soat "
        minutes = seconds - 3600*soat
        if minutes > 0:
            text += f"{minutes//60} daqiqa"
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


def format_result_item(number: int, given: str, correct: str) -> str:
    given = (given or "-").upper()
    correct = (correct or "-").upper()

    base = f"{number:>2}.{given}"
    if given == correct:
        return f"{base} ✅"
    return f"{base} ❌ ({correct})"


async def send_safe(text: str, msg: Message):
    if text.strip():
        await msg.answer(text)


async def check_answer(test: Test, msg: Message, javoblar: str, status: Status):
    global_number = 1
    umumiy_ball = 0.0
    remaining_answers = javoblar

    current_message = "<b>🧑‍🎓 Natijangiz</b>\n"

    for idx, fan in enumerate(test.data):
        fan_nomi = escape(str(fan["fan"]))
        togri_javoblar = fan["javoblar"]
        ball = float(fan["ball"])

        berilgan_javoblar = remaining_answers[:len(togri_javoblar)]
        remaining_answers = remaining_answers[len(togri_javoblar):]

        correct_answers = 0
        lines = []

        for javob_index, togri_javob in enumerate(togri_javoblar):
            berilgan = (
                berilgan_javoblar[javob_index]
                if javob_index < len(berilgan_javoblar)
                else "-"
            )

            if berilgan == togri_javob:
                correct_answers += 1

            lines.append(format_result_item(global_number, berilgan, togri_javob))
            global_number += 1

        fan_ball = round(correct_answers * ball, 1)
        umumiy_ball += fan_ball

        current_part = (
            f"\n{KITOBLAR[idx % 4]} <b>{idx + 1}. {fan_nomi}</b>\n"
            f"<pre>{escape(chr(10).join(lines))}</pre>\n"
            f"✅ To‘g‘ri: <b>{correct_answers}/{len(togri_javoblar)}</b>\n"
            f"💯 Ball: <b>{correct_answers} × {ball:g} = {fan_ball}</b>\n"
        )

        if len(current_message) + len(current_part) > 4096:
            await send_safe(current_message, msg)
            current_message = current_part
        else:
            current_message += current_part

    await send_safe(current_message, msg)

    ratio = umumiy_ball / float(test.umumiy_ball) if float(test.umumiy_ball) else 0

    final_text = f"<b>Umumiy: {round(umumiy_ball, 1)} ball</b>\n\n"
    if ratio <= 0.6:
        final_text += MAQTOV[0]
    elif ratio <= 0.8:
        final_text += MAQTOV[1]
    else:
        final_text += MAQTOV[2]

    await msg.answer(final_text, reply_markup=reply_keyboards.menu)

    try:
        fan = await status.fan
        await Natija.create(
            user_id=msg.from_user.id,
            ball=umumiy_ball,
            test=test,
            fan=fan
        )
    except Exception:
        pass

    await status.delete()
