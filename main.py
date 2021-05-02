import os
import discord
import psycopg2
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from dotenv import load_dotenv
import psycopg2

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.utils import find

import time
channel_ID = 0
# ---------------------------- CONNECTING & CONFIGURATIONS ------------------------
conn = psycopg2.connect(
    database='whole-mink-215.edubotdb',
    user='maryam',
    password='Oulnmt4wZqd-bzwR',
    host='free-tier5.gcp-europe-west1.cockroachlabs.cloud',
    port=26257
)
conn.set_session(autocommit=True)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()
cur = conn.cursor()
scheduler = AsyncIOScheduler()

# ---------------------------- DATABASE ------------------------


def show_dataBase():
    print("\n\n\n\n")
    cur.execute("SELECT * FROM EduBot;")
    table = cur.fetchall()
    conn.commit()
    for i in table:
        print(i)


def check_code(code):
    cur.execute("""
        SELECT courseCode FROM EduBot
        WHERE '{}' IN (SELECT courseCode FROM EduBot);    
    """.format(code))
    option = cur.fetchall()
    if option == []:
        return False
    return True

# ---------------------------- 24 HOUR TIME CONVERSION ------------------------


def time_conversion(time):
    timeSplit = time.split(":")
    minuteSplit = timeSplit[1].split(" ")
    convertedTime = [0, 0]

    # Case 1: Time is in PM
    if time[len(time) - 2::].upper() == "PM":
        if int(timeSplit[0]) == 12:
            convertedTime[0] = timeSplit[0]
            convertedTime[1] = minuteSplit[0]
        else:
            hour = int(timeSplit[0]) + 12
            convertedTime[0] = str(hour)
            convertedTime[1] = minuteSplit[0]

    # Case 2: Time is in AM
    if time[len(time) - 2::].upper() == "AM":
        if int(timeSplit[0]) == 12:
            convertedTime[0] = "0"
            convertedTime[1] = minuteSplit[0]
        else:
            convertedTime[0] = timeSplit[0]
            convertedTime[1] = minuteSplit[0]
    return convertedTime

# ---------------------------- DAY CONVERSION ------------------------


def day_conversion(day):
    if day.lower() == "monday":
        return "0"
    elif day.lower() == "tuesday":
        return "1"
    elif day.lower() == "wednesday":
        return "2"
    elif day.lower() == "thursday":
        return "3"
    elif day.lower() == "friday":
        return "4"
    elif day.lower() == "saturday":
        return "5"
    else:
        return "6"


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    cur.execute("""
    CREATE TABLE IF NOT EXISTS EduBot (
    courseCode VARCHAR,
    courseName VARCHAR,
    textBook VARCHAR,
    meetingLink VARCHAR,
    dayWeek VARCHAR,
    timeWeek VARCHAR
    );
    """)

# ---------------------------- NOTIFICATION TESTING ------------------------
async def job(acronym, day, hour, link):
    channel = client.get_channel(channel_ID)
    cur.execute("""
        SELECT courseName FROM EduBot
        WHERE courseCode = '{}';
    """.format(acronym))
    title = cur.fetchall()
    conn.commit()

    embed=discord.Embed(title=":alarm_clock: You have {} right now!".format(title[0][0]), description="{} takes place on {} at {}".format(acronym,day.title(),hour), color=0xb0d6ee)
    embed.add_field(name="Zoom Link: ", value=link, inline=True)
    await channel.send(embed=embed)

