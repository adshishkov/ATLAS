import os
import sys
import disnake

from disnake.ext import commands
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding = 'utf-8')


### ATLAS BOT
bot = commands.Bot(
    command_prefix = "$",
    intents = disnake.Intents.all(), 
    activity = disnake.Activity(
        type = disnake.ActivityType.watching, 
        name = "за сервером"
        ),
    status = disnake.Status.online,
    reload = True, 
    help_command = None)


### EVENT STATRTING BOT
@bot.event
async def on_ready():
    print(bot.user.name + " was successfully launched")
    print("Extensions loaded: " + str(len(bot.cogs)))
    print("Main developer: adshishkov")


### LOAD EXTENSIONS
def load_extensions(path): 
    for file in os.listdir(path):
        if os.path.isdir(os.path.join(path, file)):
            load_extensions(os.path.join(path, file))
        elif file.endswith(".py"):
            try:
                extension_path = os.path.join(path, file[:-3]).replace(os.sep, ".")
                bot.load_extension(extension_path)
                print(f"[Extension]> {extension_path} loaded")
            except Exception as e:
                print(f"Error while loading extension > {extension_path}: {type(e).__name__} - {e}")


load_extensions("extensions")
load_dotenv()


bot.run(os.getenv("TOKEN"))