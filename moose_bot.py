import discord
import random
import requests

token = ""

api_key = ""
location = "Round Rock"

response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}")
format = response.json()

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
        if msg.content.lower().startswith("?hi"):
            await msg.channel.send(f"stfu {msg.author.display_name}")

@client.event
async def on_message(msg):
    if msg.author != client.user:
        if msg.content.lower().startswith("?info"):
            await msg.channel.send(random.choice(bat_quotes))

@client.event
async def on_message(msg):
    if msg.author != client.user:
        if msg.content.lower().startswith("?weather"):
            await msg.channel.send(f'{kelvin_to_farenheit(format["main"]["temp"])} Fahrenheit')

client.run(token)