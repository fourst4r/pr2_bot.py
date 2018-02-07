import pr2hub
import discord
from discord.ext import commands

class PR2():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="returns player information", 
                      aliases=["pi", "view"])
    async def player_info(self, player_name : str):
        if len(player_name) > 20:
            await self.bot.say("Parameter too long: `player_name`")
            return

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
        if len(guild_name) > 20:
            await self.bot.say("Parameter too long: `guild_name`")
            return

        guild = None

        try:
            guild = pr2hub.get_guild_info(guild_name, False)
        except pr2hub.PR2HubError as e:
            await self.bot.say(str(e))
            return

        description = f"**Name:** {guild.name}\n"
        description += f"**GP Today:** {guild.gp_today}\n"
        description += f"**GP Total:** {guild.gp_total}\n"
        description += f"**Members:** {guild.member_count} ({guild.active_count} active)\n"
        description += f"**Creation Date:** {guild.creation_date}\n"
        description += f"**Prose:** {guild.note}"

        embed = discord.Embed(title="-- Guild Info --", description=description)
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