import os
import discord
from discord.ext import commands, tasks

import kanji_reader
import config as CONFIG

bot = commands.Bot("!")
todays_number = 1

@tasks.loop(seconds=24)
async def called_once_a_day():
    channel_id = int(os.environ['TARGET_CHANNEL_ID']) # needs to be cast to int otherwise would return none
    message_channel = bot.get_channel(channel_id)
    global todays_number
    print(f" INFO: Sending day {todays_number} on channel {message_channel}")
    await message_channel.send("Kanji of day#"+str(todays_number))
    kanji_of_the_day_table_as_string = kanji_reader.generate_todays_kanji_(todays_number, CONFIG.KANJI_AMOUNT)

    await message_channel.send(kanji_of_the_day_table_as_string)
    #kanji_embed = discord.Embed()
    #kanji_embed.add_field(name="Kanji of day# - "+str(todays_number), value=, inline=True)
    #kanji_embed.set_footer(text=kanji_of_the_day_html)
    #await message_channel.send(embed=kanji_embed)

    todays_number = todays_number + 1


@called_once_a_day.before_loop
async def before():
    await bot.wait_until_ready()
    print("INFO:  Bot is running")

print("Triggering loop start")
called_once_a_day.start()

print("INFO: bot start run")
bot.run(os.environ['DISCORD_BOT_TOKEN'])


