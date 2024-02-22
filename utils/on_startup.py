from aiogram import Bot, types
from tortoise import Tortoise

from data.config import ADMINS, POSTGRESQL_DB



async def on_startup(bot : Bot):
    await set_commands(bot)
    await startup_notify(bot)
    await init_db()
    
async def startup_notify(bot: Bot):
    for admin in ADMINS:
        try:
            await bot.send_message(
                admin,
                "<b>Bot ishga tushdi</b>"
            )
        except Exception as e:
            pass
        
async def set_commands(bot : Bot):
    await bot.set_my_commands(
        commands=[
            types.BotCommand(command='start', description='Botni ishga tushurish')
        ]
    )
    
async def init_db():
    await Tortoise.init(
        db_url=POSTGRESQL_DB,
        modules={'models':["db.models", "aerich.models"]}
    )
    await Tortoise.generate_schemas(safe=True)