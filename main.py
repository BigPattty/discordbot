import discord
from discord.ext import commands


intents = discord.Intents.all()

bot = commands.Bot(command_prefix = "/", intents = intents)



async def load_cogs():
    try:
        await bot.load_extension("cogs.economycog")
        #await bot.load_extension("")
        print("\n"'All cogs have loaded successfully!')
    except Exception as e:
        print('\n'f"The following error occured when loading cogs: {e}")

@bot.event
async def on_ready():
        print("\n"'Test Bot has connected to Discord!')

        await load_cogs()

        


bot.run('BOT_TOKEN')
