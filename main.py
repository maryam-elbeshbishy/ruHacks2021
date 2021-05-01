import os
import asyncio
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()
bot = commands.Bot(command_prefix='>')

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
    
    # if "chick" in message.content:
    #     await message.channel.send("hello")

    if message.content.startswith('$addToDo'):
        userInput = message.content[8:]
        information = userInput.split(seperator)
        f = open("testFile.txt", "a")
        count = len(open("testFile.txt").readlines(  )) + 1
        for toDo in information:
             # The number is not incrementing, it always prints 1
            f.write(str(count)+ ") " + toDo + "\n")
            count+=1
        
        f.close

    if message.content.startswith('$showToDo'):
        f = open("testFile.txt", "r")
        await message.channel.send(f.read())
   
    if message.content.startswith('$removeToDo'):
        userInput = message.content[11:]
        information = userInput.split(seperator)
        f = open("testFile.txt", "r")
        lines = f.readlines()
        f.close

        f2 = open("testFile.txt", "w")
        for line in lines:
            nLine = line.split(')')
            print(nLine[0])
            if(int(nLine[0])!=int(information[0])):
                f2.write(line)
            elif(nLine[0][0] == "~"):
                pass
            else:
                line = "~~"+line+"~~"
                f2.write(line)

        f2.close
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