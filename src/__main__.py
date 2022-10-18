from .imports import *

load_dotenv()

TOKEN : str = os.getenv("token")

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True
intents.bans = True


class Bot(commands.Bot):

    # Initializes needed data
    def __init__(self):
        super().__init__(command_prefix='!', intents=intents)
        self.initial_extentsions = ['cogs.events', 'cogs.easter_eggs', 'cogs.commands', 'cogs.interactions', 'cogs.help']

    # Loading all cogs
    async def setup_hook(self):
        for extentsions in self.initial_extentsions:
            await self.load_extension(extentsions)

# Creates instance of the bot and then runs it
client = Bot()

client.remove_command('help')

client.run(TOKEN)