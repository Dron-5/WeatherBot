import telebot
from pyowm import OWM
from pyowm.utils.config import get_default_config
from telebot import types

bot = telebot.TeleBot("5761232959:AAGRwSOvWCULSXlBB2J8FiRdDds4019Etbk")

markup = types. ReplyKeyboardMarkup(resize_keyboard = True)
item1 = types.KeyboardButton("Москва")
item2 = types.KeyboardButton("Кострома")
item3 = types.KeyboardButton("Санкт-Петербург")
item4 = types.KeyboardButton("Адлер")

markup.add(item1, item2, item3, item4)


@bot.message_handler(commands=['start'])
def welcome(message):
	bot.send_message(message.chat.id, 'Добро пожаловать, ' + str(message.from_user.first_name) + '.\nВас приветствует бот погоды🌤' + '\n/start - запуск бота\n/help - команды бота\nЧтобы узнать погоду напишите в чат название города или выберите из списка ниже🏠', reply_markup=markup)

@bot.message_handler(commands=['help'])
def help(message):
	bot.send_message(message.chat.id, '/start - запуск бота\n/help - команды бота\nЧтобы узнать погоду напишите в чат название города или выберите из списка ниже🏠')

@bot.message_handler(content_types=['text'])
def test(message):
	try:
		place = message.text

		config_dict = get_default_config()
		config_dict['language'] = 'ru'

		owm = OWM('80d3c3e910eae3efe5e1da7b0d462a45', config_dict)
		mgr = owm.weather_manager()
		observation = mgr.weather_at_place(place)
		w = observation.weather

		t = w.temperature("celsius")
		t1 = t['temp']
		t2 = t['feels_like']
		t3 = t['temp_max']
		t4 = t['temp_min']

		wi = w.wind()['speed']
		humi = w.humidity
		cl = w.clouds
		st = w.status
		dt = w.detailed_status
		ti = w.reference_time('iso')
		pr = w.pressure['press']
		vd = w.visibility_distance

		bot.send_message(message.chat.id, "В городе " + str(place) +  "\n" + 
				"Температура: " + str(t1) + " °C" + "\n" + 
				"Максимальная температура: " + str(t3) + " °C" +"\n" + 
				"Минимальная температура: " + str(t4) + " °C" + "\n" + 
				"Ощущается как: " + str(t2) + " °C" + "\n" +
				"Скорость ветра: " + str(wi) + " м/с" + "\n" + 
				"Давление: " + str(pr) + " гПа" + "\n" + 
				"Влажность: " + str(humi) + " %" + "\n"
				"Описание:  " + str(dt) + "\n\n") 


	except:
		bot.send_message(message.chat.id,"Такой город не найден! \nПопробуйте еще раз!")
		print(str(message.text),"- не найден")

bot.polling(none_stop=True, interval=0)
