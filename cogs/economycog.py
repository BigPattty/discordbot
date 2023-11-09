import discord
from discord.ext import commands
import json
import random

class EconomyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.balances = self.read_balances()

    # Read user balances from the JSON file
    def read_balances(self):
        try:
            with open('cogs/balances.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    # Save user balances back to the JSON file
    def save_balances(self):
        with open('cogs/balances.json', 'w') as file:
            json.dump(self.balances, file)

    @commands.command()
    @commands.cooldown(1, 300, commands.BucketType.user)  # 300 seconds cooldown (5 minutes)
    async def payday(self, ctx):
        user_id = str(ctx.author.id)  # Convert user_id to string for use as a dictionary key
        
        # Implement payday logic here (randomized reward)
        reward = random.randint(500, 2000)  # Random reward between 50 and 200 coins
        self.balances[user_id] = self.balances.get(user_id, 0) + reward
        self.save_balances()
        payem = discord.Embed(
            title = "Money Money Money!!",
            description = f'You got paid {reward} credits!\nYour balance is now {self.balances.get(user.id, 0)}',
            color = 0x79FCBB)
        payem.set_footer(text = "Bot made by ThePeaceKeeper")

        await ctx.send(embed = payem)        

async def setup(bot):
    await bot.add_cog(EconomyCog(bot))
