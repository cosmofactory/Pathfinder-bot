import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv


import keyboard
import api


load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


logging.basicConfig(
    level=logging.DEBUG,
    filename='program.log',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s',
    filemode='w'
)

storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)
type = (('type'), ('restaurant'))


class Location(StatesGroup):
    get = State()
    selects = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        'Этот бот поможет найти бар или ресторан рядом с вами.\n'
        'Нажмите кнопку "отправить свое местоположение",'
        ' чтобы бот узнал координаты.',
        reply_markup=keyboard.keyboard_reply
    )
    await Location.get.set()


@dp.message_handler(
        content_types=['location'],
        state=Location.get,
    )
async def get_location(message: types.Message, state: FSMContext):
    location = (f'{message.location.latitude},{message.location.longitude}')
    await message.answer(
        'Отлично, в каком радиусе будем искать?',
        reply_markup=keyboard.keyboard_inline
    )
    async with state.proxy() as data:
        data['location'] = location
    await Location.selects.set()

    

@dp.callback_query_handler(text=['300', '600', '1200'], state=Location.selects)
async def find_restaurant(
        callback_query: types.CallbackQuery,
        state: FSMContext
        ):
    async with state.proxy() as data:
        location = (('location'), (data['location']))
    radius = (('radius'), (callback_query.data))
    sorted_response = api.get_api_answer(radius, location, type)
    for number in range(0, 5):
        await callback_query.message.answer(
            api.send_message(number, sorted_response)
            )
    await callback_query.message.answer(
        'Попробовать еще раз?',
        reply_markup=keyboard.keyboard_inline_once_again
    )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
