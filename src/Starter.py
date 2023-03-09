import os

import discord
from dotenv import load_dotenv

from src import get_project_root
from src.ConsigneBot import ConsigneBot
from src.Database import Database
from src.DiscordBot import DiscordBot


class Starter:
    def __init__(self):
        dotenv_path = os.path.join(get_project_root(), ".env")
        load_dotenv(dotenv_path=dotenv_path)
        options = ["COMMAND_PREFIX", "DATABASE_NAME", "DISCORD_BOT_TOKEN"]
        self.options = {}
        for option in options:
            self.options[option] = os.getenv(option)
        database_path = os.path.join(get_project_root(), self.options["DATABASE_NAME"])
        self.database = Database(database_path=database_path)
        self.discord_bot = DiscordBot(database=self.database, command_prefix=self.options["COMMAND_PREFIX"], intents=discord.Intents.all())
        self.consigne_bot = ConsigneBot(discord_bot=self.discord_bot, database=self.database)

    def start(self):
        self.consigne_bot.start()
        self.discord_bot.run(self.options["DISCORD_BOT_TOKEN"])

