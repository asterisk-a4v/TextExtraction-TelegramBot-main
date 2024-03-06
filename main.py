from telegram.ext import ApplicationBuilder
from json import load 

from src.utils.logger import Logger
from src.core.app import App

with open("config.json", "r") as config_file:
    config = load(config_file)
if __name__ == '__main__':
    Logger().setup()
    
    App(
        ApplicationBuilder()
        .token(config["bot_token"])         
        .build()
        ).run()
