from src import *
from src.utils import UtilMethods, UTILS_DIR, VCNotDetected


class Events(commands.Cog):
    """
    Handles events, and encapsulates two event commands.
    """


    def __init__(self, bot):
        self.client = bot
        self.channel_20: int = int(os.getenv("channelid2"))
        self.id_list = UtilMethods.json_retriever(UTILS_DIR / 'tools/jsons/id_data.json')

    # Sets up do not disturb and it's "Listening to Cube"
    @commands.Cog.listener()
    async def on_ready(self):
        print('Ready!')
        print('Logged in as ---->', self.client.user)
        print('ID:', self.client.user.id)
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Cube Incorporation"), status=discord.Status.do_not_disturb)

    # Gets a list of the channels in a json to iterate through. Prevent users from viewing them and Lvl 20 from specific channel
    @commands.check(UtilMethods.is_user)
    @commands.hybrid_command(name='eventstart', with_app_command=True)
    async def eventstart(self, ctx):
        """
        Makes member channels invisible for event
        :param ctx:
        :return:
        """

        channel_lvl = self.client.get_channel(int(self.channel_20))
        for id in self.id_list:
            try:
                await self.client.get_channel(id).set_permissions(ctx.guild.default_role, view_channel=False)
            except Exception as e:
                await ctx.send(f"Certain channel could not be retrieved. Error:```{id} does not retrieve channel.```")
        await channel_lvl.set_permissions(ctx.guild.get_role(942240986103443506), view_channel=False)


    #Ends the event above doing the opposite
    @commands.check(UtilMethods.is_user)
    @commands.hybrid_command(name='eventend', with_app_command=True)
    async def eventend(self, ctx):
        """
        Makes member channels visible after event
        :param ctx:
        :return:
        """
        channel_lvl = self.client.get_channel(int(self.channel_20))
        for id in self.id_list:
            try:
                await self.client.get_channel(id).set_permissions(ctx.guild.default_role,
                                                                  read_message_history=True, view_channel=True)
            except Exception as e:
                await ctx.send(f"Certain channel could not be retrieved. Error:```{id} does not retrieve channel.```")
        await channel_lvl.set_permissions(ctx.guild.get_role(942240986103443506), view_channel=True)

    #Excepts errors, handles them accordingly, and sends new exceptions to stderr for the interpreter to print out.

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        ignored = (commands.CommandNotFound,)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

        if isinstance(error, VCNotDetected):
            await ctx.send(f"{ctx.author.mention} join a voice channel to use **music** commands.")
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