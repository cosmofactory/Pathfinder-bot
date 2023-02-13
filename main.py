import logging

from aiogram import Bot, Dispatcher, executor, types

import keyboard
import api


API_TOKEN = ('')


logging.basicConfig(
    level=logging.DEBUG,
    filename='program.log',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s',
    filemode='w'
)


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

#location = (('location'), ('55.739876,37.544188'))
type = (('type'), ('restaurant'))

@dp.message_handler(commands=['start',])
async def start(message: types.Message):
    await message.answer(
        'Этот бот поможет найти бар или ресторан рядом с вами.\n'
        'Нажмите кнопку отправить__свое_местоположение,'
        ' чтобы бот узнал координаты',
        reply_markup=keyboard.keyboard_reply
    )


@dp.message_handler(commands=['отправить_свое_местоположение',])
async def get_location(message: types.Message):
    await message.answer(
        'Отлично, в каком радиусе будем искать?',
        reply_markup=keyboard.keyboard_inline
    )

@dp.callback_query_handler(text=['300', '600', '1200'])
async def find_restaurant(callback_query: types.CallbackQuery):
    location = (('location'), (f'{callback_query.message.location.latitude},{callback_query.message.location.longitude}'))
    radius = (('radius'), (callback_query.data))
    sorted_response = api.get_api_answer(radius, location, type)
    for number in range(0, 5):
        await callback_query.message.answer(api.send_message(number, sorted_response))
    await callback_query.answer()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
