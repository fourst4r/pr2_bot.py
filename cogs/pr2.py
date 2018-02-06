import pr2hub
from discord.ext import commands

class PR2():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='returns player information')
    async def player_info(self, player_name : str):
        player = pr2hub.get_player_info(player_name)
        await self.bot.say(player.name)

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