from aiogram.types import ReplyKeyboardMarkup,KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def load_start_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text = '/register'),
                KeyboardButton(text = '/help'))

    return builder.as_markup(resize_keyboard = True,one_time_keyboard = True)

def load_default_buttons() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text = '/iq'),
                KeyboardButton(text = '/changeiq'),
                KeyboardButton(text = '/help'))

    return builder.as_markup(resize_keyboard=True)
