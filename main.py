# import discord
from discord.ext import commands, tasks


# client = discord.Client()
#
# @client.event
# async def on_ready():
#     print('Hey it me {0.user}'.format(client))
#
# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#
#     if message.content.startswith('$hello'):
#         await message.channel.send('Hello!')

bot = commands.Bot("!")
target_channel_id = 586069902427947018
COUNT = 0

@tasks.loop(seconds=24)
async def called_once_a_day():
    message_channel = bot.get_channel(target_channel_id)
    print(f"Got channel {message_channel}")
    global COUNT
    COUNT = COUNT + 1
    await message_channel.send("Take a chill pill " + str(COUNT))

@called_once_a_day.before_loop
async def before():
    await bot.wait_until_ready()
    print("Bot is running")

called_once_a_day.start()
bot.run("ODYxMTg3MjE4OTkwOTU2NTQ1.YOGJGQ.GKH_4C_ySG9nVbdZHwEbN4RwGJ4")

client.run('ODYxMTg3MjE4OTkwOTU2NTQ1.YOGJGQ.GKH_4C_ySG9nVbdZHwEbN4RwGJ4')