import telebot.types
from telebot import types


def get_pagination_markup() -> telebot.types.InlineKeyboardMarkup:
    paginator = types.InlineKeyboardMarkup(row_width=2)
    backward_button = types.InlineKeyboardButton('<', callback_data='page_b')
    forward_button = types.InlineKeyboardButton('>', callback_data='page_f')
    paginator.add(backward_button, forward_button)

    return paginator
