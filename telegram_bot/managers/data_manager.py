"""This unit contains a DataManager class serves to get requested data"""
from typing import Optional
from telebot.util import MAX_MESSAGE_LENGTH
from utils import load_from_json
# --------------------------------------------------------------------------


class DataManager:
    """The DataManager class provides logic to get data from JSON file"""
    def __init__(self, filename: str) -> None:
        """Initialize the DataManager
        :param filename: The path to the JSON file
        """
        self.data = load_from_json(filename)
        self._chosen_school = {}
        self.data_file = filename

    def get_school_names(self) -> Optional[list[str]]:
        """This method returns a list of all available school names
        :return: A list of school names
        """
        return [name for name in self.data]

    def get_course_by_school(self, school_name: str, chat_id: int) -> list[str]:
        """This method returns a list of professions available for
        a given school
        :param school_name: The string representing the school name
        :param chat_id: The id of the chat to send school list
        :return: A list of available courses for a given school
        """
        self._chosen_school[chat_id] = school_name
        courses = [course_data.get('profession') for course_data
                   in self.data.get(school_name, self.get_common_courses())]

        courses = list(set(courses))
        courses.sort()
        return courses

    def get_common_courses(self) -> list[str]:
        """This method returns a list of all courses present in the all
        schools
        :return: A list of courses
        """
        common_courses = set()

        for courses in self.data.values():
            if not common_courses:
                common_courses.update(
                    (course.get('profession') for course in courses))
            else:
                common_courses & set(
                    [course.get('profession') for course in courses])

        common_courses = list(common_courses)
        common_courses.sort()

        return common_courses

    def get_all_prices(self) -> list[str]:
        """This method creates a string with all prices existing in the file
        :return: A list of strings containing all prices
        """
        messages = []
        result = ''

        for school in self.data:
            for course_data in self.data.get(school, []):
                result += f'{school}:\n'
                record = self._create_record(course_data)
                messages, result = self._create_message_list(
                    result, record, messages)
                result += record

        if result not in messages:
            messages.append(result)

        return messages if messages else [result]

    @staticmethod
    def _create_message_list(
            message: str, current_record: str,
            messages: list) -> tuple[list, str]:
        """This method creates a list of strings from a single string if the
        message has a length greater than the maximum allowed length
        :param message: A string representing the message to check
        :param current_record: A part of message to add to the message
        :param messages: A list to add messages
        :return: A tuple containing a list of messages and a message string
        """
        if len(current_record + message) > MAX_MESSAGE_LENGTH:
            messages.append(f'\n{message}')
            message = ''

        return messages, message

    def get_prices_by_school(self, school_name: str) -> list[str]:
        """This method returns a string containing all prices for a
        given school
        :param school_name: The string representing the school name
        :return: A list of strings containing all prices for a given school
        """
        result = f'{school_name}\n'
        for course_data in self.data.get(school_name, []):
            result += self._create_record(course_data)

        return [result]

    def get_prices_by_profession(self, profession: str) -> list[str]:
        """This method returns a string containing all prices from all schools
        for a given profession
        :param profession: The string representing the profession name
        :return: A list of strings containing all prices for a given profession
        """
        result = ''
        messages = []
        for school, courses in self.data.items():
            for course_data in filter(
                    lambda x: x['profession'] == profession, courses):
                result += f'{school}:\n'
                record = self._create_record(course_data)
                messages, result = self._create_message_list(
                    result, record, messages)
                result += record

        return messages if messages else [result]

    def get_by_school_and_prof(
            self, school_name: str, prof_name: str) -> list[str]:
        """This method returns a string containing all prices from chosen
        school and profession
        :param school_name: The string representing the school name
        :param prof_name: The string representing the profession name
        :return: A list of strings containing all prices for a given school and
        profession
        """
        result = f'{school_name}\n'
        courses = self.data.get(school_name, [])
        for course in filter(lambda x: x['profession'] == prof_name, courses):
            result += self._create_record(course)

        return [result]

    def get_chosen_school(self, chat_id: int) -> str:
        """This method returns a string containing the chosen school
        :return: A string containing the chosen school
        """
        return self._chosen_school.get(chat_id)

    def remove_chosen_school(self, chat_id: int) -> None:
        """This method removes the chosen school"""
        self._chosen_school[chat_id] = None

    @staticmethod
    def _create_record(course_data: dict) -> str:
        """This serves to create a record for a given course
        :param course_data: The dictionary representing the course data
        :return: A string containing the created record
        """
        record = f'''
            {course_data.get("profession")}\n
            Тариф: {course_data.get("course_level")}\n
            Цена в месяц - {course_data.get("price")} руб.\n
            Кол-во месяцев - {course_data.get("period")}\n
            Итоговая цена - {course_data.get("total")} руб.\n
            {'-' * 30}
            '''
        return record

    def refresh_data(self) -> None:
        """This method serves to actualize data"""
        self.data = load_from_json(self.data_file)
