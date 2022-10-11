import discord
from dotenv import load_dotenv
import random
import aiohttp
import datetime
import asyncio
import json
import os
from discord.ext import commands, tasks
from discord.ui import Select, View

load_dotenv()

TOKEN = os.getenv("token")

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

async def user_communicate(user : discord.Member):
    with open('C:/Users/hgold/PycharmProjects/bot_app/src/utils/quest_ans.json', encoding='utf-8') as f:
        data = json.load(f)
        embed = discord.Embed(title="Mod Application Format")
        embed.add_field(name="Questions", value=data["total"])

        await user.send(data["total"])
        await user.send(data["rest"])


class MySelect(View):

    @discord.ui.select(
        placeholder="Which application do you want to complete",
        options=[discord.SelectOption(label="Mod App", value="1", description="Sends application to user"),
                 discord.SelectOption(label="Edited message", value="2", description="This is an edited message"),
                 discord.SelectOption(label="Normal Message", value="3", description="This is an normal message")
                 ])

    async def select_callback(self, interaction, select):
        if select.values[0] == "1":
            await user_communicate(interaction.user)

@client.command()
async def menu(ctx):
    view = MySelect()
    await ctx.send(view=view)

client.run(TOKEN)