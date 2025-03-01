import asyncio

from typing import List

from aiogram import Bot
from aiogram.types import Message
from aiogram.types import InputMediaAnimation, InputMediaAudio, InputMediaDocument, InputMediaPhoto, InputMediaVideo

from app.data.config import settings
from app.utils.enums import MessageType
from app.keyboards.inline import inline_keyboards, admin_inline_keyboards



async def send_message_to_users(
    stop_event : asyncio.Event,
    bot : Bot,
    users : List[int],
    admin : int,
    msg : Message = None,
    msgs : List[Message] = None,
    inline_buttons : List = None,
    is_admin : bool = False
):
    n = 0
    
    if msg:
        
        if is_admin:
            keyboard = admin_inline_keyboards.send_message_keyboard(inline_buttons)
        else:
            keyboard = inline_keyboards.send_message_keyboard(inline_buttons)
        
        for idx, user in enumerate(users):
            if not stop_event.is_set():
                try :
                    if msg.content_type == MessageType.TEXT:
                        await bot.send_message(
                            user,
                            text=msg.html_text,
                            reply_markup=keyboard
                        )
                    elif msg.content_type == MessageType.PHOTO:
                        await bot.send_photo(
                            user,
                            photo=msg.photo[-1].file_id,
                            caption=msg.html_text,
                            reply_markup=keyboard
                        )
                    elif msg.content_type == MessageType.DOCUMENT:
                        await bot.send_document(
                            user,
                            document=msg.document.file_id,
                            caption=msg.html_text,
                            reply_markup=keyboard
                        )
                    elif msg.content_type == MessageType.VIDEO:
                        await bot.send_video(
                            user,
                            video=msg.video.file_id,
                            caption=msg.html_text,
                            reply_markup=keyboard
                        )
                    elif msg.content_type == MessageType.ANIMATION:
                        await bot.send_animation(
                            user,
                            animation=msg.animation.file_id,
                            caption=msg.html_text,
                            reply_markup=keyboard
                        )
                    elif msg.content_type == MessageType.AUDIO:
                        await bot.send_audio(
                            user,
                            audio=msg.audio.file_id,
                            caption=msg.html_text,
                            reply_markup=keyboard
                        )
                    elif msg.content_type == MessageType.STICKER:
                        await bot.send_sticker(
                            user,
                            sticker=msg.sticker.file_id,
                            reply_markup=keyboard
                        )
                    elif msg.content_type == MessageType.LOCATION:
                        await bot.send_location(
                            user,
                            latitude=msg.location.latitude,
                            longitude=msg.location.longitude,
                            reply_markup=keyboard
                        )
                    n += 1
                    await asyncio.sleep(0.04)
                except :
                    pass
                if (idx + 1) % 100 == 0:
                    await oraliq_xabar(
                        idx, n, bot, admin
                    )
            else:
                await stop_sending(idx, n, bot, admin)
                return
        if not is_admin:
            await end_sending(
                idx, n, bot, admin
            )
    elif msgs:
        
        input_messages = []
        
        for msg in msgs:
            if msg.content_type == MessageType.VIDEO:
                input_messages.append(
                    InputMediaVideo(
                        media=msg.video.file_id,
                        caption=msg.html_text
                    )
                )
            elif msg.content_type == MessageType.PHOTO:
                input_messages.append(
                    InputMediaPhoto(
                        media=msg.photo[-1].file_id,
                        caption=msg.html_text
                    )
                )
            elif msg.content_type == MessageType.DOCUMENT:
                input_messages.append(
                    InputMediaDocument(
                        media=msg.document.file_id,
                        caption=msg.html_text
                    )
                )
            elif msg.content_type == MessageType.ANIMATION:
                input_messages.append(
                    InputMediaAnimation(
                        media=msg.animation.file_id,
                        caption=msg.html_text
                    )
                )
            elif msg.content_type == MessageType.AUDIO:
                input_messages.append(
                    InputMediaAudio(
                        media=msg.audio.file_id,
                        caption=msg.html_text
                    )
                )
            
        for idx, user in enumerate(users):
            if not stop_event.is_set():
                try :
                    await bot.send_media_group(
                        user,
                        media=input_messages
                    )
                    i += 1
                    await asyncio.sleep(0.04)
                except :
                    pass
                if (idx + 1) % 100 == 0:
                    await oraliq_xabar(
                        idx, n, bot, admin
                    )
            else:
                await stop_sending(idx, n, bot, admin)
                return
        if not is_admin:
            await end_sending(idx, n, bot, admin)

async def stop_sending(idx, n, bot : Bot, admin):
    try :
        await bot.send_message(
            admin,
            f"<b>Xabar yuborish to'xtatildi !\n\nYetib kelingan edi : {idx+1}\nYuborildi : {n} ✅\nYuborilmadi : {idx - n} ❌</b>"
        )
    except :
        pass
    
async def end_sending(idx, n, bot : Bot, admin):
    try :
        await bot.send_message(
            admin,
            f"<b>Xabar yuborish tugadi !\n\nJami : {idx+1}\nYuborildi : {n} ✅\nYuborilmadi : {idx - n + 1} ❌</b>"
        )
    except :
        pass
    
async def oraliq_xabar(idx, n, bot : Bot, admin):
    try :
        await bot.send_message(
            admin,
            f"<b>Xabar yuborilmoqda !\n\nYetib kelindi : {idx+1}\nYuborildi : {n} ✅\nYuborilmadi : {idx - n + 1} ❌</b>"
        )
    except :
        pass
