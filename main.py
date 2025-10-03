import telebot
import config
import random
import os

token = config.token
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот, который разрушает!\nОтправь мне текст, и я его разрушу.\nКартинки святы, не трогаю.")

@bot.message_handler(commands=['destructor'])
def send_destructor(message):
    with open("Destructor.jpg", "rb") as photo:
        bot.send_photo(message.chat.id, photo, caption="О нет! Моя белка!")

@bot.message_handler(commands=['random_meme'])
def send_destructor(message):
    with open("Destructor.jpg", "rb") as photo:
        files = os.listdir("pics")
        random_image = random.choice(files)
        path = os.path.join("pics", random_image)
        with open(path, 'rb') as img:
            bot.send_photo(message.chat.id, img)

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "1. Отправишь текст — я его разрушу.\n2. Отправишь картинку — я её не трону.")

@bot.message_handler(content_types=["text"])
def Text_message_handler(message):
    answer_list = list(message.text)
    random.shuffle(answer_list) 
    answer = "".join(answer_list)
    bot.reply_to(message, answer)

@bot.message_handler(content_types=["photo"])
def Text_picture_handler(message):
    file_id = message.photo[-1].file_id
    bot.send_photo(message.chat.id, file_id, caption="Фото свято, я его не трогаю.")

bot.infinity_polling()
