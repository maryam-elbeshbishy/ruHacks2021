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

    if message.content.startswith('$addClass'):
        userInput = message.content[9:]
        information = userInput.split(seperator)
        acronym = information[0]
        title = information[1]
        await message.channel.send("The class has been added 🏫")

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
        await message.channel.send("The class information has been added🏫")

    
    if message.content.startswith('$addTextbook'):
        userInput = message.content[12:]
        information = userInput.split(seperator)
        acronym = information[0]
        textbook = information[1]
        await message.channel.send("The textbook has been added 📚")

 
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
        await message.channel.send("The task(s) has been added ⌚")


    if message.content.startswith('$showToDo'):
        lst= ""
        f = open("toDoList.txt")
        lines = f.readlines()

        if len(lines)==0:
            await message.channel.send("The Todo List is empty 😯")
            return
        for todo in lines:
            lst+=todo+"\n"

        embed=discord.Embed(title="Todo List", description="Here is a list of the things you have to get done 💼")
        embed.add_field(name="List",value=lst,inline=True)
        await message.channel.send(embed=embed)


    if message.content.startswith('$removeToDo'):
        userInput = message.content[11:]
        information = userInput.split(seperator)
        f = open("toDoList.txt", "r")
        lines = f.readlines()
        f.close

        f2 = open("toDoList.txt", "w")
        for line in lines:
            nLine = line.split(')')
            print(nLine[0])
          
            if( nLine[0][0] == "~"):
                pass
            elif(int(nLine[0])!=int(information[0])):
                f2.write(line)
            else:
                await message.channel.send("The task has been remove 🧺")
                line = "~~"+line+"~~"
                f2.write(line)

        f2.close

        
    if message.content.startswith('$clearTodo'):
        open('toDoList.txt', 'w').close()
        await message.channel.send("Todo List has been cleared ✅")


client.run(TOKEN)