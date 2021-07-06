from datetime import datetime
import os
import kanji_reader
import discord
import config as CONFIG
from discord.ext import commands, tasks


class KanjiCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        today = datetime.now().timetuple()

        self.todays_number = int(today.tm_yday + (356 *
                                                  (today.tm_year - 2021)))
        self.kanji_loop.start()
        self.fileDir = os.path.dirname(os.path.abspath(__file__))

    @tasks.loop(minutes=10.0)
    async def kanji_loop(self):
        await self.send_kanji(self.todays_number)
        self.todays_number = self.todays_number + 1

    async def send_kanji(self, number):
        channel_id = int(
            os.environ['TARGET_CHANNEL_ID']
        )  # needs to be cast to int otherwise would return none
        kanji_of_the_day_df = kanji_reader.generate_todays_kanji_(
            number, CONFIG.KANJI_AMOUNT)
        url = "https://www.kanshudo.com/search?q="
        url += "%20".join(kanji_of_the_day_df.index.values)
        embed = discord.Embed(
            title="Kanji of day#" + str(number),
            #url=url, #add url if you want.. the one above will search all the kanji
            description="All your kanjis for the day!")
        i = 1
        for row in kanji_of_the_day_df.itertuples():
            embed.add_field(name=row.Index,
                            value=", ".join(row.meanings),
                            inline=False)
            if (len(row.readings_on)):
                embed.add_field(name="( " + row.Index + " ) 音読み",
                                value=" , ".join(row.readings_on),
                                inline=True)
            if (len(row.readings_kun)):
                embed.add_field(name="( " + row.Index + " ) 訓読み",
                                value=" , ".join(row.readings_kun),
                                inline=True)
            embed.add_field(name="*** ***",
                            value="***--------------------***",
                            inline=False)
            i += 1

        embed.set_footer(
            text="ありが３−９！",
            icon_url=
            'https://vignette.wikia.nocookie.net/youkoso-jitsuryoku-shijou-shugi-no-kyoushitsu-e/images/2/2d/Arisu_Sakayanagi_LN_visual.png/'
        )  #why not...
        message_channel = self.bot.get_channel(channel_id)
        print(f" INFO: Sending day {number} on channel {message_channel}")

        embed.set_image(url='attachment://Todays_Kanji.png')
        await message_channel.send(
            embed=embed,
            file=discord.File(os.path.join(self.fileDir, 'Todays_Kanji.png'),
                              filename="Todays_Kanji.png"))
        print(f" INFO: Sent day {number} on channel {message_channel}")

    @commands.command("kjd")
    async def request_kanji(self, ctx, day):
        if (isinstance(day, int) | day.isdigit()):
            day = int(day)
            if (day > self.todays_number):
                day = self.todays_number

            if (day > 0):
                await ctx.message.add_reaction("🔍")
                await self.send_kanji(day)
            else:
                await ctx.send("Hey thats not valid!")
                await ctx.message.add_reaction("👎")
        else:
            await ctx.message.add_reaction("👎")
            await ctx.send("Hey {} thats not right.. is it...".format(
                ctx.author))

    @kanji_loop.before_loop
    async def before_loop(self):
        print('waiting...')
        await self.bot.wait_until_ready()
        print('ready')

    @kanji_loop.after_loop
    async def after_loop(self):
        print('finished_loop')

    def cog_unload(self):
        self.kanji_loop.cancel()


def setup(bot):
    bot.add_cog(KanjiCog(bot))