import discord
from discord.ext import commands
import os
import datetime
import pymongo
from pymongo import MongoClient

from worktime import rounding

class Worktime(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cluster = MongoClient("mongodb+srv://andrewnobot:xuInmV8QmD9GRR5c@cluster0.28biu.mongodb.net/opiumdb?retryWrites=true&w=majority")
        self.wt = self.cluster.work.worktime

    def rounding(a):
        if (0.5 <= round(a % 1, 1) and round(a % 1, 1) <= 0.9):
            a = int(a) + 0.5
        elif (0.1 <= round(a % 1, 1) and round(a % 1, 1) <= 0.4):
            a = int(a)
        else:
            a = a
        return a

    @commands.Cog.listener
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == 930080312740950037:
            if payload.emoji.name == '➡️':
                try:
                    info = {
                        "id": payload.member.id,
                        "name": f"{payload.member.name}#{payload.member.discriminator}",
                        "come": 0,
                        "leave": 0,
                        "worktime": [0], 
                        "total": 0
                    }
                    if self.wt.count_documents({"id": payload.member.id}) == 0:
                        self.wt.insert_one(info)
                    if self.wt.find_one({"id": payload.member.id})["come"] != "0":
                        await payload.member.send("Error!")
                    else:
                        self.wt.update_one({"id": payload.member.id}, {"$set": {"come": f"{datetime.datetime.now()}"}})
                        e = discord.Embed(description = f'Дата: **{datetime.datetime.now().strftime("%d.%m.%Y")}**\nВремя: **{datetime.datetime.now().strftime("%H:%M")}**', color = 0x02ff00)
                        e.set_author(name = "VARUS | Приход", icon_url = "https://cdn.discordapp.com/attachments/735452352336756808/928601669686685716/213a003b270cf11f.jpg")
                        await payload.member.send(embed = e)
                except discord.ext.commands.errors.CommandInvokeError:
                    print("Error")
                channel = self.client.get_channel(payload.channel_id)
                msg = await channel.fetch_message(payload.message_id)
                await msg.remove_reaction("➡️", payload.member)
        if payload.message_id == 930080312740950037:
            if payload.emoji.name == '⬅️':
                try:
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
                        delta = datetime.timedelta(minutes = 90)
                        c = bb - aa - delta
                        cc = datetime.datetime.strptime(str(c), "%H:%M:%S.%f")
                        ttl = rounding(cc.hour + round(cc.minute/60, 1))
                        e = discord.Embed(description = f'Дата: **{a2}**\nВермя прихода: **{a1}**\nВремя ухода: **{datetime.datetime.now().strftime("%H:%M")}**\nОтработано: **{cc.strftime("%H:%M")}**', color = 0xff0000)
                        e.set_author(name = "VARUS | Уход", icon_url = "https://cdn.discordapp.com/attachments/735452352336756808/928601669686685716/213a003b270cf11f.jpg")
                        self.wt.update_one({"id": payload.member.id}, {"$push": {"worktime": f"{a2}. Приход: {a1} | Уход: {datetime.datetime.now().strftime('%H:%M')} | Отработано: {cc.strftime('%H:%M')}"}})
                        self.wt.update_one({"id": payload.member.id}, {"$inc": {"total": ttl}})
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
                wl = self.wt.find_one({"id": payload.member.id})['worktime']
                ttl = round(self.wt.find_one({"id": payload.member.id})['total'], 1)
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

def setup(client):
    client.add_cog(Worktime(client))