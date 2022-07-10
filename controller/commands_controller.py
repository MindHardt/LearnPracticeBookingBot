from commands import draw_map_command, hotel_search_command, redeem_promocode_command, create_promocode_command, \
    register_command, login_command, logout_command, info_command, set_config_command, view_config_command


def handle_command(message, bot):
    try:
        call = message.text
        if call == "Точка на карте":
            draw_map_command.execute(message, bot)
        elif call == "Найти отель":
            hotel_search_command.execute(message, bot)
        elif call == "Использовать промокод":
            redeem_promocode_command.execute(message, bot)
        elif call == "Создать промокод":
            create_promocode_command.execute(message, bot)
        elif call == "Зарегистрироваться":
            register_command.execute(message, bot)
        elif call == "Войти":
            login_command.execute(message, bot)
        elif call == "Выйти":
            logout_command.execute(message, bot)
        elif call == "Инфо":
            info_command.execute(message, bot)
            # ADMIN COMMANDS
        elif call.startswith("=setconfig"):
            set_config_command.execute(message, bot)
        elif call == "=viewconfig":
            view_config_command.execute(message, bot)

    except Exception as e:
        bot.send_message(message.chat.id, e.__str__())
