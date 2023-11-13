import discord
from discord.ext import commands
import brawlstats
import json

class BrawlStars(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.brawlstars = brawlstats.Client("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImZiZWYxY2EzLWViZjctNDdhOS04MzQ3LTdlOGYyMDYwY2M3ZSIsImlhdCI6MTY5OTU4ODAyOSwic3ViIjoiZGV2ZWxvcGVyLzg4NmY0MjNkLTJiMTEtMDU4NS01YWMyLWFhOGJmYTczMGMwZiIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMTAzLjExMS4zMy4xOTUiXSwidHlwZSI6ImNsaWVudCJ9XX0.swYB1syYSUJPB3xRaxPgi9fBgIY1dFPZUwhduuwPNqt8DkG1hgehhSe6Tx4jhqrKbWvSkP4de8yrqP0Cqt3Xbw")
        self.players_with_tag = self.load_players_with_tag()

    def load_players_with_tag(self):
        try:
            with open('data/players_with_tag.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_players_with_tag(self):
        with open('data/players_with_tag.json', 'w') as file:
            json.dump(self.players_with_tag, file)

    @commands.command(name="profile")
    async def user_profile_bs(self, ctx, player_tag=None):
        if player_tag is None:
            player_tag = self.players_with_tag.get(str(ctx.author.id))

            if player_tag is None:
                errorem = discord.Embed(title = "We have an issue!", description = "You seemed to have forgotten to mention a player tag or you don't have one saved! \n You can set one via `!savetag!", color = 0xFF0000)
                errorem.set_footer(text = "Brawl Stars Cog by ThePeaceKeeper")

                await ctx.send(embed = errorem)
                

        try:
            player_data = self.brawlstars.get_player(player_tag)

            profile_embed = discord.Embed(title=f"{player_data.name}'s Profile", color=0x79FCBB)
            profile_embed.add_field(name='\n'"Trophies", value=player_data.trophies, inline=False)
            profile_embed.add_field(name='\n'"Highest Trophies", value=player_data.highest_trophies, inline=False)
            profile_embed.add_field(name='\n'"Club Name", value=player_data.club.name, inline=False)
            profile_embed.add_field(name='\n'"3v3 Victories", value=player_data.x3vs3_victories, inline=False)

            if hasattr(player_data, 'power_league') and player_data.power_league is not None:
                profile_embed.add_field(name="\n **Power League:**", value=f"Power League Rank: {player_data.power_league.rank}\nHighest Power League Season: {player_data.power_league.season}", inline=False)
            else:
                profile_embed.add_field(name="\n **Power League:**", value="No Power League information available.", inline=False)

            await ctx.send(embed=profile_embed)

        except brawlstats.NotFoundError:
            not_found_embed = discord.Embed(title="Player Not Found", description="The specified player tag was not found.", color=0xFF0000)
            await ctx.send(embed=not_found_embed)

        except brawlstats.RequestError as e:
            request_error_embed = discord.Embed(title="API Error", description=f"An error occurred while fetching data from the Brawl Stars API:\n```{e}```", color=0xFF0000)
            await ctx.send(embed=request_error_embed)

    @commands.command(name="savetag")
    async def save_player_tag(self, ctx, tag=None):
        if tag is None:
            errorem = discord.Embed(title="We have an issue!", description="Unfortunately, my telepathic skills are slightly rusty, so I need you to supply me with your player tag. Soz!", color=0xFF0000)
            errorem.set_footer(text="Brawl Stars Cog by ThePeaceKeeper")
            await ctx.send(embed=errorem)
            return

        try:
            self.brawlstars.get_player(tag)
            self.players_with_tag[str(ctx.author.id)] = tag  # Use string format for user ID
            self.save_players_with_tag()

            tagem = discord.Embed(title="Success!", description=(f"I have saved **{tag}** for {ctx.author}!"), color=0x79FCBB)
            tagem.set_footer(text="Brawl Stars Cog by ThePeaceKeeper")
            await ctx.send(embed=tagem)

        except brawlstats.NotFoundError:
            errorem = discord.Embed(title="Nuh Uh!", description="Looks like that player tag isn't a real one. Check for spelling mistakes before trying again!", color=0xFF000)
            errorem.set_footer(text="Brawl Stars Cog by ThePeaceKeeper")
            await ctx.send(embed=errorem)

        except brawlstats.RequestError as e:
            errorem = discord.Embed(title="We have an API issue!", description=f"I got the following error from the Brawl Stars API: \n `{e}`", color=0xFF0000)
            errorem.set_footer(text="Brawl Stars Cog by ThePeaceKeeper")
            await ctx.send("<@1135757246337400882>", embed=errorem)

    @commands.command(name = "viewtag")
    async def view_player_tag(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        player_tag = self.players_with_tag.get(str(user.id), "not set")  # Use string format for user ID

        if player_tag == "not set":
            tagem = discord.Embed(title="No tags found!", description=f"{user} currently doesn't have a player tag set! \n One can be set via `!save_tag`!", color=0x79FCBB)
            tagem.set_footer(text="Brawl Stars Cog by ThePeaceKeeper")
            await ctx.send(embed=tagem)

        else:
            tagem = discord.Embed(title=f"One result found for {ctx.author.display_name}", description=f"Tag: {player_tag}", color=0x79FCBB)
            tagem.set_footer(text="Brawl Stars Cog by ThePeaceKeeper")
            await ctx.send(embed=tagem)

    # Additional commands can be added here...

async def setup(bot):
    await bot.add_cog(BrawlStars(bot))
