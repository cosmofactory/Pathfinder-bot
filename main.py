import logging

from logging.handlers import RotatingFileHandler
from aiogram import Bot, Dispatcher, executor, types

import keyboard
import api


API_TOKEN = ('6192684062:AAHifOjOLX-WH2c9wZSzPZEExGOH7g4JnYU')


logging.basicConfig(
    level=logging.DEBUG,
    filename='program.log',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s',
    filemode='w'
)

logger = logging.getLogger('my_app')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s'
)
my_handler = RotatingFileHandler(
    'logging.log',
    maxBytes=500,
    backupCount=2
)
my_handler.setFormatter(formatter)
my_handler.setLevel(logging.DEBUG)
logger.addHandler(my_handler)


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start',])
async def start(message: types.Message):
    await message.reply(
        'Select a place to eat',
        reply_markup=keyboard.keyboard_inline
    )


@dp.callback_query_handler(text='find_restaurant')
async def find_restaurant(callback_query: types.CallbackQuery):
    await callback_query.message.reply('I found this!')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
