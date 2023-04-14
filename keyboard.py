from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton
)


request_places_btn_300 = InlineKeyboardButton(
    '300 m',
    callback_data='300'
)
request_places_btn_600 = InlineKeyboardButton(
    '600 m',
    callback_data='600'
)
request_places_btn_1200 = InlineKeyboardButton(
    '1200 m',
    callback_data='1200'
)
try_once_again_from_start = InlineKeyboardButton(
    'Начать сначала',
    callback_data='starting'
)


start = KeyboardButton('Отправить местоположение', request_location=True)

keyboard_inline = InlineKeyboardMarkup().add(
    request_places_btn_300,
    request_places_btn_600,
    request_places_btn_1200
)

keyboard_inline_once_again = InlineKeyboardMarkup().add(
    request_places_btn_300,
    request_places_btn_600,
    request_places_btn_1200
).add(
    try_once_again_from_start
)


keyboard_reply = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True
).add(start)
