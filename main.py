import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from dotenv import load_dotenv

import api
import keyboard
from messages import MESSAGE

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


logging.basicConfig(
    level=logging.INFO,
    filename='program.log',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s',
    filemode='w'
)

storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)


class Location(StatesGroup):
    """Storage for coordinates."""

    get = State()
    selects = State()


class Establishment(StatesGroup):
    """Storage for place type."""

    establishment_type = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    """Initial message."""

    logging.info('Bot started')
    await message.answer(
        MESSAGE['initial_message'],
        reply_markup=keyboard.keyboard_type
    )
    await Establishment.establishment_type.set()


@dp.message_handler(
        content_types=['location'],
        state=Location.get
    )
async def get_location(message: types.Message, state: FSMContext):
    """Getting location of user."""

    location = (f'{message.location.latitude},{message.location.longitude}')
    logging.info(f'Location coordinates {location}')
    await message.answer(
        MESSAGE['what_radius'],
        reply_markup=keyboard.keyboard_inline
    )
    async with state.proxy() as data:
        data['location'] = location
    await Location.selects.set()


@dp.callback_query_handler(text=['300', '600', '1200'], state='*')
async def find_restaurant(
        callback_query: types.CallbackQuery,
        state: FSMContext
        ):
    """Finding the desired places with given range and type."""

    async with state.proxy() as data:
        try:
            location = (('location'), (data['location']))
            type = (('type'), (data['type']))
        except KeyError as error:
            logging.info(error)
            pass
    radius = (('radius'), (callback_query.data))
    logging.info(f'Selected radius {radius}')
    logging.info(f'Selected type {type}')
    sorted_response = api.get_api_answer(radius, location, type)
    try:
        for number in range(0, 10):
            await callback_query.message.answer(
                api.send_message(number, sorted_response),
                parse_mode=types.ParseMode.HTML
                )
    except IndexError as end_of_list:
        logging.error(f'Error {end_of_list}', exc_info=True)
        if number == 0:
            await callback_query.message.answer(
                MESSAGE['nothing_found']
            )
        else:
            await callback_query.message.answer(
                MESSAGE['end_of_search']
            )
    await callback_query.message.answer(
        MESSAGE['another_radius'],
        reply_markup=keyboard.keyboard_inline_once_again
    )
    await callback_query.answer()


@dp.callback_query_handler(text=['starting'], state='*')
async def start_from_the_beginning(callback_query: types.CallbackQuery):
    """Starting from the very beginning."""

    await callback_query.message.answer(
        MESSAGE['what_type'],
        reply_markup=keyboard.keyboard_type
    )
    await callback_query.answer()


@dp.callback_query_handler(text=['cafe', 'bar', 'restaurant'], state='*')
async def select_type_of_establishment(
    callback_query: types.CallbackQuery, state: FSMContext
):
    """Selecting type of place and requesting location."""

    async with state.proxy() as data:
        data['type'] = callback_query.data
        logging.info(f'data type {callback_query.data}')
    await Establishment.establishment_type.set()
    await callback_query.message.answer(
        MESSAGE['send_loc'],
        reply_markup=keyboard.keyboard_reply
    )
    await Location.get.set()
    await callback_query.answer()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
