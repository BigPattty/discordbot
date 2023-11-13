import discord
from discord.ext import commands
import json
import random
from datetime import datetime, timedelta

class Balance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.daily_cooldown = commands.CooldownMapping.from_cooldown(1, 24 * 60 * 60, commands.BucketType.user)
        self.payday_cooldown = commands.CooldownMapping.from_cooldown(1, 5 * 60, commands.BucketType.user)

    @commands.command(name='balance', help = "See your balance in this server!")
    async def balance(self, ctx):
        user_id = str(ctx.author.id)
        balances = self.load_data('balances')

        if user_id not in balances:
            balances[user_id] = 0

        embed = discord.Embed(
            title = f"{ctx.author.display_name}'s Balance",
            description = f'**Balance:** {balances[user_id]} credits',
            color = 0x79FCBB)

        await ctx.send(embed=embed)

    @commands.command(name='daily', help = "Collect a nice helping of cash, but only every 24h!")
    @commands.cooldown(1, 24 * 60 * 60, commands.BucketType.user)
    async def daily(self, ctx):
        user_id = str(ctx.author.id)
        balances = self.load_data('balances')

        if user_id not in balances:
            balances[user_id] = 0

        amount = random.randint(1000, 5000)
        balances[user_id] += amount
        self.save_data('balances', balances)

        embed = discord.Embed(
            title = 'Daily Reward!',
            description = f'You got paid {amount} credits for your hard days work!\nYou balance is now {balances[user_id]}',
            color = 0x79FCBB)

        await ctx.send(embed=embed)

    @commands.command(name='payday', help = "Get that money you deserve after all that hard work!")
    @commands.cooldown(1, 5 * 60, commands.BucketType.user)
    async def payday(self, ctx):
        user_id = str(ctx.author.id)
        balances = self.load_data('balances')

        if user_id not in balances:
            balances[user_id] = 0

        amount = random.randint(100, 500)
        balances[user_id] += amount
        self.save_data('balances', balances)

        embed = discord.Embed(
            title = 'Payday!',
            description = f'You got paid {amount} credits for your hard days work!\nYou balance is now {balances[user_id]}',
            color = 0x79FCBB)

        await ctx.send(embed=embed)

    def load_data(self, filename):
        try:
            with open(f'data/balances.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_data(self, filename, data):
        with open(f'data/balances.json', 'w') as f:
            json.dump(data, f, indent=4)

async def setup(bot):
    await bot.add_cog(Balance(bot))
