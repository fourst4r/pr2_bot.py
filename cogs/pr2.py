import pr2hub
import discord
from discord.ext import commands

class PR2():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="returns player information")
    async def player_info(self, player_name : str):
        player = pr2hub.get_player_info(player_name)

        description = f"**Name:** {player.name}\n"
        description += f"**Status:** {player.status}\n"
        description += f"**Group:** {player.group}\n"
        description += f"**Guild:** {player.guild_name}\n"
        description += f"**Rank:** {player.rank}\n"
        description += f"**Hats:** {player.hats}\n"
        description += f"**Joined:** {player.register_date}\n"
        description += f"**Active:** {player.login_date}"

        embed = discord.Embed(title="-- Player Info --", description=description)
        await self.bot.say(embed=embed)

    @commands.command()
    async def roll(self, dice : str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await self.bot.say('Format has to be in NdN!')
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await self.bot.say(result)

    @commands.command(description='For when you wanna settle the score some other way')
    async def choose(self, *choices : str):
        """Chooses between multiple choices."""
        self.bot.say(random.choice(choices))


def setup(bot):
    bot.add_cog(PR2(bot))