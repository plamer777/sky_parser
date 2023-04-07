from os import environ
from telebot.async_telebot import AsyncTeleBot
from constants import RESULT_PATH
from managers.data_manager import DataManager
from managers.tg_bot_manager import TelebotManager
# ------------------------------------------------------------------------

chat_ids = set()

bot = AsyncTeleBot(environ.get('BOT_TOKEN'))
telebot_manager = TelebotManager(bot)
data_manager = DataManager(RESULT_PATH)
