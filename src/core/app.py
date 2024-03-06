from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, MessageReactionHandler
from ..command.start import startCommand_handler
from ..command.help import helpCommand_handler

from ..message.image import imageMessage_handler


class App:
    def __init__(self, telebot: Application) -> None:
        self.telebot = telebot

    def run(self):

        self.telebot.add_handler(startCommand_handler)
        self.telebot.add_handler(helpCommand_handler)

        self.telebot.add_handler(imageMessage_handler)

        self.telebot.run_polling(allowed_updates=Update.ALL_TYPES)