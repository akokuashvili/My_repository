import telebot
from auth import TOKEN
from request_functions import weather_response, country_response


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'Напиши город, где хочешь узнать погоду')


@bot.message_handler(content_types=['text'])
def get_weather(message: telebot.types.Message):
    print(message.__dict__)
    if message.text.lower() in ('спасибо', 'спасибо!'):
        bot.send_message(message.chat.id, 'Мне не трудно, в каком городе хотите узнать погоду?')
    else:
        city = message.text.lower().strip()
        weather = weather_response(city)
        country = country_response(weather['sys'].get('country'))
        if weather['cod'] == 200:
            w = weather["wind"].get("gust")
            wind_gust = f'\nпорывы до: {w:.1f} м/с' if w else ''
            answer = f'Страна: {country}\n'\
                     f'Населенный пункт: {weather["name"]}\n' \
                  f'Погода: {weather["weather"][0]["description"]}\n' \
                  f'Температура: {weather["main"].get("temp"):.1f}ºС\n' \
                  f'Влажность воздуха: {weather["main"].get("humidity")}%\n' \
                  f'Скорость ветра: {weather["wind"]["speed"]:.1f} м/с{wind_gust}'
            bot.send_message(message.chat.id, answer)
        else:
            bot.send_message(message.chat.id, 'Неверное название города, введите заново')


bot.polling(none_stop=True)