@client.event
async def on_guild_join(guild):
    general = find(lambda x: x.name == 'general',  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send('Hello {}! Glad to be here :grinning: \n\nPlease enter the channel ID with the command $id [channelId] to set the annoucements channel'.format(guild.name))

@client.event
async def on_message(message):
    seperator = ">"

    if message.author == client.user:
        return

    if message.content.startswith('$id'):
        userInput = message.content[3:].strip()
        global channel_ID 
        channel_ID = userInput
        
    # ---------------------------- ADDING CLASS TITLE + ACRONYM ----------------------------
    if message.content.startswith('$addClass'):
        userInput = message.content[10:]
        information = userInput.split(seperator)
        acronym = information[0].upper().strip()
        title = information[1].title().strip()
        # if check_code(acronym):
        #     await message.channel.send("There is already information for '{}' 😯\n Use $addTime_Link or $addTextbook to update it.".format(acronym))
        #     return
        cur.execute("""
        INSERT INTO EduBot VALUES
        ('{}','{}',NULL,NULL,NULL,NULL);
        """.format(acronym, title))
        await message.channel.send("The class has been added 🏫")
        show_dataBase()

    # ---------------------------- REMOVING CLASS TITLE + ACRONYM ----------------------------
    if message.content.startswith('$removeClass'):
        userInput = message.content[13:]
        information = userInput.split(seperator)
        acronym = information[0].upper().strip()
        if not check_code(acronym):
            await message.channel.send("There no information for '{}'. It does NOT exist 😯\n Use $addClass to add it.".format(acronym))
            return

        try:
            cur.execute("""
            DELETE FROM EduBot WHERE courseCode = '{}';
            """.format(acronym))
            scheduler.remove_job(acronym)
            await message.channel.send("The class has been removed :basket:")
        except:
            cur.execute("""
            DELETE FROM EduBot WHERE courseCode = '{}';
            """.format(acronym))
            await message.channel.send("The class has been removed :basket:")


        # show_dataBase()

    # ---------------------------- ADDING CLASS INFORMATION ----------------------------
    if message.content.startswith('$addTime_Link'):
        userInput = message.content[14:]
        information = userInput.split(seperator)
        acronym = information[0].strip().upper()
        day = information[1].strip()
        hour = information[2]
        link = information[3].strip()
        conv_hour = time_conversion(hour)
        print(conv_hour)
        conv_day = day_conversion(day)

        if not check_code(acronym):
            await message.channel.send("There is no information for '{}' 😯\n Use $addClass to add some.".format(acronym))
            return

        scheduler.add_job(job, CronTrigger(hour=conv_hour[0], minute=conv_hour[1], day_of_week=conv_day), id=acronym, args=(acronym, day, hour, link))

        cur.execute("""
        UPDATE EduBot
        SET meetingLink = '{}', dayWeek = '{}', timeWeek = '{}'
        WHERE courseCode = '{}';
        """.format(link, day, hour, acronym))

        await message.channel.send("The class information has been added 🏫")

    # ---------------------------- ADD TEXTBOOK ----------------------------
    if message.content.startswith('$addTextbook'):
        userInput = message.content[13:]
        information = userInput.split(seperator)
        acronym = information[0].upper().strip()
        textbook = information[1].strip()

        if not check_code(acronym):
            await message.channel.send("There is no information for '{}' 😯\n Use $addClass to add some.".format(acronym))
            return

        cur.execute("""
        UPDATE EduBot
        SET textBook = '{}'
        WHERE courseCode = '{}';
        """.format(textbook, acronym))
        await message.channel.send("The textbook has been added 📚")

    if "chick" in message.content:
        await message.channel.send("hello")

    # ---------------------------- GET CLASS TITLE ----------------------------
    if message.content.startswith('$getClassTitle'):
        userInput = message.content[15:]
        information = userInput.split(seperator)
        acronym = information[0].upper().strip()

        if not check_code(acronym):
            await message.channel.send("There is no information for '{}' 😯\n Use $addClass to add some.".format(acronym))
            return

        cur.execute("""
            SELECT courseName FROM EduBot 
            WHERE courseCode = '{}';
        """.format(acronym))
        title = cur.fetchall()
        conn.commit()

        if title[0][0] == None:
            await message.channel.send("There no is course title for {} 😯".format(acronym))
        else:
            await message.channel.send("ℹ The course title of {} is: {}.".format(acronym, title[0][0]))

    # ---------------------------- GET MEETING LINK ----------------------------
    if message.content.startswith('$getClassCode'):
        userInput = message.content[14:]
        information = userInput.split(seperator)
        acronym = information[0].upper().strip()

        if not check_code(acronym):
            await message.channel.send("There is no information for '{}' 😯\n Use $addClass to add some.".format(acronym))
            return

        cur.execute("""
            SELECT courseCode FROM EduBot 
            WHERE courseName = '{}';
        """.format(acronym))
        code = cur.fetchall()
        conn.commit()
        if code[0][0] == None:
            await message.channel.send("There no is course code for {} 😯".format(acronym))
        else:
            await message.channel.send("ℹ The course code of {} is: {}.".format(title, code[0][0]))

    # ---------------------------- GET MEETING LINK ----------------------------
    if message.content.startswith('$getMeetingLink'):
        userInput = message.content[16:]
        information = userInput.split(seperator)
        acronym = information[0].upper().strip()
        if not check_code(acronym):
            await message.channel.send("There is no information for '{}' 😯\n Use $addClass to add some.".format(acronym))
            return
        cur.execute("""
            SELECT meetingLink FROM EduBot 
            WHERE courseCode = '{}';
        """.format(acronym))
        link = cur.fetchall()
        conn.commit()

        if link[0][0] == None:
            await message.channel.send("There is no meeting link for {} 😯".format(acronym))
        else:
            await message.channel.send("🔗 The meeting link for {} is: {}".format(acronym, link[0][0]))

    # ---------------------------- GET TEXTBOOK ----------------------------
    if message.content.startswith('$getTextbook'):
        userInput = message.content[13:]
        information = userInput.split(seperator)
        acronym = information[0].upper().strip()

        if not check_code(acronym):
            await message.channel.send("There is no information for '{}' 😯\n Use $addClass to add some.".format(acronym))
            return

        cur.execute("""
            SELECT textBook FROM EduBot 
            WHERE courseCode = '{}';
        """.format(acronym))
        text = cur.fetchall()
        conn.commit()
        if text[0][0] == None:
            await message.channel.send("There is no textbook link for {} 😯".format(acronym))
        else:
            await message.channel.send("🔗 The textbook link for {} is: {}".format(acronym, text[0][0]))

    # ---------------------------- SCHEDULE ----------------------------

    # ------------- GET SCHEDULE ---------------
    if message.content.startswith('$getSchedule'):
        lst = ""
        cur.execute("""
            SELECT courseCode, courseName, dayWeek, timeWeek FROM EduBot;
        """)
        information = cur.fetchall()
        conn.commit()

        if len(information) == 0:
            lst += "There is nothing scheduled this week 😯"

        for c in range(len(information)):
            lst += ("{} {} [ {} @ {}]\n".format(information[c][0],
                    information[c][1], information[c][2], information[c][3]))

        embed = discord.Embed(
            title="Weekly Schedule", description="Here is your weekly schedule 💼", color=discord.Color.blue())
        embed.add_field(name="This Week", value=lst, inline=True)
        await message.channel.send(embed=embed)

    # ------------- CLEAR SCHEDULE ---------------
    if message.content.startswith('$clearSchedule'):
        cur.execute("""
            DROP TABLE EduBot;
        """)
        conn.commit()
        await message.channel.send("Your schedule has been cleared :basket:")
        cur.execute("""
        CREATE TABLE IF NOT EXISTS EduBot (
            courseCode VARCHAR,
            courseName VARCHAR,
            textBook VARCHAR,
            meetingLink VARCHAR,
            dayWeek VARCHAR,
            timeWeek VARCHAR
            );
        """)

    # ---------------------------- TO DO LIST ----------------------------

    # ------------- ADD TO DO ---------------
    if message.content.startswith('$addToDo'):
        userInput = message.content[9:]
        information = userInput.split(seperator)
        f = open("toDoList.txt", "a")
        count = len(open("toDoList.txt").readlines()) + 1
        for toDo in information:
            f.write(str(count) + ") " + toDo + "\n")
            count += 1
        f.close
        await message.channel.send("The task(s) has been added ⌚")



    # ------------- SHOW TO DO ---------------
    if message.content.startswith('$showToDo'):
        lst = ""

        f = open("toDoList.txt", "a")
        f.close

        f = open("toDoList.txt", "r")
        lines = f.readlines()

        if len(lines) == 0:
            await message.channel.send("The Todo List is empty 😯")
            return
        for todo in lines:
            if(str(todo[0]) == "~"):
                lst += todo
            else:
                lst += todo+"\n"

        embed = discord.Embed(
            title="Todo List", description="Here is a list of the things you have to get done 💼")
        embed.add_field(name="List", value=lst, inline=True)
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
            elif(int(nLine[0]) != int(information[0])):
                f2.write(line)

            else:
                await message.channel.send("The task has been removed :basket:")
                line = "~~"+line+"~~\n"
                f2.write(line)

        f2.close

    # ------------- CLEAR TO DO ---------------
    if message.content.startswith('$clearToDo'):
        print("REACHED")
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
        count = len(open("ImpDates.txt").readlines()) + 1
        f.write(str(count) + ") " + title +
                " [ " + date + " @ " + hour + " ]" + "\n")
        count += 1
        f.close
        await message.channel.send("The important date has been added ⌚")

    # ------------- SHOW DATE ---------------
    if message.content.startswith('$showImpDates'):
        lst = ""

        f = open("ImpDates.txt", "a")
        f.close

        f = open("ImpDates.txt", "r")
        lines = f.readlines()

        if len(lines) == 0:
            await message.channel.send("The Important Dates list is empty 😯")
            return

        for todo in lines:
            if(str(todo[0]) == "~"):
                lst += todo
            else:
                lst += todo+"\n"

        embed = discord.Embed(
            title="Important Dates", description="Here is a list of upcoming important dates 💼", color=discord.Color.blue())
        embed.add_field(name="List", value=lst, inline=True)
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
            elif(int(nLine[0]) != int(information[0])):
                f2.write(line)

            else:
                await message.channel.send("The date has been removed :basket:")
                line = "~~"+line+"~~\n"
                f2.write(line)

        f2.close

    # ---------------------------- HELP COMMAND ----------------------------
    if message.content.startswith('$help'):
        embed = discord.Embed(
            title="Commands", description="Here's a list of the commands and how to use them!", color=0x78c6dd)
        embed.add_field(
            name="$addClass", value="$addClass CourseCode>CourseName\nAdd a class to your schedule", inline=False)
        embed.add_field(
            name="$addTextbook", value="$addTextbook TextbookName\nAdd a textbook link to stay organized", inline=False)
        embed.add_field(
            name="$addToDo", value="$addToDo Task\nAdd a task to your to do list", inline=False)
        embed.add_field(
            name="$addImpDates", value="$addImpDates Date>Time>Name\nSave important assignments and dates to be notified", inline=False)
        embed.add_field(
            name="$removeToDo", value="$removeToDo Task\nCross out a task once youre done", inline=False)
        embed.add_field(name="$removeImpDates",
                        value="$remove Date>Time>Name\nRemove an important date once it is over", inline=False)
        embed.add_field(name="$showToDo",
                        value="Lists your to do list", inline=False)
        embed.add_field(name="$showImpDate",
                        value="Lists your important dates", inline=False)
        embed.add_field(name="$clearToDo",
                        value="Clears all items off to do list", inline=False)
        embed.add_field(name="$clearImpDates",
                        value="Clears all items off important dates list", inline=False)
        embed.add_field(name="$addTime_Link",
                        value="$addTime_Link CourseCode>Day>Time>MeetingLink\nAdd a new meeting link for your lectures, by course code", inline=True)
        await message.channel.send(embed=embed)
        
scheduler.start()
client.run(TOKEN)
