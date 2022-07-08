import os
from keep_alive import keep_alive
from discord.ext import commands

bot = commands.Bot(
	command_prefix="!",  # Change to desired prefix
	case_insensitive=True  # Commands aren't case-sensitive
)

bot.author_ids = [295182226998558730, 248160341610070026, 419209849478316032]  # Change to your discord id!!!

@bot.event 
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier


extensions = [
  # Same name as it would be if you were importing it
	"cogs.speedrun_cog"
]

if __name__ == '__main__':  # Ensures this is the file being ran
	catagories = []
	for extension in extensions:
		bot.load_extension(extension)  # Loades every extension.

keep_alive()  # Starts a webserver to be pinged.
token = "OTk0NzQ5NzcxNDAxMTM0MjQx.Gpa6oD.s1FwxWPvM1eOD8Kmus28NcD8mkqGkFo19QTT84"
bot.run(token)  # Starts the bot