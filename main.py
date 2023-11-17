import discord
from discord.ext import commands
import os

intents = discord.Intents.all()

client = commands.Bot(commands.when_mentioned_or('$'), intents = intents, help_command = None)

class Dropdown(discord.ui.Select):
    def __init__(self, cog_names):
        self.cog_names = cog_names
        options = [discord.SelectOption(label = cog_name, value = f"cog_{cog_name}", description = f"{client.get_cog(cog_name).description}") for cog_name in cog_names]
        super().__init__(placeholder = "What happens if you click here?", max_values = 1, min_values = 1, options = options)
        
    async def callback(self, interaction = discord.Interaction):
        cog_names = self.values[0][4:]
        cog = client.get_cog(cog_name)
        if cog:
            embed = discord.Embed(title = "Help Menu", description = "If you click below, I might be able to dig up something for you!", color = 0x79FCBB)
            command_list = cog.get_commands()
            for command in command_list:
                embed.add_field(name = f"`${command_name}`", value = command.help or "Looks like I couldn't find a description for this command!", inline = False)
            await interaction.response.edit_message(embed = embed, view = DropView(self.cog_names))
            
class DropView(discord.ui.View):
    def __init__(self, cog_names, *, timeout = 180):
        super().__init__(timeout = timeout)
        self.cog_names = cog_names
        self.add_selmenu()
        
    def add_selmenu(self):
        self.add_item(DropMenu(self.cog_names))
        
@client.command()
async def help(ctx):
    cog_names = [cog_names for cog_name, cog in client.cog.items() if cog.get_commands()]
    
    if not cog_names:
        await ctx.send("Looks like I couldn't find any commands to put in this help menu! *Or TPK fucked up the code*")
        
    initial_embed = discord.Embed(title = "Help Menu", description = "If you click below, I might be able to dig some commands to help you out!", color = 0x79FCBB)
    
    await ctx.send(embed = initial_embed, view = DropView(cog_names))
    
@client.event
async def on_ready():
    print{'\n'"There you go, it connected *Surprisingly*")
    
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await client.load_extension(f"cogs.{filename[:-3]}")
                print(f"Look, you didnt fuck up this time with {filename}")
            except Exception as e:
                print(f"Looks like you fucked when I loaded {filename}, Here's what wrong: {e}")
                
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        print(f"{ctx.author.username} ran a command that doesn't exist. Dopey Cunt")

    else:
      	print(f"Nuh Uh: {error}")