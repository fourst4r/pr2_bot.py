import pr2hub
import discord
from discord.ext import commands
from cogs.utils import exp

class PR2():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="returns player information", 
                      aliases=["pi", "view"])
    async def player_info(self, player_name : str):
        #region SANITY

        if len(player_name) > 20:
            await self.bot.say("Parameter too long: `player_name`")
            return

        #endregion

        player = None

        try:
            player = pr2hub.get_player_info(player_name)
        except pr2hub.PR2HubError as e:
            await self.bot.say(str(e))
            return

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

    @commands.command(description="returns guild information",
                      aliases=["gi", "guild"])
    async def guild_info(self, *, guild_name : str):
        #region SANITY

        if len(guild_name) > 20:
            await self.bot.say("Parameter too long: `guild_name`")
            return

        #endregion

        guild = None

        try:
            guild = pr2hub.get_guild_info(guild_name, False)
        except pr2hub.PR2HubError as e:
            await self.bot.say(str(e))
            return

        description = f"**Name:** {guild.name}\n"
        description += "**GP Today:** {:,}\n".format(int(guild.gp_today))
        description += "**GP Total:** {:,}\n".format(int(guild.gp_total))
        description += f"**Members:** {guild.member_count} ({guild.active_count} active)\n"
        description += f"**Creation Date:** {guild.creation_date}\n"
        description += f"**Prose:** {guild.note}"

        embed = discord.Embed(title="-- Guild Info --", description=description)
        await self.bot.say(embed=embed)

    @commands.command(description="returns the names of all members in a guild",
                      aliases=["gm", "guildm"])
    async def guild_members(self, *, guild_name : str):
        #region SANITY

        if len(guild_name) > 20:
            await self.bot.say("Parameter too long: `guild_name`")
            return

        #endregion
        
        guild = None

        try:
            guild = pr2hub.get_guild_info(guild_name, True)
        except pr2hub.PR2HubError as e:
            await self.bot.say(str(e))
            return

        member_count_is_even = guild.member_count % 2 == 0
        half_member_count = int(guild.member_count / 2)
        guild_member_names = []
        value1 = []
        value2 = []

        # create a list of just the member names
        for member in guild.members:
            guild_member_names.append(member.name)

        if member_count_is_even:
            value1 = guild_member_names[:half_member_count]
            value2 = guild_member_names[half_member_count:half_member_count*2]
        else:
            value1 = guild_member_names[:half_member_count+1]
            value2 = guild_member_names[half_member_count+1:half_member_count*2+1]

        embed = discord.Embed(title=f"-- Guild Members ({guild.member_count}) --")
        embed.add_field(name="1", value="\n".join(value1), inline=True)
        if guild.member_count > 1:
            embed.add_field(name="2", value="\n".join(value2), inline=True)

        await self.bot.say(embed=embed)

    @commands.command(description="calculates experience required to reach a specified rank",
                      aliases=["xp"])
    async def exp(self, _from : int, to : int=None, exp_per_day=700):
        if to == None:
            to = _from + 1

        #region SANITY

        if _from > 1000 or _from < 0:
            await self.bot.say("Parameter out of range: `from`")
            return

        if to > 1000 or to < 0:
            await self.bot.say("Parameter out of range: `to`")
            return

        if exp_per_day > 10000 or exp_per_day < 0:
            await self.bot.say("Parameter out of range: `exp_per_day`")
            return

        #endregion

        _exp = exp.calculate(_from, to)
        days = int(_exp/(exp_per_day*1000))
        _exp = "{:,}".format(_exp)

        embed = discord.Embed(title="-- Experience Needed --", 
                              description=f"{_from} -> {to} = {_exp}\nroughly {days} days")
        await self.bot.say(embed=embed)

    @commands.command(description="returns info of every server",
                      aliases=["hh", "status"])
    async def server_info(self):
        servers = None

        try:
            servers = pr2hub.get_servers_info()
        except pr2hub.PR2HubError as e:
            await self.bot.say(str(e))
            return

        description = ""

        for server in servers:
            line = ""
            line += server.name

            if server.status == "down":
                line += " (down)"
            else:
                line += f" ({server.population} online)"

            if server.is_happy_hour:
                line = f"**!! {line}**"

            line += "\n"
            description += line

        embed = discord.Embed(title="-- Server Info --", description=description)
        await self.bot.say(embed=embed)



def setup(bot):
    bot.add_cog(PR2(bot))