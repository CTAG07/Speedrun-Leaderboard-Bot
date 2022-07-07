from datetime import datetime
from time import sleep
import srcomapi, srcomapi.datatypes as dt
import discord
from discord.ext import commands
from srcomapi.datatypes import Category

def convertrun(self, run):
    runid = run.get("id")
    runtime = str((run.get("times")).get("primary_t"))
    print(run)
    userids = run.get("players")
    tempuserids = []
    for i in userids:
        tempuserurl = (i.get("uri")).replace("https://www.speedrun.com/api/v1/", "")
        tempguestcheck = tempuserurl.split("/")
        if any(i == "guests" for i in tempguestcheck):
            tempuser = "Guest/Not Logged In"
        else:
            tempuser = ((self.api.get(tempuserurl)).get("names")).get("international")
        tempuserids.append(tempuser)
    return(tempuserids, runtime)

async def getruns(self, categories = None):
    if categories == None:
        categories = self.categories
    records = []
    strings = [str(i) for i in self.game.categories]
    for i in categories:
        tempnumber = -1
        for j in self.game.categories:
            j = str(j)
            if tempnumber == -1:
                tempnumber = j.find(i)
            if not tempnumber == -1:
                tempnumber = strings.index(j)
                break
        print(tempnumber)
        runs = (self.api.get(endpoint="leaderboards/m1mn0ekd/category/" + self.game.categories[tempnumber].id)).get("runs")
        for d in range(4):
            for f in runs:
                f = f.get("run")
                if len(f.get("players")) == d + 1:
                    tempuserids1, runtime1 = convertrun(self, f)
                    records.append(i)
                    records.append(tempuserids1)
                    records.append(runtime1)
                    break
    return(records)

async def sendformat(self, records, ctx):
    now = datetime.now()
    message = "Records as of " + now.strftime("%d/%m/%Y %H:%M:%S") + ":\n"
    message += "```\n"
    for i in range(int(len(records)/3)):
        tempnumber1 = message.find(str(records[i*3]))
        if not tempnumber1 > -1:
            message += "\n" + records[i*3] + ":\n\n"
        for e in records[i*3+1]:
            if records[i*3+1].index(e) == 0:
                message += e
            else:
                message += " and " + e
        seconds = float(records[i*3+2])
        min, sec = divmod(seconds, 60)
        message += " with a time of " + str(int(min)) + ":" + str(int(sec)) + "\n\n"
    message += "Credits to CTAG07#6191 for making the bot\n"
    message += "```"
    print(message)
    await ctx.send(content = message, delete_after = 3600)
    