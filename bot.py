import os, asyncio, openai, requests, random, discord, youtube_dl

from discord.ext import commands

location = "Round Rock"

responseWeather = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}")
formatWeather = responseWeather.json()

yt_dl_opts = {'format': 'bestaudio/best'}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

ffmpeg_options = {'options': "-vn"}

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
    channel = bot.get_channel(895502770260570123)
    await channel.send("exothermic reactions")
    print(f"Moose bot is here as {bot.user}")

@bot.event
async def on_message(message):
    await bot.process_commands(message)

@bot.command()
async def hi(ctx):
    await ctx.send(f"stfu {ctx.author.display_name}")

@bot.command()
async def chat(ctx):
    replied_message = ctx.reference
    if replied_message and replied_message.message_id:
        channel = bot.get_channel(replied_message.channel_id)
        message = await channel.fetch_message(replied_message.message_id)
    url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + message.content
    response = requests.get(url)
    data = response.json()
    try:
        summary = data["extract"]
        await msg.channel.send(summary)
    except:
        await msg.channel.send("no")

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
async def real(ctx):
    replied_message = ctx.message.reference
    if replied_message and replied_message.cached_message.content:
        replied_content = replied_message.cached_message.content
        search(ctx, replied_content)

@bot.command()
async def play(ctx, *, query):
    if ctx.author.voice is None:
        await ctx.send("You are not connected to a voice channel.")
        return

    voice_channel = ctx.author.voice.channel
    vc = await voice_channel.connect()

    try:
        response = requests.get(f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={query}&type=video&key={youtube_key}")
        format = response.json()
        url = "https://www.youtube.com/watch?v=" + format['items'][0]['id']['videoId']
        await ctx.send(url)

        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

        song = data['url']
        player = discord.FFmpegPCMAudio(song, **ffmpeg_options)

        # Play the audio
        vc.play(player)

    except Exception as e:
        print(e)
        await ctx.send("An error occurred while playing the audio.")

bot.run(token)
