from aiogram import Bot, Dispatcher, enums, filters, types
from aiogram.fsm.storage.memory import MemoryStorage
from data.config import ADMINS, BOT_TOKEN

bot = Bot(token=BOT_TOKEN, parse_mode=enums.parse_mode.ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())