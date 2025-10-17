import telebot # Импорты
import config
import random
import os
import json

token = config.token # Получение токена
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start']) # Команда start
def Command_start(message):
    keyboard = telebot.types.ReplyKeyboardRemove()
    bot.reply_to(message, "Привет! Я бот, который разрушает!\nОтправь мне текст, и я его разрушу.\nКартинки святы, не трогаю.", reply_markup=keyboard)

@bot.message_handler(commands=['help']) # Команда help
def Command_help(message):
    keyboard = telebot.types.ReplyKeyboardRemove()
    bot.reply_to(message, "1. Отправишь текст — я его разрушу.\n2. Отправишь картинку — я её не трону.", reply_markup=keyboard)

@bot.message_handler(commands=['destructor']) # Команда destructor
def Command_destructor(message):
    keyboard = telebot.types.ReplyKeyboardRemove()
    with open("TG-Bot/Destructor.jpg", "rb") as photo:
        bot.send_photo(message.chat.id, photo, caption="О нет! Моя белка!", reply_markup=keyboard)

@bot.message_handler(commands=['random_meme']) # Команда random meme
def Command_random_meme_first(message):
    files = os.listdir("TG-Bot/pics")
    random_image = random.choice(files)
    path = os.path.join("TG-Bot/pics", random_image)
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_memer = telebot.types.KeyboardButton(text="Хочу")
    keyboard.add(button_memer)
    with open(path, 'rb') as img:
        bot.send_photo(message.chat.id, img)
        bot.send_message(message.chat.id, "Хочешь ещё мем?", reply_markup=keyboard)
        img.close()

@bot.message_handler(func=lambda message: message.text == 'Хочу') # Если в предыдущей команде пользователь нажал "Хочу" на клавиатуре
def Command_random_meme_second(message):
    files = os.listdir("TG-Bot/pics")
    random_image = random.choice(files)
    path = os.path.join("TG-Bot/pics", random_image)
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_memer = telebot.types.KeyboardButton(text="Хочу")
    keyboard.add(button_memer)
    with open(path, 'rb') as img:
        bot.send_photo(message.chat.id, img)
        bot.send_message(message.chat.id, "Хочешь ещё мем?", reply_markup=keyboard)
        img.close()





@bot.message_handler(commands=['registrationsignin']) # Первая часть регистрации/входа
def Command_registration_step_one(message):
    bot.send_message(message.chat.id, "Так-с, посмотрим-с", reply_markup=telebot.types.ReplyKeyboardRemove())
    markup = telebot.types.InlineKeyboardMarkup()
    button_sign_in = telebot.types.InlineKeyboardButton("Войти", callback_data='signin')
    button_registration = telebot.types.InlineKeyboardButton("Зарегистрироваться", callback_data='register')
    markup.add(button_sign_in, button_registration)
    bot.send_message(message.chat.id, "Вы хотите зарегистрироваться или войти?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ['signin', 'register']) # Вторая часть регистрации/входа
def Command_registration_step_two(call):
    if call.data == 'signin':
        bot.send_message(call.message.chat.id, "Хорошо! Введите свой логин, ник или т.п. для входа:")
        bot.register_next_step_handler(call.message, process_entering, mode='signin')
    elif call.data == 'register':
        bot.send_message(call.message.chat.id, "Давайте начнем регистрацию! Введите логин, ник или т.п. как хотите:")
        bot.register_next_step_handler(call.message, process_entering, mode='register')

def process_entering(message, mode): # Третья часть регистрации/входа
    login = message.text
    with open('TG-Bot/Users.json', 'r', encoding='utf-8') as users_file:
        users_data = json.load(users_file)
        if mode == 'signin':
            if login in users_data:
                if users_data[login] == message.chat.id:
                    bot.send_message(message.chat.id, f"Вы упешно вошли! Но на данный момент это вам ничего не даст.")
            else:
                bot.send_message(message.chat.id, f"Подите вон отсюда, чужак!\nИли вы ввели неправильный ник(или т.п.).\nПопробуйте снова.")
        else:
            if login in users_data:
                bot.send_message(message.chat.id, f"Такой ник(или т.п.) уже есть, пройдите процедуру заново.")
            else:
                users_data[login] = message.chat.id
                with open('TG-Bot/Users.json', 'w', encoding='utf-8') as users_file:
                    json.dump(users_data, users_file, ensure_ascii=False, indent=4)
                bot.send_message(message.chat.id, f"Регистрация завершена!\nВаш логин: {login}")





@bot.message_handler(content_types=["text"]) # Ответ на полученный текст
def Text_handler(message):
    keyboard = telebot.types.ReplyKeyboardRemove()
    answer_list = list(message.text)
    random.shuffle(answer_list)
    answer = "".join(answer_list)
    bot.reply_to(message, answer, reply_markup=keyboard)

@bot.message_handler(content_types=["photo"]) # Ответ на полученную картинку
def Picture_handler(message):
    keyboard = telebot.types.ReplyKeyboardRemove()
    file_id = message.photo[-1].file_id
    bot.send_photo(message.chat.id, file_id, caption="Фото свято, я его не трогаю.", reply_markup=keyboard)

bot.infinity_polling()