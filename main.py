import discord
from discord.ext import commands
import os
import asyncio
from config import BOT_TOKEN, PREFIX
from keep_alive import app as keep_alive_app
import threading

intents = discord.Intents.default()
intents.message_content = True 
intents.guilds = True
bot = commands.Bot(command_prefix=PREFIX, intents = intents , case_insensitive=True, help_command=None)

from commands.user_commands import user_cmds
from commands.moderation import moderation_cmds
from commands.vc import vc_cmds
from commands.textchannel import text_cmds
from commands.help import help_cmds
from commands.ctoken import check
from commands.login import ready1

user_cmds(bot)
moderation_cmds(bot)
vc_cmds(bot)
text_cmds(bot)
help_cmds(bot)
check(bot)
ready1(bot)

status_messages = [
    "Helping with commands | &help",
    "Always here to assist | &help",
    "Making Discord a better place | &help",
    "Your friendly neighborhood bot | &help",
]

command_list = [f"{cmd.name} - {cmd.help}" for cmd in bot.commands if not cmd.hidden]
formatted_command_list = "\n".join(command_list)

@bot.event
async def on_ready():
    async def rotate_status():
        while True:
            for status in status_messages:
                await bot.change_presence(activity = discord.Game(status))
                await asyncio.sleep(30) # Change every 30 seconds

    print(f"Logged in as {bot.user}")
    for guild in bot.guilds:
        print(f" - {guild.name} (ID: {guild.id}) - {guild.member_count} members")

    bot.loop.create_task(rotate_status())

    print("Bot is ready!")

def run_keep_alive():
    keep_alive_app.run(host='0.0.0.0', port=8080)

threading.Thread(target=run_keep_alive, daemon=True).start()

bot.run(BOT_TOKEN)