from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


request_places_btn = InlineKeyboardButton(
    'Find restaurants nearby',
    callback_data='find_restaurant'
)

keyboard_inline = InlineKeyboardMarkup().add(request_places_btn)
