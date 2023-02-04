import disnake
from disnake.ext import commands
import os
import datetime
import pymongo
from pymongo import MongoClient

class Worktime(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cluster = MongoClient("mongodb+srv://andrewnobot:xuInmV8QmD9GRR5c@cluster0.28biu.mongodb.net/opiumdb?retryWrites=true&w=majority")
        self.wt = self.cluster.work.worktime

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == 930080312740950037:
            if payload.emoji.name == '➡️':
                try:
                    nw = datetime.datetime.now()
                    info = {
                        "id": payload.member.id,
                        "name": f"{payload.member.name}#{payload.member.discriminator}",
                        "come": "0",
                        "leave": "0",
                        f"worktime{nw.month}": [], 
                        f"total{nw.month}": 0
                    }
                    if self.wt.count_documents({"id": payload.member.id}) == 0:
                        self.wt.insert_one(info)
                    if self.wt.find_one({"id": payload.member.id})["come"] != "0":
                        await payload.member.send("Error!")
                    else:
                        def entrance(self, a):
                            if a.minute >= 0 and a.minute <= 14:
                                b = f"{a.hour}:15:00.0"
                            elif a.minute >= 15 and a.minute <= 29:
                                b = f"{a.hour}:30:00.0"
                            elif a.minute >= 30 and a.minute <= 44:
                                b = f"{a.hour}:45:00.0"
                            elif a.minute >= 45 and a.minute <= 59:
                                b = f"{a.hour + 1}:00:00.0"
                            else:
                                pass
                            return a.strftime("%Y-%m-%d ") + b
                        entr = entrance(self, datetime.datetime.now())
                        self.wt.update_one({"id": payload.member.id}, {"$set": {"come": entr}})
                        aa = datetime.datetime.strptime(entr, "%Y-%m-%d %H:%M:%S.%f")
                        a1 = aa.strftime("%H:%M")
                        delta = datetime.timedelta(minutes = 750)
                        c = aa + delta
                        cc = datetime.datetime.strptime(str(c), "%Y-%m-%d %H:%M:%S")
                        e = disnake.Embed(description = f'Дата: **{datetime.datetime.now().strftime("%d.%m.%Y")}**\nВремя: **{a1}**', color = 0x02ff00)
                        e.set_author(name = "VARUS | Вход", icon_url = "https://media.discordapp.net/attachments/735452352336756808/928601669686685716/213a003b270cf11f.jpg")
                        e.set_footer(text = f"Рекомендуемое время ухода: {cc.strftime('%H:%M')}")
                        await payload.member.send(embed = e)
                except disnake.ext.commands.errors.CommandInvokeError:
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
                        def out(self, a):
                            if a.minute >= 0 and a.minute <= 14:
                                b = f"{a.hour}:00:00.0"
                            elif a.minute >= 15 and a.minute <= 29:
                                b = f"{a.hour}:15:00.0"
                            elif a.minute >= 30 and a.minute <= 44:
                                b = f"{a.hour}:30:00.0"
                            elif a.minute >= 45 and a.minute <= 59:
                                b = f"{a.hour}:45:00.0"
                            else:
                                pass
                            return a.strftime("%Y-%m-%d ") + b
                        ext = out(self, datetime.datetime.now())
                        self.wt.update_one({"id": payload.member.id}, {"$set": {"leave": ext}})
                        st = self.wt.find_one({"id": payload.member.id})
                        a = st['come']
                        b = st['leave']
                        aa = datetime.datetime.strptime(a, "%Y-%m-%d %H:%M:%S.%f")
                        a1 = aa.strftime("%H:%M")
                        a2 = aa.strftime("%d.%m.%Y")
                        bb = datetime.datetime.strptime(b, "%Y-%m-%d %H:%M:%S.%f")
                        b1 = bb.strftime("%H:%M")
                        b2 = bb.strftime("%d.%m.%Y")
                        delta = datetime.timedelta(minutes = 90)
                        c = bb - aa - delta
                        cc = datetime.datetime.strptime(str(c), "%H:%M:%S")
                        ttl = cc.hour + round(cc.minute/60, 2)
                        e = disnake.Embed(description = f'Дата: **{b2}**\nВремя: **{b1}**', color = 0xff0000)
                        e.set_author(name = "VARUS | Выход", icon_url = "https://media.discordapp.net/attachments/735452352336756808/928601669686685716/213a003b270cf11f.jpg")
                        e.set_footer(text = f'Отработано: {ttl}')
                        self.wt.update_one({"id": payload.member.id}, {"$push": {f"worktime{nw.month}": f"{a2}. Вход: {a1} | Выход: {b1} | Отработано: {ttl}"}})
                        self.wt.update_one({"id": payload.member.id}, {"$inc": {f"total{nw.month}": ttl}})
                        self.wt.update_one({"id": payload.member.id}, {"$set": {"come": "0"}})
                        self.wt.update_one({"id": payload.member.id}, {"$set": {"leave": "0"}})
                        await payload.member.send(embed = e)
                except disnake.ext.commands.errors.CommandInvokeError:
                    payload.member.send("Error!")
                channel = self.client.get_channel(payload.channel_id)
                msg = await channel.fetch_message(payload.message_id)
                await msg.remove_reaction("⬅️", payload.member)
        if payload.message_id == 930080312740950037:
            if payload.emoji.name == '⏲️':
                nw = datetime.datetime.now()
                wl = self.wt.find_one({"id": payload.member.id})[f'worktime{nw.month}']
                ttl = round(self.wt.find_one({"id": payload.member.id})[f'total{nw.month}'], 2)
                llist = []
                i = 1
                for a in wl:
                    llist.append(f"**🔹  {i}. {a}**")
                    i += 1
                e = disnake.Embed(description = "\n".join(llist), color = 0x0090ff)
                e.set_author(name = "VARUS | Часы", icon_url = "https://media.discordapp.net/attachments/735452352336756808/928601669686685716/213a003b270cf11f.jpg")
                e.set_footer(text = f"\n\nИтого: {ttl} hours", icon_url = payload.member.avatar)
                await payload.member.send(embed = e)
                channel = self.client.get_channel(payload.channel_id)
                msg = await channel.fetch_message(payload.message_id)
                await msg.remove_reaction("⏲️", payload.member)
    
    # @commands.command()
    # async def timelist(self, ctx, m = None):
    #     nw = datetime.datetime.now()
    #     if m is None:
    #         m = nw.month
    #     else:
    #         m = m
    #     wl = self.wt.find_one({"id": ctx.author.id})[f'worktime{m}']
    #     ttl = round(self.wt.find_one({"id": ctx.author.id})[f'total{m}'], 1)
    #     llist = []
    #     i = 1
    #     for a in wl:
    #         llist.append(f"**🔹  {i}. {a}**")
    #         i += 1
    #     e = disnake.Embed(description = "\n".join(llist), color = 0x0090ff)
    #     e.set_author(name = "VARUS | Часы", icon_url = "https://cdn.disnakeapp.com/attachments/735452352336756808/928601669686685716/213a003b270cf11f.jpg")
    #     e.set_footer(text = f"\n\nИтого: {ttl} hours", icon_url = ctx.author.avatar_url)
    #     await ctx.author.send(embed = e)

def setup(client):
    client.add_cog(Worktime(client))