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
        
    # ---------------------------- ADD CLASS TITLE + ACRONYM ----------------------------
    
    if message.content.startswith('$addClass'):
        userInput = message.content[10:]
        information = userInput.split(seperator)
        acronym = information[0]
        title = information[1]

        await message.channel.send(acronym)
        await message.channel.send(title)

    # ---------------------------- ADDING CLASS INFORMATION ----------------------------
    if message.content.startswith('$addTime_Link'):
        userInput = message.content[14:]
        information = userInput.split(seperator)
        acronym = information[0]
        day = information[1]
        hour = information[2]
        link = information[3]

        await message.channel.send(acronym)
        await message.channel.send(day)
        await message.channel.send(hour)
        await message.channel.send(link)
    
    # ---------------------------- ADD TEXTBOOK ----------------------------
    if message.content.startswith('$addTextbook'):
        userInput = message.content[13:]
        information = userInput.split(seperator)
        acronym = information[0]
        textbook = information[1]
 
        await message.channel.send(acronym)
        await message.channel.send(textbook)
    
    if "chick" in message.content:
        await message.channel.send("hello")

    # ---------------------------- TO DO LIST ----------------------------
    if message.content.startswith('$addToDo'):
        userInput = message.content[9:]
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
        await message.channel.send(embed=embed)

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
                line = "~~"+line+"~~\n"
                f2.write(line)

        f2.close
        
    if message.content.startswith('$clearTodo'):
        open('toDoList.txt', 'w').close()
        await message.channel.send("Todo List has been cleared✅")


    # ---------------------------- IMPORTANT DATES ----------------------------
    if message.content.startswith('$addImpDates'):
        userInput = message.content[13:]
        information = userInput.split(seperator)
        title = information[0]
        dateInput = information[1]

        dateInfo = dateInput.split(" ")
        date = dateInfo[0]
        hour = dateInfo[1]

        f = open("ImpDates.txt", "a")
        count = len(open("ImpDates.txt").readlines(  )) + 1 
        f.write(str(count)+ ") " + title + " [ " + date + " @ " + hour + " ]" + "\n")
        count+=1
        f.close

    if message.content.startswith('$showImpDates'):
        lst= ""
        f = open("ImpDates.txt")
        lines = f.readlines()
        for todo in lines:
            lst+=todo+"\n"

        embed=discord.Embed(title="Important Dates", description="Here is a list of upcoming important dates 💼", color=discord.Color.blue())
        embed.add_field(name="List",value=lst,inline=True)
        await message.channel.send(embed=embed)

    if message.content.startswith('$clearImpDates'):
        open('ImpDates.txt', 'w').close()
        await message.channel.send("Important Dates has been cleared ✅")

    if message.content.startswith('$removeImpDates'):
        userInput = message.content[16:]
        information = userInput.split(seperator)
        f = open("ImpDates.txt", "r")
        lines = f.readlines()
        f.close

        f2 = open("ImpDates.txt", "w")
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

client.run(TOKEN)