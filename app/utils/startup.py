import bcrypt

from colorama import Fore
from tortoise import Tortoise
from aiogram import Bot, types
from redis.asyncio import Redis

from app.loader import bot
from app.db.models import Admin
from app.data.config import settings



async def set_webhook():
    await bot.set_webhook(settings.WEBHOOK_URI, drop_pending_updates=True, secret_token=settings.WEBHOOK_SECRET_TOKEN)

async def set_command(bot : Bot):
    await bot.set_my_commands(
        commands=[
            types.BotCommand(command='start', description='Botni ishga tushurish'),
            types.BotCommand(command='menu', description='Bosh menu')
        ]
    )

async def get_redis():
    return await Redis.from_url(settings.REDIS_URL)
    
async def notify_admins(bot : Bot):
    print(Fore.LIGHTBLUE_EX + "Bot ishga tushdi !") 
    for admin in settings.ADMINS:
        try :
            await bot.send_message(admin, "<b>Bot ishga tushdi</b>")
        except :
            pass

async def create_super_user():
    if not (await Admin.filter(username = 'admin').exists()):
        await Admin.create(
            username='admin',
            hash_password=bcrypt.hashpw(settings.ADMIN_PASSWORD.encode(), salt=bcrypt.gensalt()).decode(),
            is_superuser=True,
            is_active=True
        )
    
async def shutdown(redis : Redis):
    await redis.aclose()
    for admin in settings.ADMINS:
        try :
            await bot.send_message(admin, "<b>Bot o'chdi !</b>")
        except :
            pass
    print(Fore.LIGHTRED_EX + "Bot o'chdi !" + Fore.RESET)
