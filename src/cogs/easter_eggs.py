from src import *
from src.utils.resources import UTILS_DIR

class Eggs(commands.Cog):

    """
    Fun easter egg commands.
    """

    def __init__(self, bot):
        self.client = bot
        self.ignores = {}

    #Contain fun easter egg commands, which only send messages to the channel where the comamnd is called.

    @commands.command(aliases=['dio'])
    async def world(self, ctx):
        """
        Tells information about Dio's The World!
        :param ctx:
        :return:
        """
        file = discord.File(fp=UTILS_DIR / 'time.mp3', filename="time.mp3")
        await ctx.send("ZA WARUDO! TOKI WA TOMARE!", file=file)

    @commands.command()
    async def ignore(self, ctx : commands.Context, user : discord.Member):
        self.ignores[user.name] = ctx.author.name
        await ctx.send("Ignore was indexed.")

    @commands.command()
    async def ignores(self, ctx, user : discord.Member):
        for key, value in self.ignores:
            if key == user.name:
                await ctx.send(', '.join(f"{key} ignored {value}"))

    @commands.command()
    async def give_role(self, ctx, role):
        user = ctx.user
        await ctx.send(f"{user} was given {role} ||{user.id}||")

    @commands.command()
    async def dm(self, ctx):
        """
        Sends instructions how to open dms.
        :param ctx:
        :return:
        """
        await ctx.reply('https://www.youtube.com/watch?v=Jmq91taUy-A')

    @commands.check(UtilMethods.is_user)
    @commands.command()
    async def fart(self, ctx):
        """
        Funny test command.
        :param ctx:
        :return:
        """
        await ctx.send("HAHAHAH THAT WAS FUNNY")


async def setup(bot):
    await bot.add_cog(Eggs(bot))