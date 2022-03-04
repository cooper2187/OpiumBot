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

    def rounding(self, a):
        if (0.5 <= round(a % 1, 1) and round(a % 1, 1) <= 0.9):
            a = int(a) + 0.5
        elif (0.1 <= round(a % 1, 1) and round(a % 1, 1) <= 0.4):
            a = int(a)
        else:
            a = a
        return a

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == 930080312740950037:
            if payload.emoji.name == '➡️':
                try:
                    nw = datetime.datetime.now()
                    info = {
                        "id": payload.member.id,
                        "name": f"{payload.member.name}#{payload.member.discriminator}",
                        "come": 0,
                        "leave": 0,
                        f"worktime{nw.month}": [None], 
                        f"total{nw.month}": 0
                    }
                    if self.wt.count_documents({"id": payload.member.id}) == 0:
                        self.wt.insert_one(info)
                    if self.wt.find_one({"id": payload.member.id})["come"] != "0":
                        await payload.member.send("Error!")
                    else:
                        self.wt.update_one({"id": payload.member.id}, {"$set": {"come": f"{datetime.datetime.now()}"}})
                        e = discord.Embed(description = f'Дата: **{datetime.datetime.now().strftime("%d.%m.%Y")}**\nВремя: **{datetime.datetime.now().strftime("%H:%M")}**', color = 0x02ff00)
                        e.set_author(name = "VARUS | Вход", icon_url = "https://cdn.discordapp.com/attachments/735452352336756808/928601669686685716/213a003b270cf11f.jpg")
                        await payload.member.send(embed = e)
                except discord.ext.commands.errors.CommandInvokeError:
                    print("Error")
                channel = self.client.get_channel(payload.channel_id)
                msg = await channel.fetch_message(payload.message_id)
                await msg.remove_reaction("➡️", payload.member)
        if payload.message_id == 930080312740950037:
            if payload.emoji.name == '⬅️':
                try:
                    nw = datetime.datetime.now()
                    if self.wt.find_one({"id": payload.member.id})["come"] == "0" or self.wt.find_one({"id": payload.member.id})["leave"] != "0":
                        await payload.member.send("Error!")
                    else:
                        self.wt.update_one({"id": payload.member.id}, {"$set": {"leave": f"{datetime.datetime.now()}"}})
                        st = self.wt.find_one({"id": payload.member.id})
                        a = st['come']
                        b = st['leave']
                        aa = datetime.datetime.strptime(a, "%Y-%m-%d %H:%M:%S.%f")
                        a1 = aa.strftime("%H:%M")
                        a2 = aa.strftime("%d.%m.%Y")
                        bb = datetime.datetime.strptime(b, "%Y-%m-%d %H:%M:%S.%f")
                        b2 = bb.strftime("%d.%m.%Y")
                        delta = datetime.timedelta(minutes = 60)
                        c = bb - aa - delta
                        cc = datetime.datetime.strptime(str(c), "%H:%M:%S.%f")
                        ttl = self.rounding(cc.hour + round(cc.minute/60, 1))
                        e = discord.Embed(description = f'Дата: **{b2}**\nВремя: **{datetime.datetime.now().strftime("%H:%M")}**\nОтработано: **{cc.strftime("%H:%M")}**', color = 0xff0000)
                        e.set_author(name = "VARUS | Выход", icon_url = "https://cdn.discordapp.com/attachments/735452352336756808/928601669686685716/213a003b270cf11f.jpg")
                        self.wt.update_one({"id": payload.member.id}, {"$push": {f"worktime{nw.month}": f"{a2}. Вход: {a1} | Выход: {datetime.datetime.now().strftime('%H:%M')} | Отработано: {cc.strftime('%H:%M')}"}})
                        self.wt.update_one({"id": payload.member.id}, {"$inc": {f"total{nw.month}": ttl}})
                        self.wt.update_one({"id": payload.member.id}, {"$set": {"come": "0"}})
                        self.wt.update_one({"id": payload.member.id}, {"$set": {"leave": "0"}})
                        await payload.member.send(embed = e)
                except discord.ext.commands.errors.CommandInvokeError:
                    payload.member.send("Error!")
                channel = self.client.get_channel(payload.channel_id)
                msg = await channel.fetch_message(payload.message_id)
                await msg.remove_reaction("⬅️", payload.member)
        if payload.message_id == 930080312740950037:
            if payload.emoji.name == '⏲️':
                nw = datetime.datetime.now()
                wl = self.wt.find_one({"id": payload.member.id})[f'worktime{nw.month}']
                ttl = round(self.wt.find_one({"id": payload.member.id})[f'total{nw.month}'], 1)
                llist = []
                i = 1
                for a in wl:
                    llist.append(f"**🔹  {i}. {a}**")
                    i += 1
                e = discord.Embed(description = "\n".join(llist), color = 0x0090ff)
                e.set_author(name = "VARUS | Часы", icon_url = "https://cdn.discordapp.com/attachments/735452352336756808/928601669686685716/213a003b270cf11f.jpg")
                e.set_footer(text = f"\n\nИтого: {ttl} hours", icon_url = payload.member.avatar_url)
                await payload.member.send(embed = e)
                channel = self.client.get_channel(payload.channel_id)
                msg = await channel.fetch_message(payload.message_id)
                await msg.remove_reaction("⏲️", payload.member)
    
    @commands.command()
    async def timelist(self, ctx, m = None):
        nw = datetime.datetime.now()
        if m is None:
            m = nw.month
        else:
            m = m
        wl = self.wt.find_one({"id": ctx.author.id})[f'worktime{m}']
        ttl = round(self.wt.find_one({"id": ctx.author.id})[f'total{m}'], 1)
        llist = []
        i = 1
        for a in wl:
            llist.append(f"**🔹  {i}. {a}**")
            i += 1
        e = discord.Embed(description = "\n".join(llist), color = 0x0090ff)
        e.set_author(name = "VARUS | Часы", icon_url = "https://cdn.discordapp.com/attachments/735452352336756808/928601669686685716/213a003b270cf11f.jpg")
        e.set_footer(text = f"\n\nИтого: {ttl} hours", icon_url = ctx.author.avatar_url)
        await ctx.author.send(embed = e)

def setup(client):
    client.add_cog(Worktime(client))
