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
import util

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
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Cube Incorporation"), status=discord.Status.do_not_disturb)


@client.command(aliases=['pingpong'])
async def ping(ctx, *, question=None):
    await ctx.send('Pong! {0}'.format(round(client.latency, 1)))

@client.command(aliases=['dio'])
async def world(ctx):
    await ctx.send("ZA WARUDO! TOKI WA TOMARE! ||Naruto and Sasuke obliterate Dio + Goku||")

@client.command()
async def dm(ctx):
    await ctx.reply('https://www.youtube.com/watch?v=Jmq91taUy-A')

async def user_callback(user : discord.Member):

        data = await util.UtilMethods.json_retriever('utils/quest_ans.json')
        answers = []
        for i in range(len(data) - 1):
            em = discord.Embed(color=discord.Color.red())
            em.add_field(name=f"Question {i + 1}", value=data[i])
            response = await user.send(embed=em)
            msg = await client.wait_for('message', check=lambda m: m.author == user and m.channel == user.dm_channel)
            answers.append(msg.content)
        fem = discord.Embed(color=discord.Color.green())
        fem.add_field(name="Congratulations!", value=data[len(data) - 1])
        await user.send(embed=fem)
        return answers

@commands.check(util.UtilMethods.is_user)
@client.command()
async def fart(ctx):
    await ctx.send("HAHAHAH THAT WAS FUNNY")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"You are missing permissions for this command.")


@commands.check(util.UtilMethods.is_user)
@client.command(aliases=['thanossnap'])
async def eventstart(ctx):
    id_list = await util.UtilMethods.json_retriever('utils/id_data.json')
    for id in id_list:
        await client.get_channel(id).set_permissions(ctx.guild.default_role, view_channel=False)

@commands.check(util.UtilMethods.is_user)
@client.command()
async def eventend(ctx):
    id_list = await util.UtilMethods.json_retriever('utils/id_data.json')
    for id in id_list:
        await client.get_channel(id).set_permissions(ctx.guild.default_role, view_channel=True)

class Menu(View):

    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label="Staff Application", style=discord.ButtonStyle.red)
    async def menu1(self, interaction : discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Application sent to your dms :)", ephemeral=True)
        channel = client.get_channel(int(answer_channel))
        answer_data = await user_callback(interaction.user)
        em = discord.Embed(color=discord.Color.blue(), title="Mod Apps", description=f"User {interaction.user} ({interaction.user.id})")
        for i in range(len(answer_data)):
            em.add_field(name=f"Question {i}", value=answer_data[i])
        await channel.send(embed=em)


@commands.check_any(commands.check(util.UtilMethods.is_user), commands.has_role("Senior Staff Team"), commands.is_owner())
@client.command(aliases=['button', 'apps'])
async def menu(ctx):
    view = Menu()
    await ctx.send(view=view)

client.run(TOKEN)