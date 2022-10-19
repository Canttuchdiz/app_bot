from src import *
from src.utils import UtilMethods, UTILS_DIR

class Interactions(commands.Cog):

    """Handles interaction based commands like buttons."""

    def __init__(self, bot):
        self.client = bot

    # Not necessarily a callback, but handles posting questions, and receiving user input data from dms
    # Then data is returned
    async def user_callback(self, user: discord.Member):

        data = UtilMethods.json_retriever(UTILS_DIR / "quest_ans.json")
        answers = []
        for i in range(len(data) - 1):
            em = discord.Embed(color=discord.Color.red())
            em.add_field(name=f"Question {i + 1}", value=data[i])
            response = await user.send(embed=em)
            msg = await self.client.wait_for('message', check=lambda m: m.author == user and m.channel == user.dm_channel)
            answers.append(msg.content)
        fem = discord.Embed(color=discord.Color.green())
        fem.add_field(name="Congratulations!", value=data[len(data) - 1])
        await user.send(embed=fem)
        return answers



    # Calls the view containg the button.
    @commands.check_any(commands.check(UtilMethods.is_user), commands.has_role("Senior Staff Team"), commands.is_owner())
    @commands.command(aliases=['button', 'apps'])
    async def menu(self, ctx):
        """
        Sends button, which is pressed for mod apps.
        :param ctx:
        :return:
        """
        view = Menu(self)
        await ctx.send(view=view)
# The class containing the button.
class Menu(View):

    # Initializes important attributes
    def __init__(self, instance):
        super().__init__(timeout=None)
        self.answer_channel: int = int(os.getenv("channelid"))
        self.value = None
        self.instance = instance

    # Creates the button, and takes data from user_callback to send to channel in embed format
    # Takes in instance of cog class to retrieve certain data
    @discord.ui.button(label="Staff Application", style=discord.ButtonStyle.red)
    async def menu1(self, interaction: discord.Interaction, button: discord.ui.Button):
        client = interaction.client
        await interaction.response.send_message("Application sent to your dms :)", ephemeral=True)
        channel = client.get_channel(int(self.answer_channel))
        answer_data = await self.instance.user_callback(interaction.user)
        em = discord.Embed(color=discord.Color.blue(), title="Mod Apps", description=f"User {interaction.user} ({interaction.user.id})")
        for i in range(len(answer_data)):
            em.add_field(name=f"Question {i}", value=answer_data[i])
        await channel.send(embed=em)


async def setup(bot):
    await bot.add_cog(Interactions(bot))