import discord
from discord.ext import commands
import os
import datetime
import pymongo
from pymongo import MongoClient

class Worktime(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cluster = MongoClient("mongodb+srv://andrewnobot:xuInmV8QmD9GRR5c@cluster0.28biu.mongodb.net/opiumdb?retryWrites=true&w=majority")
        self.wt = self.cluster.work.worktime

    @commands.command()
    async def come(self, ctx):
        info = {
            "id": ctx.author.id,
            "name": f"{ctx.author.name}#{ctx.author.discriminator}",
            "come": 0,
            "leave": 0,
            "worktime": [0]
        }
        if self.wt.count_documents({"id": ctx.author.id}) == 0:
            self.wt.insert_one(info)
        self.wt.update_one({"id": ctx.author.id}, {"$set": {"come": f"{datetime.datetime.now()}"}})
        e = discord.Embed(description = f'Дата: **{datetime.datetime.now().strftime("%d.%m.%Y")}**\nВремя прихода: **{datetime.datetime.now().strftime("%H:%M")}**')
        await ctx.send(embed = e)

    @commands.command()
    async def leave(self, ctx):
        self.wt.update_one({"id": ctx.author.id}, {"$set": {"leave": f"{datetime.datetime.now()}"}})
        st = self.wt.find_one({"id": ctx.author.id})
        a = st['come']
        b = st['leave']
        aa = datetime.datetime.strptime(a, "%Y-%m-%d %H:%M:%S.%f")
        a1 = aa.strftime("%H:%M")
        a2 = aa.strftime("%d.%m.%Y")
        bb = datetime.datetime.strptime(b, "%Y-%m-%d %H:%M:%S.%f")
        c = bb - aa
        cc = datetime.datetime.strptime(str(c), "%H:%M:%S.%f")
        e = discord.Embed(description = f'Дата: **{a2}**\nВермя прихода: **{a1}**\nВремя ухода: **{datetime.datetime.now().strftime("%H:%M")}**\nОтработано: **{cc.strftime("%H:%M")}**')
        self.wt.update_one({"id": ctx.author.id}, {"$push": {"worktime": f"{a2}. Приход: {a1} | Уход: {datetime.datetime.now().strftime('%H:%M')} | Отработано: {cc.strftime('%H:%M')}"}})
        await ctx.send(embed = e)

def setup(client):
    client.add_cog(Worktime(client))