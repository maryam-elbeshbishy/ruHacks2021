import os
import discord
from discord.ext import commands, tasks
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

    # ---------------------------- ADDING CLASS TITLE + ACRONYM ----------------------------
    if message.content.startswith('$addClass'):
        userInput = message.content[10:]
        information = userInput.split(seperator)
        acronym = information[0]
        title = information[1]
        await message.channel.send("The class has been added 🏫")

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
        await message.channel.send("The class information has been added 🏫")

    
    # ---------------------------- ADD TEXTBOOK ----------------------------
    if message.content.startswith('$addTextbook'):
        userInput = message.content[13:]
        information = userInput.split(seperator)
        acronym = information[0]
        textbook = information[1]
        await message.channel.send("The textbook has been added 📚")

 
        await message.channel.send(acronym)
        await message.channel.send(textbook)
    
    if "chick" in message.content:
        await message.channel.send("hello")

    # ---------------------------- TO DO LIST ----------------------------

    # ------------- ADD TO DO --------------- 
    if message.content.startswith('$addToDo'):
        userInput = message.content[9:]
        information = userInput.split(seperator)
        f = open("toDoList.txt", "a")
        count = len(open("toDoList.txt").readlines(  )) + 1 # The number is not incrementing, it always prints 1
        for toDo in information:
            f.write(str(count)+ ") " + toDo + "\n")
            count+=1
        f.close
        await message.channel.send("The task(s) has been added ⌚")

    # ------------- SHOW TO DO ---------------  
    if message.content.startswith('$showToDo'):
        lst= ""

        f = open("toDoList.txt", "a")
        f.close

        f = open("toDoList.txt", "r")
        lines = f.readlines()

        if len(lines)==0:
            await message.channel.send("The Todo List is empty 😯")
            return
        for todo in lines:
            if(str(todo[0]) == "~"):
                lst+=todo
            else:
                lst+=todo+"\n"

        embed=discord.Embed(title="Todo List", description="Here is a list of the things you have to get done 💼")
        embed.add_field(name="List",value=lst,inline=True)
        await message.channel.send(embed=embed)

    # ------------- REMOVE TO DO ---------------  
    if message.content.startswith('$removeToDo'):
        userInput = message.content[11:]
        information = userInput.split(seperator)
        f = open("toDoList.txt", "r")
        lines = f.readlines()
        f.close

        f2 = open("toDoList.txt", "w")
        for line in lines:
            nLine = line.split(')')
            
            if(str(nLine[0][0]) == "~" or str(nLine[0][0]) == ""):
                f2.write(line)
            elif(int(nLine[0])!=int(information[0])):
                f2.write(line)
                
            else:
                await message.channel.send("The task has been removed :basket:")
                line = "~~"+line+"~~\n"
                f2.write(line)

        f2.close

    # ------------- CLEAR TO DO ---------------    
    if message.content.startswith('$clearTodo'):
        open('toDoList.txt', 'w').close()
        await message.channel.send("Todo List has been cleared✅")


    # ---------------------------- IMPORTANT DATES ----------------------------

    # ------------- ADD DATE ---------------
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
        await message.channel.send("The important date has been added ⌚")

    # ------------- SHOW DATE ---------------
    if message.content.startswith('$showImpDates'):
        lst= ""
        
        f = open("ImpDates.txt", "a")
        f.close

        f = open("ImpDates.txt", "r")
        lines = f.readlines()

        if len(lines)==0:
            await message.channel.send("The Important Dates list is empty 😯")
            return

        for todo in lines:
            if(str(todo[0]) == "~"):
                lst+=todo
            else:
                lst+=todo+"\n"

        embed=discord.Embed(title="Important Dates", description="Here is a list of upcoming important dates 💼", color=discord.Color.blue())
        embed.add_field(name="List",value=lst,inline=True)
        await message.channel.send(embed=embed)

    # ------------- CLEAR DATE ---------------
    if message.content.startswith('$clearImpDates'):
        open('ImpDates.txt', 'w').close()
        await message.channel.send("Important dates has been cleared ✅")

    # ------------- REMOVE DATE ---------------
    if message.content.startswith('$removeImpDates'):
        userInput = message.content[16:]
        information = userInput.split(seperator)
        f = open("ImpDates.txt", "r")
        lines = f.readlines()
        f.close

        f2 = open("ImpDates.txt", "w")
        for line in lines:
            nLine = line.split(')')

            if(str(nLine[0][0]) == "~" or str(nLine[0][0]) == ""):
                f2.write(line)
            elif(int(nLine[0])!=int(information[0])):
                f2.write(line)
                
            else:
                await message.channel.send("The date has been removed :basket:")
                line = "~~"+line+"~~\n"
                f2.write(line)

        f2.close

    # ---------------------------- HELP COMMAND ----------------------------
    if message.content.startswith('$help'):
        embed=discord.Embed(title="Commands", description="Here's a list of the commands and how to use them!", color=0x78c6dd)
        embed.add_field(name="$addClass", value="$addClass CourseCode>CourseName\nAdd a class to your schedule", inline=False)
        embed.add_field(name="$addTextbook", value="$addTextbook TextbookName\nAdd a textbook link to stay organized", inline=False)
        embed.add_field(name="$addToDo", value="$addToDo Task\nAdd a task to your to do list", inline=False)
        embed.add_field(name="$addImpDates", value="$addImpDates Date>Time>Name\nSave important assignments and dates to be notified", inline=False)
        embed.add_field(name="$removeToDo", value="$removeToDo Task\nCross out a task once youre done", inline=False)
        embed.add_field(name="$removeImpDates", value="$remove Date>Time>Name\nRemove an important date once it is over", inline=False)
        embed.add_field(name="$showToDo", value="Lists your to do list", inline=False)
        embed.add_field(name="$showImpDate", value="Lists your important dates", inline=False)
        embed.add_field(name="$clearToDo", value="Clears all items off to do list", inline=False)
        embed.add_field(name="$clearImpDates", value="Clears all items off important dates list", inline=False)
        embed.add_field(name="$addTime_Link", value="$addTime_Link CourseCode>Day>Time>MeetingLink\nAdd a new meeting link for your lectures, by course code", inline=True)
        await message.channel.send(embed=embed)

client.run(TOKEN)