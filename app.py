import asyncio
from utils.on_startup import on_startup
from loader import dp, bot
from data.config import ADMINS
from handlers import admin, user

async def main():    
    dp.include_routers(admin.router,user.router)
    await on_startup(bot)
    print("Bot ishga tushdi")
    await dp.start_polling(bot)
    
    

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e :
        print(f"ERROR : {e}")
