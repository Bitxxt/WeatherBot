import telebot
import requests
import json
from translate import Translator

token = "6751568884:AAF5Cmegg6ebL1Pof09TBevbSjAScqN_A2g"
bot = telebot.TeleBot(token)
API = "96351c4148d13495b7aab3f40ead2e2a"

translator = Translator(from_lang='english', to_lang='russian')


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет, напишите город в котором находитесь что бы узнать погоду в нем)))")


@bot.message_handler(content_types=['text'])
def city_message(message):
    city = message.text.strip().lower()
    res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric")
    # bot.reply_to(message, f'Сейчас погода:{res.json()}')
    if res.status_code == 200:  # Проверка на наличие ошибок
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        feel_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        wind_gust = data["wind"]["gust"]
        weather = data['weather'][0]
        weather_description = weather['description']
        translation = translator.translate(weather_description)
        icon_url = f"http://openweathermap.org/img/wn/{weather['icon']}@2x.png"
        bot.send_photo(message.chat.id, icon_url)
        bot.reply_to(message, f"Температура сейчас: {temp}℃\nОщущается как: {feel_like}℃\nВлажность: {humidity}%\n"
                              f"Скорость ветра: {wind}м/с\nПорывы ветра достигают: {wind_gust}м/с\n"
                              f"Описание: {translation}")
        bot.send_message(message.chat.id, "Введете другой город чтобы узнать погоду в нем")
    else:
        bot.reply_to(message, "Неверно указан город")


bot.infinity_polling()
