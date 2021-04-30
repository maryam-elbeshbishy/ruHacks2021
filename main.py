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

    if message.content.startswith('$thumb'):
        channel = message.channel
        await channel.send('Send me that 👍🏽 reaction, mate')

        def check(str, user):
            return user == message.author and str(reaction.emoji) == '👍'

        try:
            reaction, message.author = await client.wait_for('reaction_add', timeout=20.0, check=check)
        except asyncio.TimeoutError:
            await channel.send('👎')
        else:
            await channel.send('👍')
client.run(TOKEN)