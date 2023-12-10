import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View, Button
from flask import Flask, jsonify
import threading
import os
from datetime import datetime

# Discord Bot Setup
intents = discord.Intents.all()
client = commands.Bot(commands.when_mentioned_or('$'), intents=intents, help_command=None)

# Flask App Setup
app = Flask(__name__)

@app.route('/ping')
def ping_check():
    return jsonify(status="up"), 200

def run_flask():
    app.run(host='0.0.0.0', port=5000)

# Update this timestamp on each restart
last_restart = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

def create_home_embed():
    embed = discord.Embed(
        title='Bob Help Menu - Home',
        description="Need Help? You've come to the right place!",
        color=discord.Color.green())
    embed.add_field(name="Last Help Menu Update:",
                    value=last_restart,
                    inline=False)
    embed.add_field(name="Can't find what you're looking for?",
                    value="[Join our support server!](discord_link)",
                    inline=False)
    embed.set_footer(text="Thanks for using Bob!")
    return embed

@client.tree.command(name='help', description='Need help? Use this command!')
async def help_menu(interaction: discord.Interaction):
    cogs = [c for c in client.cogs.keys()]
    pages = ['Home Page'] + cogs
    current_page = 0

    def create_embed(page):
        if page == 'Home Page':
            return create_home_embed()
        else:
            cog = client.get_cog(page)
            embed = discord.Embed(title=f'Bob Help Menu - {cog.qualified_name}', color=discord.Color.green())
            for command in cog.get_commands():
                embed.add_field(name=command.name, value=command.help or "No description", inline=False)
            embed.set_footer(text='Thanks for using Bob!')
            return embed

    def create_view(current_page):
        view = View()

        # Back button
        back_button = Button(label="Back", style=discord.ButtonStyle.secondary, disabled=(current_page <= 0))
        async def back_callback(interaction):
            nonlocal current_page
            current_page = max(0, current_page - 1)
            await interaction.response.edit_message(content="", embed=create_embed(pages[current_page]), view=create_view(current_page))
        back_button.callback = back_callback
        view.add_item(back_button)

        # Home button
        home_button = Button(label="Home", style=discord.ButtonStyle.primary, disabled=(current_page == 0))
        async def home_callback(interaction):
            nonlocal current_page
            current_page = 0
            await interaction.response.edit_message(content="", embed=create_home_embed(), view=create_view(current_page))
        home_button.callback = home_callback
        view.add_item(home_button)

        # Forward button
        forward_button = Button(label="Forward", style=discord.ButtonStyle.primary, disabled=(current_page >= len(pages) - 1))
        async def forward_callback(interaction):
            nonlocal current_page
            current_page = min(len(pages) - 1, current_page + 1)
            await interaction.response.edit_message(content="", embed=create_embed(pages[current_page]), view=create_view(current_page))
        forward_button.callback = forward_callback
        view.add_item(forward_button)

        return view

    await interaction.response.send_message(embed=create_embed(pages[current_page]), view=create_view(current_page))

@client.event
async def on_ready():
    guilds = [guild for guild in client.guilds]
    for guild in guilds:
        await client.tree.sync(guild=discord.Object(id=guild.id))
    print(f"Connected to Discord! Bot: {client.user}")
    
    for filenane in os.listdir('./cogs'):
        if filename.endswith('.py'):
            cog = filename[:-3]
            await bot.load_extension(f'cogs.{cog}')
            print(f'Loaded: {cog}')

@client.event
async def on_guild_join(guild):
    await client.tree.sync(guild=discord.Object(id=guild.id))

if __name__ == "__main__":
    # Start Flask app in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Start Discord bot
    client.run('YOUR_BOT_TOKEN')