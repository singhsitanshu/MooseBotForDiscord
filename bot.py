import discord
import random
import requests
import os
import asyncio

from discord.ext import commands
from discord import FFmpegPCMAudio

token = "MTEwNDk4MjI0Nzk2NDE2MDA3MQ.GJKWv2.Ksd9QpRDnxqgLPpE1UBQrfrDhDZOeyh-QbMl8E"

api_key = "25a8bd03eb02605ef5235259141e2e33"
location = "Round Rock"

responseWeather = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}")
formatWeather = responseWeather.json()

def kelvin_to_farenheit(k):
    c = (k-273.15)
    c *= (9/5)
    c += 32
    return round(c)

bat_quotes = ["I am vengeance, I am the night", "It's not who I am underneath, but what I do that defines me.", "The night is darkest just before the dawn. And I promise you, the dawn is coming.", "I have one power. I never give up.", "You either die a hero or you live long enough to see yourself become the villain.", "A hero can be anyone, even a man doing something as simple and reassuring as putting a coat around a little boy's shoulders to let him know that the world hadn't ended."]

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"Moose bot is here as {bot.user}")

@bot.command()
async def hi(ctx):
    await ctx.send(f"stfu {ctx.author.display_name}")

@bot.command()
async def info(ctx):
    await ctx.send(random.choice(bat_quotes))

@bot.command()
async def weather(ctx):
    await ctx.send(f'{kelvin_to_farenheit(formatWeather["main"]["temp"])} Fahrenheit')

@bot.command()
async def test(ctx):
    with open("choppa.jpg", "rb") as f:
        file = discord.File(f)
        await ctx.send(file=file)

@bot.command()
async def rank(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    usertag = str(member)
    usertag = usertag.split("#")
    response_mmr = requests.get(f"https://api.henrikdev.xyz/valorant/v1/mmr/na/{usertag[0]}/{usertag[1]}")
    format_mmr = response_mmr.json()
    url_rank = format_mmr['data']['images']['large']
    response_rank = requests.get(url_rank)
    with open("rank.png", "wb") as f:
        f.write(response_rank.content)
    await ctx.send(file=discord.File("rank.png"))

@bot.command()
async def search(ctx, *, query):
    url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + query
    response = requests.get(url)
    data = response.json()
    try:
        summary = data["extract"]
        await ctx.send(summary)
    except:
        await ctx.send("There is not a wikipedia page on the requested subject.")

@bot.command()
async def join(ctx):
    if not ctx.author.voice:
        await ctx.send("You are not connected to a voice channel.")
        return
    channel = ctx.author.voice.channel
    await channel.connect()

@bot.command()
async def play(ctx):
    if ctx.author.voice is None:
        await ctx.send("You are not connected to a voice channel.")
        return

    # Join the voice channel of the user who called the command
    voice_channel = ctx.author.voice.channel
    vc = await voice_channel.connect()

    try:
        # Load the audio file
        audio_source = discord.FFmpegPCMAudio("onepiece.mp3")

        # Play the audio
        vc.play(audio_source)

        # Wait for the audio to finish playing
        while vc.is_playing():
            await asyncio.sleep(1)

        # Disconnect from the voice channel
        await vc.disconnect()

    except Exception as e:
        print(e)
        await ctx.send("An error occurred while playing the audio.")

bot.run(token)
