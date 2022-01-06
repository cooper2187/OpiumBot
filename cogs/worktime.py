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
            if self.wt.find_one({"id": ctx.author.id})["come"] != "0":
                await ctx.send("Error!")
            else:
                info = {
                    "id": ctx.author.id,
                    "name": f"{ctx.author.name}#{ctx.author.discriminator}",
                    "come": 0,
                    "leave": 0,
                    "worktime": [0], 
                    "total": 0
                }
                if self.wt.count_documents({"id": ctx.author.id}) == 0:
                    self.wt.insert_one(info)
                self.wt.update_one({"id": ctx.author.id}, {"$set": {"come": f"{datetime.datetime.now()}"}})
                e = discord.Embed(description = f'Дата: **{datetime.datetime.now().strftime("%d.%m.%Y")}**\nВремя: **{datetime.datetime.now().strftime("%H:%M")}**', color = 0x02ff00)
                e.set_author(name = "VARUS | Приход", icon_url = "https://cdn.discordapp.com/attachments/735452352336756808/928601669686685716/213a003b270cf11f.jpg")
                await ctx.send(embed = e)

        @commands.command()
        async def leave(self, ctx):
            if self.wt.find_one({"id": ctx.author.id})["come"] == "0" or self.wt.find_one({"id": ctx.author.id})["leave"] != "0":
                await ctx.send("Error!")
            else:
                self.wt.update_one({"id": ctx.author.id}, {"$set": {"leave": f"{datetime.datetime.now()}"}})
                st = self.wt.find_one({"id": ctx.author.id})
                a = st['come']
                b = st['leave']
                aa = datetime.datetime.strptime(a, "%Y-%m-%d %H:%M:%S.%f")
                a1 = aa.strftime("%H:%M")
                a2 = aa.strftime("%d.%m.%Y")
                bb = datetime.datetime.strptime(b, "%Y-%m-%d %H:%M:%S.%f")
                delta = datetime.timedelta(minutes = 90)
                c = bb - aa - delta
                cc = datetime.datetime.strptime(str(c), "%H:%M:%S.%f")
                ttl = cc.hour + round(cc.minute/60, 1)
                e = discord.Embed(description = f'Дата: **{a2}**\nВермя прихода: **{a1}**\nВремя ухода: **{datetime.datetime.now().strftime("%H:%M")}**\nОтработано: **{cc.strftime("%H:%M")}**', color = 0xff0000)
                e.set_author(name = "VARUS | Уход", icon_url = "https://cdn.discordapp.com/attachments/735452352336756808/928601669686685716/213a003b270cf11f.jpg")
                self.wt.update_one({"id": ctx.author.id}, {"$push": {"worktime": f"{a2}. Приход: {a1} | Уход: {datetime.datetime.now().strftime('%H:%M')} | Отработано: {cc.strftime('%H:%M')}"}})
                self.wt.update_one({"id": ctx.author.id}, {"$inc": {"total": ttl}})
                self.wt.update_one({"id": ctx.author.id}, {"$set": {"come": "0"}})
                self.wt.update_one({"id": ctx.author.id}, {"$set": {"leave": "0"}})
                await ctx.send(embed = e)

        @commands.command()
        async def timelist(self, ctx):
            wl = self.wt.find_one({"id": ctx.author.id})['worktime']
            ttl = round(self.wt.find_one({"id": ctx.author.id})['total'], 1)
            llist = []
            i = 1
            for a in wl:
                llist.append(f"**🔹  {i}. {a}**")
                i += 1
            e = discord.Embed(description = "\n".join(llist), color = 0x0090ff)
            e.set_author(name = "VARUS | Часы", icon_url = "https://cdn.discordapp.com/attachments/735452352336756808/928601669686685716/213a003b270cf11f.jpg")
            e.set_footer(text = f"\n\nTotal: {ttl} hours", icon_url = ctx.author.avatar_url)
            await ctx.send(embed = e)

def setup(client):
    client.add_cog(Worktime(client))