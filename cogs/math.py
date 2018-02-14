import re
from discord.ext import commands

class Math:
    def __init__(self, bot):
        self.bot = bot
        self.pattern = re.compile(r"[\d\+-\/\*]+")

    @commands.command(description="returns the sum of an equation.",
                      aliases=["m"],
                      brief="equation")
    async def math(self, equation : str):
        #region SANITY

        if not self.pattern.match(equation):
            await self.bot.say("Invalid equation.")
            return

        #endregion

        try:
            await self.bot.say(eval(equation))
            return
        except Exception as e:
            await self.bot.say(str(e))

def setup(bot):
    bot.add_cog(Math(bot))
