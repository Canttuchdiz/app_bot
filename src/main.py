import discord
from dotenv import load_dotenv
import random
import datetime
from asyncio import sleep
import aiofiles
import json
import os
from discord.ext import commands, tasks
from discord.ui import Select, View

load_dotenv()

TOKEN = os.getenv("token")
answer_channel = os.getenv("channelid")

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True
intents.bans = True

client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print("Bot is ready.")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Cube Corp."), status=discord.Status.do_not_disturb)


@client.command(aliases=['pingpong'])
async def ping(ctx, *, question=None):
    await ctx.send('Pong! {0}'.format(round(client.latency, 1)))


@client.command()
async def activate_app(ctx, member : discord.Member, *, message):
    await member.send(f"{ctx.author}: {message}")

async def user_callback(user : discord.Member):
    async with aiofiles.open('utils/quest_ans.json', encoding='utf-8') as f:
        content = await f.read()
        data = json.loads(content)
        answers = []
        for i in range(len(data)):
            em = discord.Embed(color=discord.Color.red())
            em.add_field(name=f"Question {i + 1}", value=data[i])
            await user.send(embed=em)
            if i != len(data) - 1:
                msg = await client.wait_for('message', check=lambda m: m.author == user)
                answers.append(msg.content)
        return answers



class Menu(View):

    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="Mod Application", style=discord.ButtonStyle.green)
    async def menu1(self, interaction : discord.Interaction, button: discord.ui.Button):
        channel = client.get_channel(int(answer_channel))
        answer_data = await user_callback(interaction.user)
        em = discord.Embed(color=discord.Color.blue(), title="Mod Apps", description=f"User {interaction.user}")
        for i in range(len(answer_data)):
            em.add_field(name=f"Question {i}", value=answer_data[i])
        await channel.send(embed=em)


@client.command(aliases=['dropdown'])
async def menu(ctx):
    view = Menu()
    await ctx.send(view=view)

client.run(TOKEN)