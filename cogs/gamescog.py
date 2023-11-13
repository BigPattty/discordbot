import discord
from discord.ext import commands
import json
import random

class GamesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = ['slots', 'coinflip']

    @commands.command(name='coinflip')
    async def coinflip(self, ctx, bet: int):
        user_id = str(ctx.author.id)
        balances = self.load_data('balances')

        if user_id not in balances:
            await ctx.send("You don't have a balance. Use the `!daily` command to get started.")
            return

        if balances[user_id] < bet or bet <= 0:
            await ctx.send("Invalid bet amount or insufficient funds.")
            return

        result = random.choice(['Heads', 'Tails'])
        if result == 'Heads':
            winnings = bet
            outcome = 'You won!'
        else:
            winnings = -bet
            outcome = 'You lost!'

        balances[user_id] += winnings
        self.save_data('balances', balances)

        embed = discord.Embed(title='Coin Flip', color=0x00ff00)
        embed.add_field(name='Result', value=result, inline=False)
        embed.add_field(name='Bet', value=f"${bet}", inline=False)
        embed.add_field(name='Outcome', value=outcome, inline=False)
        embed.add_field(name='Winnings', value=f"${winnings}", inline=False)
        embed.add_field(name='New Balance', value=f"${balances[user_id]}", inline=False)

        await ctx.send(embed=embed)

    @commands.command(name='slots')
    async def slots(self, ctx, bet: int):
        user_id = str(ctx.author.id)
        balances = self.load_data('balances')

        if user_id not in balances:
            await ctx.send("You don't have a balance. Use the `!daily` command to get started.")
            return

        if balances[user_id] < bet or bet <= 0:
            await ctx.send("Invalid bet amount or insufficient funds.")
            return

        symbols = ['🍇', '🍊', '🍋', '🍒', '🍉']
        result = [random.choice(symbols) for _ in range(3)]

        if result[0] == result[1] == result[2]:
            winnings = bet * 3
            outcome = 'You won!'
        else:
            winnings = -bet
            outcome = 'You lost!'

        balances[user_id] += winnings
        self.save_data('balances', balances)

        embed = discord.Embed(title='Slot Machine', color=0x00ff00)
        embed.add_field(name='Result', value=' '.join(result), inline=False)
        embed.add_field(name='Bet', value=f"${bet}", inline=False)
        embed.add_field(name='Outcome', value=outcome, inline=False)
        embed.add_field(name='Winnings', value=f"${winnings}", inline=False)
        embed.add_field(name='New Balance', value=f"${balances[user_id]}", inline=False)

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
    await bot.add_cog(GamesCog(bot))
