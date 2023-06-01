@bot.event
async def on_message(msg):
    if msg.content.lower().startswith("chat is this real"):
        print("success")
        replied_message = msg.reference
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