import discord
import random
import requests

token = "MTEwNDk4MjI0Nzk2NDE2MDA3MQ.GSKBNi.FyvcYCEP2dL5RE-noknJfJO7TA7RO19Vagzpxs"

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
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Moose bot is here as {client.user}")

@client.event
async def on_message(msg):
    if msg.author != client.user:
        if msg.content.lower().startswith("hi"):
            await msg.channel.send(f"stfu {msg.author.display_name}")
        if msg.content.lower().startswith("info"):
            await msg.channel.send(random.choice(bat_quotes))
        if msg.content.lower().startswith("weather"):
            await msg.channel.send(f'{kelvin_to_farenheit(formatWeather["main"]["temp"])} Fahrenheit')
        if msg.content.lower().startswith("test"):
            with open("choppa.jpg", "rb") as f:
                file = discord.File(f)
                await msg.channel.send(file=file)
        if msg.content.lower().startswith("rank"):
            username = msg.content.replace("rank", "")
            username = username.replace("<@1104982247964160071>", "")
            usertag = username.split("#")
            response_mmr = requests.get(f"https://api.henrikdev.xyz/valorant/v1/mmr/na/{usertag[0]}/{usertag[1]}")
            format_mmr = response_mmr.json()
            url_rank = format_mmr['data']['images']['large']
            response_rank = requests.get(url_rank)
            with open("rank.png", "wb") as f:
                f.write(response_rank.content)
            await msg.channel.send(file=discord.File("rank.png"))

client.run(token)