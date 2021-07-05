import os
import discord
from discord.ext import commands, tasks

import kanji_reader
import config as CONFIG

bot = commands.Bot("!")
todays_number = 1

@tasks.loop(hours=24)
async def called_once_a_day():
    channel_id = int(os.environ['TARGET_CHANNEL_ID']) # needs to be cast to int otherwise would return none
    message_channel = bot.get_channel(channel_id)
    global todays_number
    print(f"Sending day {todays_number} on channel {message_channel}")
    await message_channel.send("Kanjis of day#"+str(todays_number))
    await message_channel.send(file=discord.File('Todays_Kanji.png'))
    kanji_of_the_day_markdown = kanji_reader.generate_todays_kanji_(todays_number, CONFIG.KANJI_AMOUNT)
    await message_channel.send(kanji_of_the_day_markdown)
    todays_number = todays_number + 1

@called_once_a_day.before_loop
async def before():
    await bot.wait_until_ready()
    print("Bot is running")

called_once_a_day.start()
bot.run(os.environ['DISCORD_BOT_TOKEN'])