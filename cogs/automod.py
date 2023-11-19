import discord
from discord.ext import commands
import json

class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.automod_settings = {}  # Dictionary to store automod settings for each server
        self.modlog_channels = {}  # Dictionary to store modlog channels for each server
        self.load_settings()

    def load_settings(self):
        try:
            with open('data/automod_settings.json', 'r') as file:
                self.automod_settings = json.load(file)
        except FileNotFoundError:
            pass

        try:
            with open('data/modlog_channels.json', 'r') as file:
                modlog_channels_data = json.load(file)
                # Convert channel IDs back to TextChannel objects
                self.modlog_channels = {int(guild_id): self.bot.get_channel(int(channel_id)) for guild_id, channel_id in modlog_channels_data.items()}
        except FileNotFoundError:
            pass

    def save_settings(self):
        with open('data/automod_settings.json', 'w') as file:
            json.dump(self.automod_settings, file, indent=2)

        # Convert TextChannel objects to their IDs for serialization
        modlog_channels_data = {str(guild_id): str(channel.id) for guild_id, channel in self.modlog_channels.items()}
        with open('data/modlog_channels.json', 'w') as file:
            json.dump(modlog_channels_data, file, indent=2)

    def get_modlog_channel(self, guild):
        return self.modlog_channels.get(guild.id)

    async def log_to_modlog(self, guild, message):
        modlog_channel = self.get_modlog_channel(guild)
        if modlog_channel:
            embed = discord.Embed(title="Moderation Log", description=message, color=discord.Color.red())
            await modlog_channel.send(embed=embed)

    @commands.command(name="setautomod")
    @commands.has_permissions(manage_guild=True)
    async def set_automod(self, ctx, censor_words: str = "", max_mentions: int = 5):
        """
        Set up automod rules.

        Parameters:
        `censor_words (str)`: Comma-separated list of words to be censored.
        
        `max_mentions (int)`: Maximum number of mentions allowed in a message (default is 5).
        """'\n'
        if not censor_words:
            embed = discord.Embed(
                title="Set Automod",
                description="Configure the automod settings for the server.\n\n"
                            "**Usage:**\n"
                            "`$setautomod word1,word2,... [max_mentions]`\n\n"
                            "**Example:**\n"
                            "`$setautomod badword1,badword2 3`",
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
            return

        # Convert censor_words to a list
        censor_list = [word.strip() for word in censor_words.split(',')]

        # Save automod settings for the server
        self.automod_settings[ctx.guild.id] = {"censor_words": censor_list, "max_mentions": max_mentions}
        self.save_settings()

        embed = discord.Embed(
            title="Automod Settings Updated",
            description="Automod settings have been updated successfully.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.command(name="setmodlog")
    @commands.has_permissions(manage_guild=True)
    async def set_modlog(self, ctx, modlog_channel: discord.TextChannel = None):
        """
        Set the modlog channel for logging incidents.

        Parameters:
        modlog_channel (discord.TextChannel): The channel to log incidents.
        """
        if not modlog_channel:
            embed = discord.Embed(
                title="Set Modlog",
                description="Set the modlog channel for logging incidents.\n\n"
                            "**Usage:**\n"
                            "`$setmodlog #modlog-channel`\n\n"
                            "**Example:**\n"
                            "`$setmodlog #mod-log`",
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
            return

        self.modlog_channels[ctx.guild.id] = modlog_channel
        self.save_settings()

        embed = discord.Embed(
            title="Modlog Channel Set",
            description=f"Modlog channel set to {modlog_channel.mention}.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore messages from bots
        if message.author.bot:
            return

        # Check if automod is enabled for the server
        if message.guild.id in self.automod_settings:
            automod_config = self.automod_settings[message.guild.id]

            # Check for censor words
            for word in automod_config["censor_words"]:
                if word.lower() in message.content.lower():
                    await message.delete()
                    await self.log_to_modlog(message.guild, f"{message.author.mention}'s message was deleted due to a censor word.")
                    return

            # Check for excessive mentions
            if len(message.mentions) > automod_config["max_mentions"]:
                await message.delete()
                await self.log_to_modlog(message.guild, f"{message.author.mention}'s message was deleted due to excessive mentions.")
                return

async def setup(bot):
    await bot.add_cog(AutoMod(bot))