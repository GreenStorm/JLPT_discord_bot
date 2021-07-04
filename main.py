import os
import discord
from discord.ext import commands, tasks

import kanji_reader
import config as CONFIG

bot = commands.Bot("!")
todays_number = 1

@tasks.loop(seconds=10)
async def called_once_a_day():
    message_channel = bot.get_channel(os.environ['TARGET_CHANNEL_ID'])
    global todays_number
    kanji_of_the_day_markdown = kanji_reader.generate_todays_kanji_(todays_number, CONFIG.KANJI_AMOUNT)
    print(f"Sending day {todays_number} on channel {message_channel}")
    await message_channel.send(file=discord.File('Todays_Kanji.png'))
    todays_number = todays_number + 1
    await message_channel.send(kanji_of_the_day_markdown)

@called_once_a_day.before_loop
async def before():
    await bot.wait_until_ready()
    print("Bot is running")

called_once_a_day.start()
print("INFO: token is "+ str(os.environ['DISCORD_BOT_TOKEN']))
bot.run(os.environ['DISCORD_BOT_TOKEN'])