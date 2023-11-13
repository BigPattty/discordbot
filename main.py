import discord
from discord.ext import commands
import os

intents = discord.Intents.all()

client = commands.Bot(command_prefix=commands.when_mentioned_or("$"), intents=intents, help_command=None)

class CommandSelectView(discord.ui.View):
    def __init__(self, cog_names, *, timeout=180):
        super().__init__(timeout=timeout)
        self.cog_names = cog_names
        self.add_buttons()  

    def add_buttons(self):
        self.add_item(CommandSelect(self.cog_names))

class CommandSelect(discord.ui.Select):
    def __init__(self, cog_names):
        self.cog_names = cog_names
        options = [discord.SelectOption(label=cog_name, value=f"cog_{cog_name}", description="Click here for more!") for cog_name in cog_names]
        super().__init__(placeholder="View my Commands!", max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        cog_name = self.values[0][4:]
        cog = client.get_cog(cog_name)
        if cog:
            embed = discord.Embed(
                title=f"Help Menu - {cog_name}",
                description=f"Commands available for {cog_name}",
                color=0x3498db
            )
            commands_list = cog.get_commands()
            for command in commands_list:
                embed.add_field(
                    name=f"**{command.name}**",
                    value=command.help or "No description provided",
                    inline=False
                )

            await interaction.response.edit_message(embed=embed, view=CommandSelectView(self.cog_names))

@client.command()
async def help(ctx):
    cog_names = [cog_name for cog_name, cog in client.cogs.items() if cog.get_commands()]

    if not cog_names:
        await ctx.send("No cogs with commands found.")
        return

    initial_embed = discord.Embed(
        title="Command Categories",
        description="Select a category to view commands",
        color=0x3498db
    )

    await ctx.send(embed=initial_embed, view=CommandSelectView(cog_names))

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} ({client.user.id})')
    
    
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await client.load_extension(f"cogs.{filename[:-3]}")
                print(f"Loaded {filename}")
            except Exception as e:
                print(f"Failed to load extension {filename}: {e}")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found.")

client.run("TOKEN")
