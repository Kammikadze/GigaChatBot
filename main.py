from Modules.DoMain.BotClass import Bot
from Modules.Instanses.Bot_Instanse import BOT
from Modules.Database.tables import create_tables

create_tables()


@BOT.message_handler(commands=["start"])
def start_message(message):
    bot = Bot(message)
    bot.send("Для использования бота введите /reg [ключ активации]")


@BOT.message_handler(commands=["reg"])
def check_password(message):
    bot = Bot(message)
    bot.check_password()


@BOT.message_handler(content_types=["text"])
def reg_chat(message):
    bot = Bot(message)
    if bot.activated:
        bot.send("Тест (Здесь пока ничего нет)")


BOT.infinity_polling()
