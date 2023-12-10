import discord
from discord.ext import commands
from discord import app_commands
import random

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.balance_file = 'balances.txt'

    async def get_balance(self, user_id):
        """Get the balance of a user."""
        with open(self.balance_file, 'r') as file:
            for line in file:
                user, balance = line.split(':')
                if int(user) == user_id:
                    return int(balance)
        return 0

    async def update_balance(self, user_id, amount):
        """Update the balance of a user."""
        balances = {}
        with open(self.balance_file, 'r') as file:
            for line in file:
                user, balance = line.split(':')
                balances[int(user)] = int(balance)
        
        balances[user_id] = balances.get(user_id, 0) + amount

        with open(self.balance_file, 'w') as file:
            for user, balance in balances.items():
                file.write(f'{user}:{balance}\n')

    async def balance_embed(self, user_id):
        """Create an embed for the user's balance."""
        balance = await self.get_balance(user_id)
        embed = discord.Embed(title="Wallet", description=f"Your balance is {balance} coins.", color=0x00ff00)
        return embed

    @discord.app_commands.command(name='balance')
    async def balance(self, interaction: discord.Interaction, user: discord.User = None):
        """Show the user's balance."""
        user_id = user.id if user else interaction.user.id
        embed = await self.balance_embed(user_id)
        await interaction.response.send_message(embed=embed)

    @discord.app_commands.command(name='pay')
    async def pay(self, interaction: discord.Interaction, user: discord.User, amount: int):
        """Transfer coins to another user."""
        giver_id = interaction.user.id
        receiver_id = user.id

        if giver_id == receiver_id:
            return await interaction.response.send_message("You cannot pay yourself.", ephemeral=True)

        if amount <= 0:
            return await interaction.response.send_message("Please enter a valid amount.", ephemeral=True)

        giver_balance = await self.get_balance(giver_id)
        if amount > giver_balance:
            return await interaction.response.send_message("You do not have enough coins.", ephemeral=True)

        await self.update_balance(giver_id, -amount)
        await self.update_balance(receiver_id, amount)

        message = f"You have successfully paid {amount} coins to {user.display_name}."
        await interaction.response.send_message(message)

    @discord.app_commands.command(name='work')
    async def work(self, interaction: discord.Interaction):
        """Earn coins by working."""
        user_id = interaction.user.id
        earnings = random.randint(10, 100)  # Random earnings between 10 and 100 coins
        await self.update_balance(user_id, earnings)
        message = f"You worked hard and earned {earnings} coins!"
        await interaction.response.send_message(message)

    @discord.app_commands.command(name='steal')
    async def steal(self, interaction: discord.Interaction, user: discord.User):
        """Attempt to steal coins from another user."""
        thief_id = interaction.user.id
        victim_id = user.id

        if thief_id == victim_id:
            return await interaction.response.send_message("You cannot steal from yourself.", ephemeral=True)

        success_chance = random.randint(1, 100)
        if success_chance <= 30:  # 30% success rate
            stolen_amount = random.randint(10, 50)
            victim_balance = await self.get_balance(victim_id)

            if stolen_amount > victim_balance:
                stolen_amount = victim_balance

            await self.update_balance(thief_id, stolen_amount)
            await self.update_balance(victim_id, -stolen_amount)
            message = f"You successfully stole {stolen_amount} coins from {user.display_name}."
        else:
            message = "Your attempt to steal was unsuccessful."

        await interaction.response.send_message(message)

    @discord.app_commands.command(name='slots')
    async def slots(self, interaction: discord.Interaction, bet: int):
        """Slot machine game with a 2x multiplier."""
        user_id = interaction.user.id
        balance = await self.get_balance(user_id)

        if bet > balance:
            return await interaction.response.send_message("You don't have enough coins to bet that much.", ephemeral=True)
        
        # Simple slot machine logic
        result = random.choices(["🍒", "🍋", "🔔"], k=3)
        await self.update_balance(user_id, -bet)
        if result[0] == result[1] == result[2]:
            win_amount = bet * 2  # 2x multiplier
            await self.update_balance(user_id, win_amount)
            message = f"You won {win_amount} coins!\n{' '.join(result)}"
        else:
            message = f"You lost {bet} coins.\n{' '.join(result)}"

        embed = await self.balance_embed(user_id)
        embed.add_field(name="Slot Result", value=message, inline=False)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Economy(bot))