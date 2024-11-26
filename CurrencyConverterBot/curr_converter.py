import json
from time import sleep
from currency.converter import conversion_rate
from telebot import types, TeleBot
from auth import TOKEN2


class User:
    def __init__(self):
        self.pair = None
        self.rate = 0


bot = TeleBot(TOKEN2)
users = {}


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    btn1 = types.KeyboardButton('RUB/USD')
    btn2 = types.KeyboardButton('RUB/EUR')
    btn3 = types.KeyboardButton('RUB/GEL')
    btn4 = types.KeyboardButton('RUB/TRY')
    btn5 = types.KeyboardButton('RUB/AED')
    btn6 = types.KeyboardButton('RUB/KZT')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=3)
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    bot.send_message(message.chat.id, 'Выберете валютную пару\n'
                                      'или ведите валютную пару в формате "ХХХ/ХХХ"\n'
                                      'Перечень валютных кодов - "/help"', reply_markup=markup)


@bot.message_handler(commands=['help'])
def curr_list(message): 
    with open('currencies.json') as file:
        curr_dict = json.load(file)
        ans = '\n'.join((f'{key} - {curr_dict[key]["name"]}' for key in curr_dict))
    bot.send_message(message.chat.id, ans)


def valid_amount(message: types.Message):
    try:
        amount = abs(float(message.text))
        val1, val2 = users.get(message.from_user.id).pair
        rate = users.get(message.from_user.id).rate
        bot.send_message(message.chat.id, f'{amount} {val1} = {amount * rate:,.1f} {val2}')
        sleep(1)
        start(message)
    except ValueError:
        bot.send_message(message.chat.id, 'Введите корректное значение:')
        bot.register_next_step_handler(message, valid_amount)


@bot.message_handler(content_types=['text'])
def valid_pair(message: types.Message):
    try:
        pair = message.text.split('/')
        rate = conversion_rate(*pair)
        if not isinstance(rate, float):
            raise ValueError
        take_user_rates(message.from_user.id, pair, rate)
        bot.send_message(message.chat.id, 'Введите сумму:')
        bot.register_next_step_handler(message, valid_amount)
    except Exception:
        bot.send_message(message.chat.id, 'Неверная валютная пара, введите корректную пару:')
        bot.register_next_step_handler(message, valid_pair)


def take_user_rates(user_id, pair, rate):
    user = users.setdefault(user_id, User())
    user.pair = pair
    user.rate = rate


bot.polling(none_stop=True)
