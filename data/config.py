from environs import Env
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = [int(x) for x in env.list("ADMINS")]
POSTGRESQL_DB = env.str("POSTGRESQL_DB")

TORTOISE_ORM = {
    "connections": {"default": POSTGRESQL_DB},
    "apps": {
        "models": {
            "models": ["db.models", "aerich.models"],
            "default_connection": "default",
        },
    }
}