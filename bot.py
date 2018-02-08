import settings
import inspect
import discord
from discord.ext import commands
from os import listdir
from os.path import isfile, join

description = '''A PR2 utility bot.'''

# this specifies what extensions to load when the bot starts up (from this directory)
cogs_dir = "cogs"

bot = commands.Bot(command_prefix='!', description=description)
bot.remove_command("help")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def help(command_name : str=None):
    if command_name == None:
        command_names = []
        for _,command in bot.commands.items():
            if command.name not in command_names:
                command_names.append(command.name)
        
        embed = discord.Embed(title="-- Command List --", description="\n".join(command_names))
        await bot.say(embed=embed)
    else:
        if command_name in bot.commands:
            command = bot.commands[command_name]
            aliases_str = ", ".join(command.aliases)
            params_str = get_params_str(command)

            description = f"**Name:** {command.name}\n"
            description += f"**Params:** {params_str}\n"
            description += f"**Aliases:** {aliases_str}\n"
            description += f"**Description:** {command.description}"

            embed = discord.Embed(title="-- Command Info --", description=description)
            embed.set_footer(text="try '!help <command>' for more info")
            await bot.say(embed=embed)
        else:
            await bot.say("That command does not exist.")

def get_params_str(command):
        func = inspect.signature(eval(command.name))
        return func.parameters

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