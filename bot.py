from telebot import TeleBot
from buttons import change_groups, accept_to_send_msg, main_menu
from selenium_finds_whatsapp import selenium_whatsapp_get_site
bot = TeleBot(token='Token here')
temp_messages = {}

@bot.message_handler(commands = ['start'])
def start(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Введите пароль')
    bot.register_next_step_handler(message, check_pass)

def check_pass(message):
    user_id = message.from_user.id
    password = message.text
    if password == "your password':
        bot.send_message(user_id, 'Добро пожаловать', reply_markup= main_menu())
    else:
        bot.send_message(user_id, 'Пароль не правильный')
        bot.register_next_step_handler(message, check_pass)

@bot.message_handler(func=lambda message: message.text == 'Рассылка')
def country_selection(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Выберите группу чатов', reply_markup=change_groups())

@bot.message_handler(func=lambda message : message.text in ['World🌎', 'USA🇺🇸', 'Russia 1000🇷🇺', 'Russia 60🇷🇺',
                                                            'SPB🇷🇺', 'Moscow 1000🇷🇺', 'Moscow 60🇷🇺',
                                                            'Ekaterinburg🇷🇺', 'Novosibirsk🇷🇺', 'Sochi🇷🇺',
                                                            'Ukraine🇺🇦', 'Europe🌍', 'Armenia🇦🇲', 'Azerbaijan🇦🇿',
                                                            'Georgia🇬🇪', 'Moldova🇲🇩', 'Germany🇩🇪', 'London🇬🇧',
                                                            'Spain🇪🇸', 'Argentina🇦🇷', 'Italy🇮🇹', 'israel🇮🇱', 'Greece🇬🇷',
                                                            'Cyprus🇨🇾', 'Brazil🇧🇷', 'Dubai🇦🇪', 'Thailand🇹🇭', 'Asia🌏',
                                                            'Kazahstan🇰🇿', 'Turkey🇹🇷', 'Bali🇮🇩'])
def send_to_moscow_chats(message):
    user_id = message.from_user.id
    geo = message.text
    bot.send_message(user_id, 'Введите текст для рассылки')
    bot.register_next_step_handler(message, newsletter, geo)

def  newsletter(message, geo):
    user_id = message.from_user.id
    newsletter_text = message.text
    accept_msg = bot.send_message(user_id, f'ГЕО - {geo}\nВаш текст\n{newsletter_text}\nВерно?',
                     reply_markup=accept_to_send_msg())
    temp_messages[user_id] = {'geo':geo, 'text':newsletter_text, 'msg_id':accept_msg.message_id, 'user_id':user_id}


@bot.callback_query_handler(lambda call: call.data == 'accept')
def confirm_send(message):
    user_id = message.from_user.id
    if user_id in temp_messages:
        data = temp_messages.pop(user_id)
        geo, msg, msg_id, user_id = data['geo'], data['text'], data['msg_id'], data['user_id']
        print(user_id)
        print(f'{geo} телега засчитала')
        selenium_whatsapp_get_site(user_id=user_id, msg=msg, geo=geo)
        bot.send_message(user_id, 'Рассылка в процессе', reply_markup=main_menu())
        bot.delete_message(user_id,msg_id)
    else:
        bot.send_message(user_id, 'Ошибка, обратитесь к разработчику @kadambaev_o')

@bot.callback_query_handler(lambda call: call.data == 'decline')
def decline_send(message):
    user_id = message.from_user.id
    data = temp_messages.pop(user_id)
    bot.delete_message(user_id, message_id=data['msg_id'])
    bot.send_message(user_id, 'Отмена действия', reply_markup=main_menu())

@bot.message_handler(func=lambda message: message.text == 'Группы')
def show_groups(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Список стран\nMoscow | SPB | Dubai | Europa | Azer\n'
                              'Для добавления\Удаления обратитесь к разработчику @kadambaev_o',
                     reply_markup=main_menu())
bot.infinity_polling(skip_pending=True)