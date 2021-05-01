import os
import discord
import psycopg2
from discord.ext import commands, tasks
from dotenv import load_dotenv

 # ---------------------------- ADDING CLASS TITLE + ACRONYM ----------------------------
import psycopg2

conn = psycopg2.connect(
database='whole-mink-215.edubotdb',
user='maryam',
password= 'Oulnmt4wZqd-bzwR',
host='free-tier5.gcp-europe-west1.cockroachlabs.cloud',
port=26257
)
conn.set_session(autocommit=True)


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

conn =conn = psycopg2.connect(
database='whole-mink-215.edubotdb',
user='maryam',
password= 'Oulnmt4wZqd-bzwR',
host='free-tier5.gcp-europe-west1.cockroachlabs.cloud',
port=26257
)
cur = conn.cursor()

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



@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    cur.execute( """
    CREATE TABLE IF NOT EXISTS EduBot (
    courseCode VARCHAR,
    courseName VARCHAR,
    textBook VARCHAR,
    meetingLink VARCHAR,
    dayWeek VARCHAR,
    timeWeek VARCHAR
    );
    """)

@client.event
async def on_message(message):
    seperator = ">"
    
    if message.author == client.user:
        return    

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
        """.format(acronym,title))
        await message.channel.send("The class has been added 🏫")
        show_dataBase()

    # ---------------------------- ADDING CLASS INFORMATION ----------------------------
    if message.content.startswith('$addTime_Link'):
        userInput = message.content[14:]
        information = userInput.split(seperator)
        acronym = information[0].strip().upper()
        day = information[1].strip()
        hour = information[2]
        link = information[3].strip()

        if not check_code(acronym):
            await message.channel.send("There is no information for '{}' 😯\n Use $addClass to add some.".format(acronym))
            return

        cur.execute("""
        UPDATE EduBot
        SET meetingLink = '{}', dayWeek = '{}', timeWeek = '{}'
        WHERE courseCode = '{}';
        """.format(link,day,hour,acronym))
        

        show_dataBase()
        await message.channel.send(acronym)
        await message.channel.send(day)
        await message.channel.send(hour)
        await message.channel.send(link)
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
        """.format(textbook,acronym))
        await message.channel.send("The textbook has been added 📚")

    
    if "chick" in message.content:
        await message.channel.send("hello")

    # ---------------------------- RETRIEVING DATA FROM DB----------------------------

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
            await message.channel.send("ℹ The course title of {} is: {}.".format(acronym,title[0][0]))


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
            await message.channel.send("ℹ The course code of {} is: {}.".format(title,code[0][0]))
    
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
            await message.channel.send("🔗 The meeting link for {} is: {}".format(acronym,link[0][0]))
           
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
            await message.channel.send("🔗 The textbook link for {} is: {}".format(acronym,text[0][0]))

    if message.content.startswith('$getSchedule'):
        lst = ""
        cur.execute("""
            SELECT courseCode, courseName, dayWeek, timeWeek FROM EduBot;
        """)   
        information = cur.fetchall()
        conn.commit()

        if len(information) == 0:
            lst += "There are no classes this week 😯"

        for c in range(len(information)):
                lst += ("{} {} [ {} @ {}]\n".format(information[c][0], information[c][1], information[c][2], information[c][3]))

        embed=discord.Embed(title="Weekly Schedule", description="Here is your weekly schedule 💼", color=discord.Color.blue())
        embed.add_field(name="This Week",value=lst,inline=True)
        await message.channel.send(embed=embed)

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