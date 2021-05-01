import os
import asyncio
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()
# bot = commands.Bot(command_prefix='>')

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
    
    if "chick" in message.content:
        await message.channel.send("hello")

    if message.content.startswith('$addToDo'):
        userInput = message.content[8:]
        information = userInput.split(seperator)
        f = open("toDoList.txt", "a")
        count = len(open("toDoList.txt").readlines(  )) + 1 # The number is not incrementing, it always prints 1
        for toDo in information:
            f.write(str(count)+ ") " + toDo + "\n")
            count+=1
        f.close

    if message.content.startswith('$showToDo'):
        lst= ""
        f = open("toDoList.txt")
        lines = f.readlines()
        for todo in lines:
            lst+=todo+"\n"

        embed=discord.Embed(title="Todo List", description="Here is a list of the things you have to get done 💼", color=discord.Color.blue())
        embed.add_field(name="List",value=lst,inline=True)
        embed.set_author(name="EduBot", icon_url="https://images.pexels.com/photos/3299/postit-scrabble-to-do.jpg?auto=compress&cs=tinysrgb&h=650&w=940")
        await message.channel.send(embed=embed)
        
    if message.content.startswith('$clearTodo'):
        open('toDoList.txt', 'w').close()
        await message.channel.send("Todo List has been cleared✅")




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