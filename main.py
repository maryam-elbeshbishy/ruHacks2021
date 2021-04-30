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
    seperator = ">"

    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$bye'):
        await message.channel.send('```bye!```')

    if message.content.startswith('$addClass'):
        userInput = message.content[9:]
        information = userInput.split(seperator)
        acronym = information[0]
        title = information[1]

        await message.channel.send(acronym)
        await message.channel.send(title)


    if message.content.startswith('$addTime_Link'):
        userInput = message.content[13:]
        information = userInput.split(seperator)
        acronym = information[0]
        day = information[1]
        hour = information[2]
        link = information[3]

        await message.channel.send(acronym)
        await message.channel.send(day)
        await message.channel.send(hour)
        await message.channel.send(link)
    
    if message.content.startswith('$addTextbook'):
        userInput = message.content[12:]
        information = userInput.split(seperator)
        acronym = information[0]
        textbook = information[1]
 
        await message.channel.send(acronym)
        await message.channel.send(textbook)

    if message.content.startswith('$addToDo'):
        userInput = message.content[8:]
        information = userInput.split(seperator)
        toDo = information[1]
        
        f = open("testFile.txt", "a")
        f.write(toDo+"\n")
        f.close

        await message.channel.send(toDo)    

    if message.content.startswith('$showToDo'):
        f = open("testFile.txt", "r")
        await message.channel.send(f.read())



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