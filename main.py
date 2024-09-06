import discord
from discord.ext import commands
import requests
import json
from discord import FFmpegPCMAudio 
# import os

from apikeys import *
from blacklist_word import *



intents = discord.Intents.all()
intents.members=True

queues  = {}
def check_queue(ctx,id):
    if queues != []:
        voice = ctx.guild.voice_client
        source = queues[id].pop[0]
        player = voice.play(source)

client = commands.Bot(command_prefix = '?',intents=intents)

@client.event
async def on_ready():
    print("The Bot is ready :)")
    print("------------------------")

@client.command()
async def hello(ctx):
    await ctx.send("Hello I am discord bot")

#Send msg when new members join the server
@client.event
async def on_member_join(member):

    url = "https://joke3.p.rapidapi.com/v1/joke"

    headers = {
        "x-rapidapi-key": "257d5b1b92msh8c79fcc611acb84p19349fjsn0c537baf5c34",
        "x-rapidapi-host": "joke3.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    print(response.json())

    channel =client.get_channel(1279863352360964139)
    await channel.send("Welcome")


@client.event
async def on_member_remove(member):
    channel=client.get_channel(1279863352360964139)
    await channel.send("Bhag gaya gandu")


@client.command(pass_context = True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I left the voice cahnnel")

    else:
        await ctx.send("I am not in a voice channel")

# PLAYING SONG IN THE VOICE CHANNEL
@client.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        channel=ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('Manana.mp3')
        player = voice.play(source)

    else:
        await ctx.send("You are not in a voice channel Dumb!!!")


# PAUSE SONGS
@client.command(pass_context = True)
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("At the moment, There is no audio playing!")

# RESUME THE SONG
@client.command(pass_context = True)
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The song is already resumed!")

#STOP THE SONG
@client.command(pass_context = True)
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    voice.stop()

#PLAY THE SONG
@client.command(pass_context = True)
async def play(ctx,arg):
    voice = ctx.guild.voice_client
    song = arg + '.mp3'
    source = FFmpegPCMAudio(song)
    player = voice.play(source,after=lambda x=None: check_queue(ctx, ctx.message.guild.id))

#QUEUE
@client.command(pass_context = True)
async def queue(ctx,arg):
    voice = ctx.guild.voice_client
    song = arg + '.mp3'
    source = FFmpegPCMAudio(song)
    
    guild_id = ctx.message.guild.id
    if guild_id in queues:
        queues[guild_id].append(source)
    else:
        queues[guild_id] = [source]
    
    await ctx.send("Added to queue")

#DETECTING SPECIFIC WORD


@client.event
async def on_message(message):
    for i in blacklist:
        if message.content.lower() == i:
            await message.delete()
            await message.channel.send("Sudhar ja bsdk...")


client.run(BOTTOKKEN)
