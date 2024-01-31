from discord.ext import commands
import discord


class MyClient(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)

    async def on_ready(self):
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, name="for images"
            )
        )
        print(f"Logged on as {self.user}!")

    async def on_message(self, message):
        await self.process_commands(message)  # Process commands in on_message
