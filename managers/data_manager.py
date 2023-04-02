"""This unit contains a DataManager class serves to get requested data"""
from typing import Optional
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

    def get_school_names(self) -> Optional[list[str]]:
        """This method returns a list of all available school names
        :return: A list of school names
        """
        return [name for name in self.data]

    def get_course_by_school(self, school_name: str, chat_id: int) -> list[str]:
        """This method returns a list of professions available for
        a given school
        :param school_name: The string representing the school name
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

    def get_all_prices(self) -> str:
        """This method creates a string with all prices existing in the file
        :return: A string containing all prices
        """
        result = ''
        for school in self.data:
            result += f'{school}:\n'

            for course_data in self.data.get(school, []):
                result += self._create_record(course_data)

        return result

    def get_prices_by_school(self, school_name: str) -> str:
        """This method returns a string containing all prices for a
        given school
        :param school_name: The string representing the school name
        :return: A string containing all prices for a given school
        """
        result = f'{school_name}\n'
        for course_data in self.data.get(school_name, []):
            result += self._create_record(course_data)

        return result

    def get_prices_by_profession(self, profession: str) -> str:
        """This method returns a string containing all prices from all schools
        for a given profession
        :param profession: The string representing the profession name
        :return: A string containing all prices for a given profession
        """
        result = ''
        for school, courses in self.data.items():
            result += f'{school}:\n'
            for course_data in filter(
                    lambda x: x['profession'] == profession, courses):

                result += self._create_record(course_data)

        return result

    def get_by_school_and_prof(self, school_name: str, prof_name: str) -> str:
        """This method returns a string containing all prices from chosen
        school and profession
        :param school_name: The string representing the school name
        :param prof_name: The string representing the profession name
        :return: A string containing all prices for a given school and
        profession
        """
        result = f'{school_name}\n'
        courses = self.data.get(school_name, [])
        for course in filter(lambda x: x['profession'] == prof_name, courses):
            result += self._create_record(course)

        return result

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
            Цена в месяц - {course_data.get("price")}\n
            Кол-во месяцев - {course_data.get("period")}\n
            Итоговая цена - {course_data.get("total")}\n
            {'-' * 30}
            '''
        return record
