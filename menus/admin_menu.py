import uuid
import database.table_admins

create_admin_code_button_name = 'Создать админ-код'
triggers = [create_admin_code_button_name]

admin_codes = []
bot = None


def handle_message(message):
    if message.text == create_admin_code_button_name:
        new_code = create_code()
        bot.send_message(message.chat.id, f'Ваш новый админ-код `{new_code}`\nОн действует до перезапуска бота.')


def create_code() -> str:
    new_code = uuid.uuid4().__str__()
    admin_codes.append(new_code)
    return new_code


def try_redeem_code(code, user_id) -> bool:
    if code in admin_codes:
        database.table_admins.add_admin(user_id)
        admin_codes.remove(code)
        return True
    else:
        return False
