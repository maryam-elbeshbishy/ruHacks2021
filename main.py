import os
import asyncio
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$bye'):
        await message.channel.send('```bye!```')


    if message.content.startswith('$addClass'):
        userInput = message.content[8:]
        await client.send_message(message.channel, userInput)
        







    # if message.content.startswith('$thumb'):
    #     channel = message.channel
    #     await channel.send('Send me that "hi" reaction, mate')

    #     def check(string, user):
    #         return user == message.author and string == "hi"

    #     # try:
    #     #     # string, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
    #     # except asyncio.TimeoutError:
    #     if check:
    #         await channel.send('👎')
    #     else:
    #         await channel.send('👍')
client.run(TOKEN)