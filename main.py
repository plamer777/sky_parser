"""This is a main file to start the parser"""
from asyncio import sleep, run, create_task, gather
from datetime import datetime
from constants import RESULT_PATH, TIME_DELAY_24_H, TABLE_NAME, \
    PARSE_TAGS_SHEET, CHAT_IDS_PATH
from container import table_manager, storage_manager, chat_ids
from utils import load_from_json
from container import bot, telebot_manager, data_manager
from tg_bot import main_handlers
# ------------------------------------------------------------------------

bot.register_message_handler(main_handlers.start_handler)
bot.register_message_handler(main_handlers.menu_handler)
bot.register_message_handler(main_handlers.all_prices_handler)
bot.register_message_handler(main_handlers.choose_school_handler)
bot.register_message_handler(main_handlers.common_profs_handler)
bot.register_message_handler(main_handlers.price_by_school_prof_handler)
bot.register_message_handler(main_handlers.prices_notice_handler)

chat_ids.update(set(load_from_json(CHAT_IDS_PATH)))


async def main() -> None:
    """Main function with necessary logic"""
    while True:
        start_time = datetime.now()
        table_manager.open_table(TABLE_NAME)
        parse_data = table_manager.load_from_table(PARSE_TAGS_SHEET)

        if not parse_data:
            parse_data = storage_manager.load_from_storage()

        if parse_data:
            old_data = load_from_json(RESULT_PATH)
            await table_manager.refresh(parse_data, old_data)
            storage_manager.save_to_storage(parse_data)
            await telebot_manager.send_messages(chat_ids)

        table_manager.close_table()
        data_manager.refresh_data()

        work_time = (datetime.now() - start_time).seconds
        await sleep(TIME_DELAY_24_H - work_time)


async def event_loop() -> None:
    """This function serves as an event loop to allow parser and telegram
    bot work together"""
    parse_task = create_task(main())
    tg_bot_task = create_task(bot.infinity_polling(non_stop=True))
    await gather(parse_task, tg_bot_task)


if __name__ == '__main__':
    run(event_loop())
