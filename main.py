import discord
from discord.ext import commands, tasks
import kanji_reader

bot = commands.Bot("!")

TARGET_CHANNEL_ID = 586069902427947018
KANJI_AMOUNT = 5

todays_number = 1

@tasks.loop(seconds=10)
async def called_once_a_day():
    message_channel = bot.get_channel(TARGET_CHANNEL_ID)
    global todays_number
    kanji_of_the_day_markdown = kanji_reader.generate_todays_kanji_(todays_number, KANJI_AMOUNT)
    print(f"Sending day {todays_number} on channel {message_channel}")
    await message_channel.send(file=discord.File('Todays_Kanji.png'))
    todays_number = todays_number + 1
    await message_channel.send(kanji_of_the_day_markdown)

@called_once_a_day.before_loop
async def before():
    await bot.wait_until_ready()
    print("Bot is running")

called_once_a_day.start()
bot.run("ODYxMTg3MjE4OTkwOTU2NTQ1.YOGJGQ.GKH_4C_ySG9nVbdZHwEbN4RwGJ4")