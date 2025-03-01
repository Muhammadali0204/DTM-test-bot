from pathlib import Path
from decouple import Config, Csv



config = Config('.env')


class Settings():
    ADMINS = config('ADMINS', cast=Csv(int))
    
    BOT_TOKEN = config("BOT_TOKEN", cast=str)
    
    BOT_USERNAME = config("BOT_USERNAME", cast=str)
    
    DB_URL = config("DB_URL", cast=str)
    
    REDIS_URL = config("REDIS_URL", cast=str)
    
    RATE_LIMIT = config('RATE_LIMIT', cast=int)
    
    QOLLANMA_LINK = config('QOLLANMA_LINK', cast=str)
    
    WEBHOOK_HOST = config("WEBHOOK_HOST", cast=str)
    
    WEBHOOK_PATH = config('WEBHOOK_PATH', cast=str)
    
    WEBHOOK_SECRET_TOKEN = config('WEBHOOK_SECRET_TOKEN', cast=str)
    
    WEBHOOK_URI = WEBHOOK_HOST + WEBHOOK_PATH
    
    BOT_ADMIN_USERNAME = config('BOT_ADMIN_USERNAME', cast=str)
    
    REDIS_KEY_PREFIX = config('REDIS_KEY_PREFIX', cast=str)
    
    ADMIN_PASSWORD : str = config('ADMIN_PASSWORD', cast=str)

    BASE_DIR = Path(__file__).resolve().parent.parent
    
    PHOTO_PATH = BASE_DIR / 'static' / 'media' / 'photos'
    

settings = Settings()

DATABASE_CONFIG = {
    "connections": {"default": settings.DB_URL},
    "apps": {
        "models":{
            "models": ["app.db.models", "aerich.models"],
            "default_connection": "default",
        },
    },
    "use_tz": True,
    "timezone": "Asia/Tashkent"
}

