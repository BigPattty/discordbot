import discord
from discord.ext import commands
import json

class ShopCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='shop')
    async def shop(self, ctx):
        items = {
            'item1': {'name': 'Item 1', 'price': 50},
            'item2': {'name': 'Item 2', 'price': 100},
            # Add more items as needed
        }

        embed = discord.Embed(title='Shop', color=0x00ff00)

        for item_id, item_info in items.items():
            embed.add_field(name=item_info['name'], value=f"Price: ${item_info['price']}", inline=False)

        await ctx.send(embed=embed)

    @commands.command(name='buy')
    async def buy(self, ctx, item_id):
        user_id = str(ctx.author.id)
        balances = self.load_data('balances')
        items = self.load_data('items')

        if user_id not in balances:
            balances[user_id] = 0

        if user_id not in items:
            items[user_id] = []

        if item_id not in items[user_id]:
            shop_items = {
                'item1': {'name': 'Item 1', 'price': 50},
                'item2': {'name': 'Item 2', 'price': 100},
                # Add more items as needed
            }

            if item_id in shop_items:
                if balances[user_id] >= shop_items[item_id]['price']:
                    balances[user_id] -= shop_items[item_id]['price']
                    items[user_id].append(item_id)

                    self.save_data('balances', balances)
                    self.save_data('items', items)

                    embed = discord.Embed(title='Purchase Successful', color=0x00ff00)
                    embed.add_field(name='User', value=ctx.author.display_name, inline=True)
                    embed.add_field(name='Item Purchased', value=shop_items[item_id]['name'], inline=True)
                    embed.add_field(name='New Balance', value=f"${balances[user_id]}", inline=True)

                    await ctx.send(embed=embed)
                else:
                    await ctx.send("Insufficient funds to purchase this item.")
            else:
                await ctx.send("Invalid item ID.")
        else:
            await ctx.send("You already own this item.")

    def load_data(self, filename):
        try:
            with open(f'data/items.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_data(self, filename, data):
        with open(f'data/items.json', 'w') as f:
            json.dump(data, f, indent=4)

async def setup(bot):
    await bot.add_cog(ShopCog(bot))
