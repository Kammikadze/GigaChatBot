import telebot.types

from Modules.Database.tables import Chats
from Modules.Instanses.Bot_Instanse import BOT


class Bot:
    def __init__(self, message: telebot.types.Message):
        self.message: telebot.types.Message = message

        self.chat_id: int = message.chat.id
        self.text = message.text

        self.add_chat_to_database()

    def send(
            self,
            text: str,
            parse: bool = False,
            protect: bool = False,
    ) -> None:
        """
        Отправляет новое сообщение в указанный чат
        :param text: Текст сообщения
        :param parse: Форматировать текст
        :param protect: Защитить сообщение от копирования и пересылки
        """
        BOT.send_message(
            chat_id=self.chat_id,
            text=text,
            parse_mode="HTML" if parse else None,
            protect_content=protect,
            disable_web_page_preview=True
        )

    def extract(
            self,
            cut: int,
            split: str | None = None
    ) -> str | list[str]:
        data: str = telebot.util.extract_arguments(self.text)[cut:]
        if split:
            return data.split(split)
        return data

    def check_password(self) -> None:
        password = self.extract(cut=0)
        chat: Chats = Chats.get(telegram_id=self.chat_id)
        real_password = chat.key
        if password != real_password:
            chat.key = self.generate_token()
            Chats.save(chat)
            self.send("Вы ввели неправильный ключ активации! Для безопасности он был сменен.")
            return
        chat.activated = True
        Chats.save(chat)
        self.send("Чат активирован!")

    def add_chat_to_database(self):
        if Chats.select().where(Chats.telegram_id == self.chat_id)[:]:
            return
        Chats.create(
            telegram_id=self.chat_id,
            key=self.generate_token(),
            activated=False
        )

    @staticmethod
    def generate_token() -> str:
        return telebot.util.generate_random_token()

    @property
    def activated(self) -> bool:
        return Chats.get(telegram_id=self.chat_id).activated
