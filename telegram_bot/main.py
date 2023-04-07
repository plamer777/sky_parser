import os
from asyncio import run, create_task, gather, sleep
from constants import CHAT_IDS_PATH, RESULT_PATH, CHECK_UPDATES_DELAY_10M
from container import bot, chat_ids, telebot_manager, data_manager
from tg_bot import main_handlers
from utils import load_from_json
# -------------------------------------------------------------------------

bot.register_message_handler(main_handlers.start_handler)
bot.register_message_handler(main_handlers.menu_handler)
bot.register_message_handler(main_handlers.all_prices_handler)
bot.register_message_handler(main_handlers.choose_school_handler)
bot.register_message_handler(main_handlers.common_profs_handler)
bot.register_message_handler(main_handlers.price_by_school_prof_handler)
bot.register_message_handler(main_handlers.prices_notice_handler)

chat_ids.update(set(load_from_json(CHAT_IDS_PATH)))


async def main():
    current_changed_time = None
    while True:
        if os.path.exists(RESULT_PATH):
            file_changed_time = os.path.getmtime(RESULT_PATH)
            if file_changed_time != current_changed_time:
                await telebot_manager.send_messages(chat_ids)
                data_manager.refresh_data()
                current_changed_time = file_changed_time
        await sleep(CHECK_UPDATES_DELAY_10M)


async def event_loop() -> None:
    """This function serves as an event loop to allow parser and telegram
    bot work together"""
    parse_task = create_task(main())
    tg_bot_task = create_task(bot.infinity_polling())
    await gather(parse_task, tg_bot_task)


if __name__ == '__main__':
    run(event_loop())
