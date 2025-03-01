from aiohttp import web
from aiogram import types
from fastapi import HTTPException, Request

from app.data.config import settings
from app.loader import bot, dp, redis
from app.handlers.user import main as user_main
from app.handlers.admin import main as admin_main
from app.middlewares.ratelimit import ThrottlingMiddlware
from app.utils.startup import shutdown, get_redis, set_webhook, set_command, notify_admins, create_super_user



async def handle_webhook(request: Request):
    url = str(request.url)
    index = url.rfind('/')
    path = url[index:]

    if path == settings.WEBHOOK_PATH and request.headers.get("X-Telegram-Bot-Api-Secret-Token", None) == settings.WEBHOOK_SECRET_TOKEN:
        try :
            update = types.Update(**await request.json())
            await dp.feed_webhook_update(bot, update)
            return web.Response()
        except:
            raise HTTPException(status_code=500, detail="Internal Server Error")
    else:
        raise HTTPException(status_code=403, detail="Forbidden")


async def on_startup():
    global redis
    
    await set_webhook()
    await set_command(bot)
    await notify_admins(bot)
    await create_super_user()
    
    dp.include_routers(
        user_main.router,
        admin_main.router
    )

    redis = await get_redis()
    dp.message.middleware.register(ThrottlingMiddlware(redis, settings.RATE_LIMIT, settings.REDIS_KEY_PREFIX))

async def on_shutdown():
    global redis
    
    await shutdown(redis)
