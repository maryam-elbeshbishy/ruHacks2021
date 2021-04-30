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

    if message.content.startswith('$addClass'):
        userInput = message.content[9:]
        information = userInput.split("-")
        acronym = information[1]
        title = information[2]

        await message.channel.send(acronym)
        await message.channel.send(title)


    if message.content.startswith('$addTime_Link'):
        userInput = message.content[13:]
        information = userInput.split("-")
        acronym = information[1]
        day = information[2]
        hour = information[3]
        link = information[4]

        await message.channel.send(acronym)
        await message.channel.send(day)
        await message.channel.send(hour)
        await message.channel.send(link)
        

    if message.content.startswith('$addTextbook'):
        userInput = message.content[12:]
        information = userInput.split("-")
        acronym = information[1]
        textbook = information[2]
 
        await message.channel.send(acronym)
        await message.channel.send(textbook)

        




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