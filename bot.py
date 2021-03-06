import settings
import discord
import pr2hub

from discord.ext import commands
from os import listdir
from os.path import isfile, join

description = '''A PR2 utility bot.'''

gog_hh_start_time = None
gog_hh_active = False

cogs_dir = "cogs"

bot = commands.Bot(command_prefix='!', description=description)
bot.remove_command("help")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    #bot.loop.create_task(check_gog_status())

@bot.command(pass_context=True)
async def help(ctx, command_name : str=None):
    if command_name == None:
        command_names = []
        for _,command in bot.commands.items():
            if command.name not in command_names:
                command_names.append(command.name)
        
        embed = discord.Embed(title="-- Command List --", description="\n".join(sorted(command_names)))
        embed.set_footer(text="try '!help <command>' for more info")
        await bot.send_message(ctx.message.author, embed=embed)
        #await bot.say(embed=embed)
    else:
        if command_name in bot.commands:
            command = bot.commands[command_name]
            aliases_str = ", ".join(command.aliases)

            description = f"**Name:** {command.name}\n"
            description += f"**Params:** {command.brief}\n"
            description += f"**Aliases:** {aliases_str}\n"
            description += f"**Description:** {command.description}"

            embed = discord.Embed(title="-- Command Info --", description=description)
            await bot.say(embed=embed)
        else:
            await bot.say("That command does not exist.")

def on_happy_hour(server : pr2hub.Server):
    if server.id != "148":
        return

    print("")

# async def check_gog_status():
#     while True:
#         servers = pr2hub.get_servers_info()
#         gog_server = next((x for x in servers if lambda s: s.id == "148"), None)

#         if gog_server != None:
#             if gog_server.is_happy_hour:
#                 if gog_hh_active:

#                 else:
                    

def main():
    for extension in [f.replace('.py', '') for f in listdir(cogs_dir) if isfile(join(cogs_dir, f))]:
        try:
            bot.load_extension(cogs_dir + "." + extension)
        except Exception:
            print(f'Failed to load extension {extension}.')
            #traceback.print_exc()

    bot.run(settings.token)

if __name__ == "__main__":
    main()