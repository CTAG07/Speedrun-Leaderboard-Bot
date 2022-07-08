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

async def getruns(self):
    categories = []
    records = []
    for i in self.game.categories:
        if i.type == "per-game":
            categories.append(i)
    for i in categories:
        runs = self.api.get(endpoint="leaderboards/m1mn0ekd/category/" + i.id)
        runs = runs.get("runs")
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
        tempnumber1 = message.find(records[i*3].name)
        if not tempnumber1 > -1:
            message += "\n" + records[i*3].name + ":\n\n"
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
    await ctx.send(content = message, delete_after = 3600)
    