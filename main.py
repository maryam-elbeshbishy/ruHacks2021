import os
import discord
import psycopg2
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from dotenv import load_dotenv
import psycopg2
import re
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

# ---------------------------- DATE CONVERSION ------------------------
def date_conversion(date):
    convertedDate = [0,0,0]
    dateSplit = date.split("/")
    month = dateSplit[0].lstrip('0')
    day = dateSplit[1].lstrip('0')
    year = dateSplit[2]

    convertedDate[0] = month
    convertedDate[1] = day
    convertedDate[2] = year

    return convertedDate
    
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

# ---------------------------- NOTIFICATION ALERTS------------------------

# ------------- CLASS NOTIFICATION -------------------
async def class_notification(acronym, day, hour, link):
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

# ------------- IMPORTANT DATE NOTIFICAITION ---------------
async def impDate_notification(title, date, hour):
    channel = client.get_channel(838199083491524659)

    embed=discord.Embed(title=":alarm_clock: You have {} right now!".format(title), description="{} at {}".format(date,hour), color=0xb0d6ee)
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
        try:
            userInput = message.content[10:]
            information = userInput.split(seperator)
            acronym = information[0].upper().strip()
            title = information[1].title().strip()
            if len(acronym)==0 or len(title)==0:
                await message.channel.send("🩹 **Please use the command as so: $addClass CODE>TITLE**\nFor more information use $help")
                return
            cur.execute("""
            INSERT INTO EduBot VALUES
            ('{}','{}',NULL,NULL,NULL,NULL);
            """.format(acronym, title))
            
            await message.channel.send("The class has been added 🏫")
            show_dataBase()
        except:
            await message.channel.send("🩹 **Please use the command as so: $addClass CODE>TITLE**\nFor more information use $help")


    # ---------------------------- REMOVING CLASS TITLE + ACRONYM ----------------------------
    if message.content.startswith('$removeClass'):
        try:
            userInput = message.content[13:]
            information = userInput.split(seperator)
            acronym = information[0].upper().strip()
            if len(acronym)==0:
                await message.channel.send("🩹 **Please use the command as so: $removeClass CODE**\nFor more information use $help")
                return
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
        except:
            await message.channel.send("🩹 **Please use the command as so: $removeClass CODE**\nFor more information use $help")



        # show_dataBase()

    # ---------------------------- ADDING CLASS INFORMATION ----------------------------
    if message.content.startswith('$addTime_Link'):
        
        try:
            userInput = message.content[14:]
            information = userInput.split(seperator)
            acronym = information[0].strip().upper()
            day = information[1].strip()
            hour = information[2]
            link = information[3].strip()

            patterns =["((1[0-2])|[1-9]):[0-5][0-9] (A|P)M","((m|M)on|(t|T)ues|(w|W)ednes|(T|t)hurs|(f|F)ri)day"]
    
            res1 = re.match(patterns[0],hour)
            res2 = re.match(patterns[1],day)


            conv_hour = time_conversion(hour)
            conv_day = day_conversion(day)

            if len(acronym)==0 or len(day)==0 or len(hour)==0 or len(link)==0:
                await message.channel.send("🩹 **Please use the command as so: $addTime_Link CODE>DAY>TIME>MEETINGLINK**\n*Be sure to format the time as so: 00:00 AM or 00:00 PM*\nFor more information use $help")
                return

            if not res2: 
                await message.channel.send("🩹 **Please input a valid day and try again. Ex.(Monday)**")
                return
            if not res1:
                await message.channel.send("🩹 **Please input a valid time and try again.**")
                return

            if not check_code(acronym):
                await message.channel.send("There is no information for '{}' 😯\n Use $addClass to add some.".format(acronym))
                return

            scheduler.add_job(class_notification, CronTrigger(hour=conv_hour[0], minute=conv_hour[1], day_of_week=conv_day), id=acronym, args=(acronym, day, hour, link))

            cur.execute("""
            UPDATE EduBot
            SET meetingLink = '{}', dayWeek = '{}', timeWeek = '{}'
            WHERE courseCode = '{}';
            """.format(link, day, hour, acronym))

            await message.channel.send("The class information has been added 🏫")
        except:
            print("here4")
            await message.channel.send("🩹 **Please use the command as so: $addTime_Link CODE>DAY>TIME>MEETINGLINK**\n*Be sure to format the time as so: 00:00 AM or 00:00 PM*\nFor more information use $help")

    # ---------------------------- ADD TEXTBOOK ----------------------------
    if message.content.startswith('$addTextbook'):
        try:
            userInput = message.content[13:]
            information = userInput.split(seperator)
            acronym = information[0].upper().strip()
            textbook = information[1].strip()
            if len(acronym)==0 or len(textbook)==0:
                await message.channel.send("🩹 **Please use the command as so: $addTextbook CODE>TEXTBOOK LINK**\nFor more information use $help")
                return

            if not check_code(acronym):
                await message.channel.send("There is no information for '{}' 😯\n Use $addClass to add some.".format(acronym))
                return

            cur.execute("""
            UPDATE EduBot
            SET textBook = '{}'
            WHERE courseCode = '{}';
            """.format(textbook, acronym))
            await message.channel.send("The textbook has been added 📚")

        except:
            await message.channel.send("🩹 **Please use the command as so: $addTextbook CODE>TEXTBOOK LINK**\nFor more information use $help")



    # ---------------------------- GET CLASS TITLE ----------------------------
    if message.content.startswith('$getClassTitle'):
        try: 
            userInput = message.content[15:]
            information = userInput.split(seperator)
            acronym = information[0].upper().strip()

            if len(acronym)==0:
                await message.channel.send("🩹 **Please use the command as so: $getClassTitle CODE**\nFor more information use $help")
                return
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
                    await message.channel.send("There no is Class title for {} 😯".format(acronym))
            else:
                await message.channel.send("ℹ The class title of {} is: {}.".format(acronym, title[0][0]))
        except:
            await message.channel.send("🩹 **Please use the command as so: $getClassTitle CODE**\nFor more information use $help")


    # ---------------------------- GET CLASSCODE ---------------------------- 
    if message.content.startswith('$getClassCode'):   
        try:
            userInput = message.content[14:]
            information = userInput.split(seperator)
            check = information[0].title().strip()
            if len(str(check))==0:
                await message.channel.send("🩹 **Please use the command as so: $getClassCode TITLE**\nFor more information use $help")
                return
            cur.execute("""
                SELECT courseCode FROM EduBot 
                WHERE courseName = '{}';
            """.format(check))
            code = cur.fetchall()

            if len(code) == 0:
                await message.channel.send("There no is course code for {} 😯".format(check))
                return
           
            await message.channel.send("ℹ The course code of {} is: {}.".format(check, code[0][0]))
        except:
            await message.channel.send("🩹 **Please use the command as so: $getClassCode TITLE**\nFor more information use $help")


    # ---------------------------- GET MEETINGLINK ----------------------------
    if message.content.startswith('$getMeetingLink'):
        try:
            userInput = message.content[16:]
            information = userInput.split(seperator)
            acronym = information[0].upper().strip()
            if len(acronym)==0:
                        await message.channel.send("🩹 **Please use the command as so: $getMeetingLink CODE**\nFor more information use $help")
                        return
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
        except:
            await message.channel.send("🩹 **Please use the command as so: $getMeetingLink CODE**\nFor more information use $help")


    # ---------------------------- GET TEXTBOOK ----------------------------
    if message.content.startswith('$getTextbook'):
        try:
            userInput = message.content[13:]
            information = userInput.split(seperator)
            acronym = information[0].upper().strip()

            if len(acronym)==0:
                    await message.channel.send("🩹 **Please use the command as so: $getTextbook CODE**\nFor more information use $help")
                    return

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
        except:
            await message.channel.send("🩹 **Please use the command as so: $getTextbook CODE**\nFor more information use $help")

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
        try:
            userInput = message.content[9:]
            information = userInput.split(seperator)
            print(information)
            if len(information[0])==0:
                await message.channel.send("🩹 **Please use the command as so: $addToDo** *Task you want to complete...*\nFor more information use $help")
                return
            f = open("toDoList.txt", "a")
            count = len(open("toDoList.txt").readlines()) + 1
            for toDo in information:
                f.write(str(count) + ") " + toDo + "\n")
                count += 1
            f.close
            await message.channel.send("The task(s) has been added ⌚")
        except:
            await message.channel.send("🩹 **Please use the command as so: $addToDo** *Task you want to complete...*\nFor more information use $help")


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
        try:
            userInput = message.content[11:]
            information = userInput.split(seperator)
            if len(information[0])==0:
                await message.channel.send("🩹 **Please use the command as so: $removeToDo TASK NUMBER** \nFor more information use $help")
                return
            f = open("toDoList.txt", "r")
            lines = f.readlines()
            f.close

            if int(information[0])>len(lines):
                await message.channel.send("🩹 **Please enter a valid task number.**")
                return

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
        except:
            await message.channel.send("🩹 **Please use the command as so: $removeToDo TASK NUMBER** \nFor more information use $help")


    # ------------- CLEAR TO DO ---------------
    if message.content.startswith('$clearToDo'):
        # print("REACHED")
        open('toDoList.txt', 'w').close()
        await message.channel.send("Todo List has been cleared✅")

    # ---------------------------- IMPORTANT DATES ----------------------------

    # ------------- ADD DATE ---------------
    if message.content.startswith('$addImpDates'):
        try:
            userInput = message.content[13:]
            information = userInput.split(seperator)
            title = information[0]
            date = information[1]
            hour = information[2]

            conv_date = date_conversion(date)
            conv_hour = time_conversion(hour)
             
            patterns =["^((((0[13578])|([13578])|(1[02]))[\/](([1-9])|([0-2][0-9])|(3[01])))|(((0[469])|([469])|(11))[\/](([1-9])|([0-2][0-9])|(30)))|((2|02)[\/](([1-9])|([0-2][0-9]))))[\/]\d{4}$|^\d{4}$","((1[0-2])|[1-9]):[0-5][0-9] (A|P)M"]

            res1 = re.match(patterns[0],date)
            res2 = re.match(patterns[1],hour)
    

            if len(title)==0 or len(date)==0 or len(hour)==0:
                await message.channel.send("🩹 **Please use the command as so: $addImpDates TITLE>MM/DD/YYYY>00:00 PM** \n*Be sure to format the time as so: 00:00 AM or 00:00 PM*\nFor more information use $help")
                return

            if not res1:
                await message.channel.send("🩹 **Please enter a valid date in the following format MM/DD/YYYY**")
                return
            if not res2:
                await message.channel.send("🩹 **Please enter a valid time.**\n*Be sure to format the time as so: 00:00 AM or 00:00 PM*")
                return

            f = open("ImpDates.txt", "a")
            count = len(open("ImpDates.txt").readlines()) + 1
            f.write(str(count) + ") " + title +
                    " [ " + date + " @ " + hour + " ]" + "\n")
            count += 1
            f.close

            scheduler.add_job(impDate_notification, CronTrigger(hour=conv_hour[0], minute=conv_hour[1], month=conv_date[0], day=conv_date[1], year=conv_date[2]), args=(title, date, hour))
            await message.channel.send("The important date has been added ⌚")
        except:
            await message.channel.send("🩹 **Please use the command as so: $addImpDates TITLE>MM/DD/YYYY>00:00 PM** \n*Be sure to format the time as so: 00:00 AM or 00:00 PM*\nnFor more information use $help")


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
        try:
            userInput = message.content[16:]
            information = userInput.split(seperator)

            if len(information[0])==0 :
                await message.channel.send("🩹 **Please use the command as so: $removeImpDates NUMBER** \nFor more information use $help")
                return

            f = open("ImpDates.txt", "r")
            lines = f.readlines()
            f.close

            if int(information[0])>len(lines):
                await message.channel.send("🩹 **Please enter a valid number.**")
                return

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
        except:
            await message.channel.send("🩹 **Please use the command as so: $removeImpDates NUMBER** \nFor more information use $help")


    # ---------------------------- HELP COMMAND ----------------------------
    if message.content.startswith('$help'):
        embed = discord.Embed(title=":sos:  COMMANDS", description="Here's a list of the commands and how to use them!", color=0x78c6dd)
        
        embed.add_field(name=":green_circle: ADDING", value="- - - - - - - - -", inline=False)
        embed.add_field(name="$addClass", value="$addClass CourseCode>CourseName\nAdd a class to your schedule", inline=False)
        embed.add_field(name="$addTime_Link", value="$addTime_Link CourseCode>Day>Time>MeetingLink\nDay: Monday/Tuesday/Wednesday/Thursday/Saturday/Sunday\n Time: hh:mm AM/PM\nAdd a time & meeting link for your lectures, by course code", inline=True)
        embed.add_field(name="$addTextbook", value="$addTextbook CourseCode>TextbookLink\nAdd a textbook link to stay organized", inline=False)
        embed.add_field(name="$addToDo", value="$addToDo Task\nAdd a task to your to do list", inline=False)
        embed.add_field(name="$addImpDates", value="$addImpDates Title>Date>Time\nDate: mm/dd/yyyy\n Time: hh:mm AM/PM\nSave important assignments and dates to be notified", inline=False)

        embed.add_field(name=":red_circle: REMOVING", value="- - - - - - - - - - - -", inline=False)
        embed.add_field(name="$removeClass", value="$removeClass CourseCode\nRemove a class to your schedule", inline=False)
        embed.add_field(name="$removeToDo", value="$removeToDo Task\nCross out a task once youre done", inline=False)
        embed.add_field(name="$removeImpDates", value="$remove Date>Time>Name\nRemove an important date once it is over", inline=False)
        embed.add_field(name="$clearToDo",value="Clears all items off to do list", inline=False)
        embed.add_field(name="$clearImpDates",value="Clears all items off important dates list", inline=False) 
        embed.add_field(name="$clearSchedule",value="Clears all items off your weekly schedule", inline=False) 

        embed.add_field(name=":yellow_circle: RETRIEVING", value="- - - - - - - - - - - -", inline=False)
        embed.add_field(name="$getSchedule", value="$getSchedule CourseCode\nGet your weekly schedule of your courses", inline=False)
        embed.add_field(name="$getClassTitle", value="$getClassTitle CourseCode\nGet the class title of a course", inline=False)
        embed.add_field(name="$getClassCode", value="$getClassCode CourseName\nGet the class title of a course", inline=False)
        embed.add_field(name="$gettextbook", value="$getTextbook CourseCode\nGet the textbook link of a course", inline=False)
        embed.add_field(name="$getMeetingLink", value="$getMeetingLink CourseCode\nGet the meeting link of a course", inline=False)
        embed.add_field(name="$showToDo", value="Lists your to do list", inline=False)
        embed.add_field(name="$showImpDate",value="Lists your important dates", inline=False)

        await message.channel.send(embed=embed)
        
scheduler.start()
client.run(TOKEN)
