"""This file contains functions serves as telegram bot handlers"""
from random import choice
from telebot import types
from constants import CHAT_IDS_PATH
from container import chat_ids, data_manager
from tg_bot import bot_phrases
from container import bot
from utils import save_data_to_json
# -------------------------------------------------------------------------


@bot.message_handler(commands=['start'])
async def start_handler(message) -> None:
    """This async handler processes 'start' command sending from telegram
    bot
    :param message: A message object containing chat id, text and so on
    """
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_button = types.KeyboardButton(text='Меню')
    buttons.add(menu_button)

    if message.chat.id not in chat_ids:
        text = choice(bot_phrases.get('greetings'))

    else:
        text = choice(bot_phrases.get('member_greetings'))

    await bot.send_message(
        message.chat.id,
        text=text,
        reply_markup=buttons)


@bot.message_handler(func=lambda message: message.text == 'Меню')
async def menu_handler(message) -> None:
    """This async handler serves to precess 'Меню' text sending from telegram
    bot
    :param message: A message object containing chat id, text and so on
    """
    data_manager.remove_chosen_school(message.chat.id)

    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_button = types.KeyboardButton('Меню')
    all_prices_button = types.KeyboardButton('Все прайсы')
    prices_by_prof_button = types.KeyboardButton('Прайсы по профессии')
    prices_by_school_button = types.KeyboardButton('Прайсы по конкурентам')

    if message.chat.id not in chat_ids:
        subscribe_button = types.KeyboardButton(text='Включить уведомления')
        buttons.add(subscribe_button)

    else:
        unsubscribe_button = types.KeyboardButton(text='Отключить уведомления')
        buttons.add(unsubscribe_button)

    text = (f"{bot_phrases.get('menu_info')}{'*' * 40}\n" +
            f"\n{'-' * 80}\n".join(bot_phrases.get('menu')))

    buttons.add(menu_button, all_prices_button, prices_by_prof_button)
    buttons.add(prices_by_school_button)

    await bot.send_message(
        message.chat.id,
        text=text,
        reply_markup=buttons)


@bot.message_handler(
    func=lambda message: message.text in ['Включить уведомления',
                                          'Отключить уведомления'])
async def prices_notice_handler(message) -> None:
    """This async handler serves to switch on or the switch off price change
    notifications
    :param message: A message object containing chat id, text and so on
    """
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_button = types.KeyboardButton(text='Меню')
    buttons.add(menu_button)

    if message.text == 'Включить уведомления':
        chat_ids.add(message.chat.id)
        unsubscribe_button = types.KeyboardButton(text='Отключить уведомления')
        buttons.add(unsubscribe_button)
        text = bot_phrases.get('subscribe_success')

    elif message.text == 'Отключить уведомления':
        chat_ids.discard(message.chat.id)
        subscribe_button = types.KeyboardButton(text='Включить уведомления')
        buttons.add(subscribe_button)
        text = bot_phrases.get('unsubscribe_success')

    save_data_to_json(list(chat_ids), CHAT_IDS_PATH)
    await bot.send_message(
        message.chat.id,
        text=text,
        reply_markup=buttons
    )


@bot.message_handler(func=lambda message: message.text == 'Все прайсы')
async def all_prices_handler(message) -> None:
    """This async handler serves to show all available prices
    :param message: A message object containing chat id, text and so on
    """
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_button = types.KeyboardButton(text='Меню')
    buttons.add(menu_button)
    text = data_manager.get_all_prices()

    await bot.send_message(
        message.chat.id,
        text=text,
        reply_markup=buttons)


@bot.message_handler(
    func=lambda message: message.text == 'Прайсы по профессии'
    or message.text in data_manager.get_common_courses() and not
    data_manager.chosen_school)
async def common_profs_handler(message) -> None:
    """This async handler serves to show prices by certain profession and
    menu with all available professions
    :param message: A message object containing chat id, text and so on
    """
    common_courses = data_manager.get_common_courses()

    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_button = types.KeyboardButton(text='Меню')
    prof_buttons = [types.KeyboardButton(prof) for prof in common_courses]
    buttons.add(menu_button)
    buttons.add(*prof_buttons)

    if message.text == 'Прайсы по профессии':
        text = 'А теперь выберите профессию и узнаете прайсы всех конкурентов'
    else:
        text = data_manager.get_prices_by_profession(message.text)

    await bot.send_message(
        message.chat.id,
        text=text,
        reply_markup=buttons)


@bot.message_handler(
    func=lambda message: message.text == 'Прайсы по конкурентам'
    or message.text in data_manager.get_school_names())
async def choose_school_handler(message) -> None:
    """This async handler serves to show available schools and to allow user
    to choose one
    :param message: A message object containing chat id, text and so on
    """
    schools = data_manager.get_school_names()

    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_button = types.KeyboardButton(text='Меню')

    if message.text == 'Прайсы по конкурентам':
        school_buttons = [types.KeyboardButton(button) for button in schools]
        buttons.add(menu_button, *school_buttons)
        text = 'Выберите школу чтобы получить текущие прайсы'

    else:
        all_courses_button = types.KeyboardButton('Все курсы')
        school_courses = data_manager.get_course_by_school(message.text,
                                                           message.chat.id)
        school_courses_buttons = [
            types.KeyboardButton(course) for course in school_courses]
        buttons.add(all_courses_button, *school_courses_buttons)
        text = 'Выберите желаемую профессию'

    await bot.send_message(
        message.chat.id,
        text=text,
        reply_markup=buttons)


@bot.message_handler(
    func=lambda message: message.text
    in ['Все курсы', *data_manager.get_course_by_school(
        data_manager.get_chosen_school(message.chat.id))])
async def price_by_school_prof_handler(message) -> None:
    """This async handler serves to show prices by previously chosen school
    and certain profession or by all professions available in the school
    :param message: A message object containing chat id, text and so on
    """
    school_courses = data_manager.get_course_by_school(
        data_manager.chosen_school)

    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)

    menu_button = types.KeyboardButton(text='Меню')
    all_courses_button = types.KeyboardButton('Все курсы')
    school_courses_buttons = [
        types.KeyboardButton(course) for course in school_courses]

    buttons.add(menu_button, all_courses_button, *school_courses_buttons)

    if message.text == 'Все курсы':
        text = data_manager.get_prices_by_school(
            data_manager.get_chosen_school(message.chat.id))

    else:
        text = data_manager.get_by_school_and_prof(
            data_manager.chosen_school, message.text)

    await bot.send_message(
        message.chat.id,
        text=text,
        reply_markup=buttons)
