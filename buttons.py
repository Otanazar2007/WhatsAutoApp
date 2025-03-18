from telebot import types


def main_menu():
    """
    These are the main menu buttons (after entering the password)
    you can add other auxiliary buttons here from yourself

    """
    kb = types.ReplyKeyboardMarkup(row_width=2)
    button = types.KeyboardButton(text='Рассылка')
    kb.add(button)
    return kb

def change_groups():
    """
    Add the name of your group to the buttons,
    increase or decrease the number depending on the number of group categories,
    this will play a key role in the project later
    example:
    """
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)
    world = types.KeyboardButton(text='World🌎')
    usa = types.KeyboardButton(text='USA🇺🇸')
    kb.add(world, usa)
    return kb

def accept_to_send_msg():
    """
    These 2 buttons play a big role,
    "accept" runs the Selenium script and "decline"
    on the contrary deletes

    """
    kb = types.InlineKeyboardMarkup(row_width=2)
    button = types.InlineKeyboardButton(text='Готово', callback_data='accept')
    button2 = types.InlineKeyboardButton(text='Отменить', callback_data='decline')
    kb.row(button)
    kb.row(button2)
    return kb