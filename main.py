import os
from discord.ext import commands

bot = commands.Bot("!")
bot.load_extension("KanjiCog")


@bot.event
async def on_ready():
    print("INFO:  Bot is running")


print("INFO: bot start run")
bot.run(os.environ['DISCORD_BOT_TOKEN'], reconnect=True)
