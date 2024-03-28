from peewee import *

db = SqliteDatabase("database")


class BaseModel(Model):
    class Meta:
        database = db


class Chats(BaseModel):
    id = AutoField()
    telegram_id = IntegerField()
    key = CharField(max_length=16)
    activated = BooleanField()


class Themes(BaseModel):
    id = AutoField()
    theme = CharField(max_length=128)
    chat = ForeignKeyField(Chats, backref="themes")


def create_tables():
    with db:
        db.create_tables([
            Chats,
            Themes
        ])
