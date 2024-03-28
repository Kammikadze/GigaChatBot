import schedule
import telebot.types

from Modules.DoMain.BotClass import Bot


class WriteAndSendPost:
    def __init__(self, message: telebot.types.Message):
        self.bot: Bot = Bot(message)
        self.stop_script: bool = False

    def create_time_line(self, time: list[str]):
        for t in time:
            schedule.every().day.at(t).do(self.bot.send("-"))

    def work_const(self):
        while True:
            if self.stop_script:
                break
            schedule.run_pending()
