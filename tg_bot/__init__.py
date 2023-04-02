"""This file contains a dictionary with phrases used by the bot"""
from constants import BOT_PHRASES_PATH
from utils import load_from_json
# ----------------------------------------------------------------------

bot_phrases = load_from_json(BOT_PHRASES_PATH)
