import logging
from typing import Dict

from discord import Intents
from discord.ext import commands

from src.Database import Database


class DiscordBot(commands.Bot):
    def __init__(self, database: Database, command_prefix, intents: Intents):
        commands.Bot.__init__(self, command_prefix=command_prefix, intents=intents)
        self.database = database
        self.remove_command("help")
        self.add_commands()
        self.active_users = []
        self.msg_loop = []

    def write_proxies(self):
        with open("proxies.txt", "r") as f:
            line = f.readline()
            while line:
                if line.endswith("\r\n"):
                    line = line[:-2]
                if line.endswith("\n") or line.endswith("\r"):
                    line = line[:-1]
                split = line.split(":")
                ip = split[0]
                port = split[1]
                username = split[2]
                password = split[3]
                self.database.add_proxy(ip, port, username, password)
                line = f.readline()
        self.database.assign_proxy_to_users()

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
            self.database.add_user(member.id, member.name)
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
            if consigne[0:49] != "https://sell.wethenew.com/fr/consignment/product/":
                await ctx.send("Lien invalide")
            else:
                num_product = consigne[49:]
                self.database.add_consigne(ctx.author.id, consigne, num_product)
                await ctx.send("Consigne ajoutée")

        @self.command(pass_context=True)
        async def remove_consigne(ctx, consigne):
            if consigne[0:49] != "https://sell.wethenew.com/fr/consignment/product/":
                await ctx.send("Lien invalide")
            else:
                if not self.database.get_consigne(ctx.author.id, consigne):
                    await ctx.send("Consigne inexistante")
                else:
                    self.database.remove_consigne(ctx.author.id, consigne)
                    await ctx.send("Consigne supprimée")

        @self.command(pass_context=True)
        async def addproxies(ctx):
            if ctx.guild is None and ctx.author.id == 218810179590815744:
                await ctx.send("Please send your proxies list")
                response = await self.wait_for("message", check=lambda message: message.author == ctx.author)
                await response.attachments[0].save("proxies.txt")
                self.database.remove_all_proxy()
                self.write_proxies()
                await ctx.send("Proxies list successfully added")

        @self.command(pass_context=True)
        async def start(ctx):
            user_id = ctx.author.id
            if not self.database.get_user(user_id):
                await ctx.send("You don't have the permission to do this.")
            else:
                if user_id in self.active_users:
                    await ctx.send("Bot already started!")
                else:
                    self.active_users.append(user_id)
                    logging.info(f"Added {user_id} to active users")
                    await ctx.send("Bot started!")
