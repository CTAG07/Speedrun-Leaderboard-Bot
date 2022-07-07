import asyncio
import discord
from discord.ext import commands
import srcomapi, srcomapi.datatypes as dt
from test import *
class SpeedrunCommands(commands.Cog, name='Speedrun Commands'):

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):  
        '''
        The default check for this cog whenever a command is used. Returns True if the command is allowed.
        '''
        return ctx.author.id == self.bot.author_id

    @commands.command(name="run") 
    async def run(self, ctx):
        while True:
            if not self.categories == []:
                records = await getruns(self)
            await sendformat(self, records, ctx)
            await asyncio.sleep(3600)

    @commands.command(name="setgame") 
    async def setgame(self, ctx, gamename = "apeirophobia"):
        self.api = srcomapi.SpeedrunCom(); self.api.debug = 1
        self.game = self.api.search(srcomapi.datatypes.Game, {"name": gamename})[0]
        if gamename == "apeirophobia":
            self.categories = ["Any%", "Classic", "Any% Nightmare", "Modern", "Reality"]
        else:
            self.categories = []

    @commands.command(name="addcategory") 
    async def addcategory(self, ctx, category):
        if any(i == category for i in self.categories):
            await ctx.send("Category already added!")
        else:
            self.categories.append(category)

    @commands.command(name="removecategory") 
    async def removecategory(self, ctx, category):
        if any(i == category for i in self.categories):
            self.categories.remove(category)
        else:
            await ctx.send("No such category exists")

def setup(bot):
    bot.add_cog(SpeedrunCommands(bot))