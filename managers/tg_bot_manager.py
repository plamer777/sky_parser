"""This file contains a TelebotManager class providing functionality to work
with messages sending to users"""
from telebot.async_telebot import AsyncTeleBot
from constants import RESULT_PATH
from tg_bot import bot_phrases, load_from_json
# ---------------------------------------------------------------------------


class TelebotManager:
    """The TelebotManager class serves to prepare and send messages to users"""
    def __init__(self, tg_bot: AsyncTeleBot) -> None:
        """Initialization of the class
        :param tg_bot: An instance of AsyncTeleBot class
        """
        self.tg_bot = tg_bot
        self.price_changes = []

    async def send_messages(self, chats: list[int]) -> None:
        """This async method serves to send prepared messages to users
        :param chats: A list of ids of users' chats
        """
        self._create_change_messages()
        for chat in chats:
            await self.tg_bot.send_message(
                chat, text='\n'.join(self.price_changes))

        self._clear_changes_list()

    def _create_change_messages(self) -> None:
        """This secondary method serves to create messages with price
        changes"""
        results = load_from_json(RESULT_PATH)
        for school, courses in results.items():
            for course_data in filter(
                    lambda x: x['price_change'] != 0, courses):

                self._add_new_message(school, course_data)

    def _add_new_message(self, school: str, course_data: dict) -> None:
        """This secondary method serves to create a single message with
        school name, profession and price change
        :param school: The school name
        :param course_data: A dictionary containing profession information
        such as name, price, changes, etc.
        """
        if not self.price_changes:
            self._add_message_title()
        price_change = course_data.get('price_change')
        profession = course_data.get('profession')
        tariff = course_data.get('course_level')

        if price_change < 0:
            template = bot_phrases.get('price_down')
        else:
            template = bot_phrases.get('price_up')

        template = template.format(
            school, profession, tariff, abs(price_change)) + f"\n{'*' * 30}"

        if template not in self.price_changes:
            self.price_changes.append(template)

    def _add_message_title(self) -> None:
        """This secondary method serves to add title to the list of messages"""
        self.price_changes.append(bot_phrases.get('change_title'))

    def _clear_changes_list(self) -> None:
        """This method clears the list of changes"""
        self.price_changes = []
