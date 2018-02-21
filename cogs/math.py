import re
from cogs.utils import exp
from discord.ext import commands

class Math:
    def __init__(self, bot):
        self.bot = bot
        self.equation_pattern = re.compile(r"[\d\+-\/\*\.]+")

    @commands.command(description="returns the sum of an equation.",
                      aliases=["m"],
                      brief="equation")
    async def math(self, equation : str):
        #region SANITY

        if not self.equation_pattern.match(equation):
            await self.bot.say("Invalid equation.")
            return

        #endregion

        try:
            await self.bot.say(eval(equation))
            return
        except Exception as e:
            await self.bot.say(str(e))
            return
    
    # @math.error
    # async def do_repeat_handler(self, ctx, error):
    #     if isinstance(error, commands.MissingRequiredArgument):
    #         if error.param == 'inp':
    #             await ctx.send("You forgot to give me input to repeat!")

    # per jmar's request ?
    @commands.command(description="returns the sum of the required exp for the specified ranks",
                      aliases=[],
                      brief="*ranks")
    async def exp_add(self, *arg : int):
        #region SANITY

        if len(arg) == 0:
            await self.bot.say("Too few ranks.")
            return

        if len(arg) > 10:
            await self.bot.say("Okay settle down...")
            return

        #endregion

        sum = 0
        for n in list(arg):
            if n < 0 or n > 1000:
                await self.bot.say(f"Parameter out of range: *ranks ({n})")
                return
            sum += exp.calculate(n, n+1)

        await self.bot.say(sum)

        


def setup(bot):
    bot.add_cog(Math(bot))
