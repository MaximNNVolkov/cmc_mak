import app_logger as log
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from os import getenv
from sys import exit
from utils.startup import set_default


# переменные
Token = getenv("TOKEN_CMC_MAK")
if not Token:
    exit("Error: no token provided")
bot = Bot(token=Token)
dp = Dispatcher(bot, storage=MemoryStorage())
logger = log.get_logger(__name__)


if __name__ == "__main__":
    logger.info('bot started')
    executor.start_polling(dispatcher=dp,
                           skip_updates=False,
                           on_startup=set_default)
