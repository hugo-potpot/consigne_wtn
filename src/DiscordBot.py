import discord
from discord import Intents
from discord.ext import commands

from src.Database import Database


class DiscordBot(commands.Bot):
    def __init__(self, database: Database, command_prefix, intents: Intents):
        commands.Bot.__init__(self, command_prefix=command_prefix, intents=intents)
        self.database = database
        self.remove_command("help")
        self.add_commands()
        self.msg_loop = []


    async def on_ready(self):
        print("Bot is ready")
        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} commands")
        except Exception as e:
            print(e)

    def add_commands(self):
        @self.event
        async def on_member_join(member):
            self.database.add_user(member.id, member.name, 0)
            print(f"New user: {member.name} ({member.id})")

        @self.event
        async def on_member_remove(member):
            self.database.remove_user(member.id)
            print(f"User left: {member.name} ({member.id})")

        @self.event
        async def on_message(message):
            if not self.database.get_user(message.author.id):
                return
            else:
                if message.content.startswith("!"):
                    await self.process_commands(message)

        @self.command(pass_context=True)
        async def add_consigne(ctx, consigne):
            print(len(consigne))
            if consigne[0:49] != "https://sell.wethenew.com/fr/consignment/product/":
                await ctx.send("Lien invalide")
            else:
                self.database.add_consigne(ctx.author.id, consigne)
                await ctx.send("Consigne ajoutée")



