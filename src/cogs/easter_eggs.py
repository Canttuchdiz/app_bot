from src import *

class Eggs(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    #Contain fun easter egg commands, which only send messages to the channel where the comamnd is called.

    @commands.command(aliases=['dio'])
    async def world(self, ctx):
        await ctx.send("ZA WARUDO! TOKI WA TOMARE! ||Naruto and Sasuke obliterate Dio + Goku||")

    @commands.command()
    async def dm(self, ctx):
        await ctx.reply('https://www.youtube.com/watch?v=Jmq91taUy-A')

    @commands.check(util.UtilMethods.is_user)
    @commands.command()
    async def fart(self, ctx):
        await ctx.send("HAHAHAH THAT WAS FUNNY")


async def setup(bot):
    await bot.add_cog(Eggs(bot))