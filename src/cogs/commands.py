from src.imports import *

class Commands(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    # Gets the instnace of the bot and registers a command which returns the latency of the command.
    @commands.command(aliases=['pingpong'])
    async def ping(self, ctx, *, question=None):
        await ctx.send('Pong! {0}'.format(round(self.client.latency, 1)))

    # Shuts down bot, which can only be used by users in id_list in utils
    @commands.check(util.UtilMethods.is_user)
    @commands.command(aliases=['end', 'shutoff'])
    async def close(self, ctx):
        await ctx.send("Shutting down... :wave: bye!")
        await self.client.close()




async def setup(bot):
    await bot.add_cog(Commands(bot))