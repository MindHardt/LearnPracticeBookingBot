import uuid

import telebot.types

import database.table_admins
from menus import admin_menu

create_admin_code_button_name = 'Использовать промокод'
filter_triggers = [create_admin_code_button_name]

bot = None


def handle_promocode(message):
    promocode = message.text
    if admin_menu.try_redeem_code(promocode, message.chat.id):
        pass