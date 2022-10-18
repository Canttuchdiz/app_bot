from src import *


class Events(commands.Cog):

    def __init__(self, bot):
        self.client = bot
        self.channel_20: int = int(os.getenv("channelid2"))

    # Sets up do not disturb and it's "Listening to Cube"
    @commands.Cog.listener()
    async def on_ready(self):
        print('Ready!')
        print('Logged in as ---->', self.client.user)
        print('ID:', self.client.user.id)
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Cube Incorporation"), status=discord.Status.do_not_disturb)

    # Gets a list of the channels in a json to iterate through. Prevent users from viewing them and Lvl 20 from specific channel
    @commands.check(util.UtilMethods.is_user)
    @commands.command(aliases=['thanossnap'])
    async def eventstart(self, ctx):
        id_list = await util.UtilMethods.json_retriever('utils/id_data.json')
        channel_lvl = self.client.get_channel(int(self.channel_20))
        for id in id_list:
            await self.client.get_channel(id).set_permissions(ctx.guild.default_role, view_channel=False)
        await channel_lvl.set_permissions(ctx.guild.get_role(942240986103443506), view_channel=False)


    #Ends the event above doing the opposite
    @commands.check(util.UtilMethods.is_user)
    @commands.command()
    async def eventend(self, ctx):
        id_list = await util.UtilMethods.json_retriever('utils/id_data.json')
        channel_lvl = self.client.get_channel(int(self.channel_20))
        for id in id_list:
            await self.client.get_channel(id).set_permissions(ctx.guild.default_role, view_channel=True)
        await channel_lvl.set_permissions(ctx.guild.get_role(942240986103443506), view_channel=True)

    #Excepts errors, handles them accordingly, and sends new exceptions to stderr for the interpreter to print out.
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        ignored = (commands.CommandNotFound,)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except discord.HTTPException:
                pass

            # For this error example we check to see where it came from...
        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':  # Check if the command being invoked is 'tag list'
                await ctx.send('I could not find that member. Please try again.')

        else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

        """Below is an example of a Local Error Handler for our command do_repeat"""


async def setup(bot):
    await bot.add_cog(Events(bot))