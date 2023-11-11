#importing modules for discord.py
import discord
from discord.ext import commands

intents = discord.Intents.all()

bot = commands.Bot(command_prefix = commands.when_mentioned_or("$"), intents = intents, help_command = None)


#loading files from the file "cogs"
async def load_cogs():
    try:
        await bot.load_extension("cogs.help")
        print("\n"'All cogs have loaded successfully!')
    except Exception as e:
        print('\n'f"Issue loading cogs: '\n' *** {e} ***")

@bot.event
async def on_ready():
        print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')

        await load_cogs()

        


bot.run('BOT_TOKEN')
