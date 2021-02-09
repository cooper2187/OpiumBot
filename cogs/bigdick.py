import discord
from discord.ext import commands
import os
import asyncio
import pymongo
from pymongo import MongoClient
import time
import datetime
from random import randint

class Dick(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cluster = MongoClient("mongodb+srv://andrewnobot:xuInmV8QmD9GRR5c@cluster0.28biu.mongodb.net/opiumdb?retryWrites=true&w=majority", connect = False)
        self.game = self.cluster.opiumdb.dsdickcoll
        self.prx = self.cluster.opiumdb.prefixcoll

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not self.game.count_documents({"guild_id": member.guild.id, "user_id": member.id}) == 0:
            self.game.update_one({"guild_id": member.guild.id, "user_id": member.id}, {"$set": {"in_game": 0}})
        else:
            pass

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if not self.game.count_documents({"guild_id": member.guild.id, "user_id": member.id}) == 0:
            self.game.update_one({"guild_id": member.guild.id, "user_id": member.id}, {"$set": {"in_game": 1}})
        else:
            pass


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        ch = {
            "guild_id": guild.id,
            "guild_name": guild.name,
            "channel_id": 0,
            "lang": "Ukr"
        }
        if self.game.count_documents({"guild_id": guild.id}) == 0:
            self.game.insert_one(ch)

    @commands.command()
    async def set_channel(self, ctx, channel: discord.TextChannel = None):
        prefix = self.prx.find_one({"_id": ctx.guild.id})["prefix"]
        if channel is None:
            await ctx.send(embed = discord.Embed(description = f'**{prefix}set_channel [#TextChannel]** - Установить канал для игры\n**{prefix}set_channel #TextChannelName**', color = 0x667676))
        else:
            self.game.update_one({"guild_id": ctx.guild.id}, {"$set": {"channel_id": channel.id}})
            await ctx.send(embed = discord.Embed(description = f"**Channel for Big-Dick-Game was changed: {channel.name}**", color = 0x8eac60))


    @commands.command()
    async def set_lang(self, ctx, lang = None):
        prefix = self.prx.find_one({"_id": ctx.guild.id})["prefix"]
        if lang is None:
            await ctx.send(embed = discord.Embed(description = f'**{prefix}set_lang [rus/ukr]** - Установить язык(Русский/Украинский)\n**{prefix}set_lang rus**', color = 0x667676))
        elif lang == "rus":
            self.game.update_one({"guild_id": ctx.guild.id}, {"$set": {"lang": "Rus"}})
            await ctx.send(embed = discord.Embed(description = "**Language for Big-Dick-Game was changed: Russian**", color = 0x8eac60))
        elif lang == "ukr":
            self.game.update_one({"guild_id": ctx.guild.id}, {"$set": {"lang": "Ukr"}})
            await ctx.send(embed = discord.Embed(description = f"**Language for Big-Dick-Game was changed: Ukrainian**", color = 0x8eac60))
        else:
            await ctx.send(embed = discord.Embed(description = f'**{prefix}set_lang [rus/ukr]** - Установить язык(Русский/Украинский)\n**{prefix}set_lang rus**', color = 0x667676))     

    @commands.command()
    async def dick(self, ctx):
        lang = self.game.find_one({"guild_id": ctx.guild.id})["lang"]
        if not ctx.channel.id == self.game.find_one({"guild_id": ctx.guild.id})["channel_id"]:
            return
        new = {
        "user_id": ctx.author.id,
        "guild_id": ctx.guild.id,
        "name": f"{ctx.author.name}#{ctx.author.discriminator}",
        "len": 0,
        "status": 0, 
        "in_game": 0
        }
        if self.game.count_documents({"guild_id": ctx.guild.id, "user_id": ctx.author.id}) == 0:
            self.game.insert_one(new)
            if lang == "Rus":
                await ctx.send(embed = discord.Embed(description = f'**🔰 {ctx.author.mention}, ты зарегистрировался в игре "Самый длинный пэсюн!"**', color = 0x0073fe))
            else:
                await ctx.send(embed = discord.Embed(description = f'**🔰 {ctx.author.mention}, ти зареєструвався у грі "Найдовший песюн!"**', color = 0x0073fe))
        data = self.game.find_one({"guild_id": ctx.guild.id, "user_id": ctx.author.id})
        delta = datetime.timedelta(hours=3, minutes=0)
        now = datetime.datetime.now() + delta
        date = datetime.datetime(1990,1,1, hour=0, minute=0, second=0)
        d = date - now
        hr = time.strftime("%H", time.gmtime(d.seconds))
        mins = time.strftime("%M", time.gmtime(d.seconds))
        if lang == "Rus":
            tt = '{} ч. {} мин.'.format(int(hr), int(mins) + 1)
        else:
            tt = '{} год. {} хв.'.format(int(hr), int(mins) + 1)
        n = randint(1, 20)
        lplus = randint(1, 10)
        lminus = randint(-5, -1)
        a = [18, 5, 6, 3, 4, 7, 12, 9, 15, 11, 17, 8] 
        b = [10, 13, 19, 2, 16, 14, 20, 1]
        if data["in_game"] == 0:
            pass
        else:
            if lang == "Ukr":
                await ctx.send(embed = discord.Embed(description = f"**{ctx.author.mention}, ти повернувся до гри! ✅**", color = 0x0073fe))
            else:
                await ctx.send(embed = discord.Embed(description = f"**{ctx.author.mention}, ты вернулся к игре! ✅**", color = 0x0073fe))
            self.game.update_one({"guild_id": ctx.guild.id, "user_id": ctx.author.id}, {"$set": {"in_game": 0}})
        if data["status"] == 0:
            if n in a:
                self.game.update_one({"guild_id": ctx.guild.id, "user_id": ctx.author.id}, {"$inc": {"len": lplus}})
                if lang == "Ukr":
                    e = discord.Embed(description = f'**📈 Твій песюн виріс на {lplus} см.\n💎 Тепер його довжина: {self.game.find_one({"guild_id": ctx.guild.id, "user_id": ctx.author.id})["len"]} см.\n⌚️ Продовжуй грати через {tt}**', timestamp = ctx.message.created_at, color = 0x26cb00)
                else:
                    e = discord.Embed(description = f'**📈 Твой пэсюн вырос на {lplus} см.\n💎 Теперь его длина: {self.game.find_one({"guild_id": ctx.guild.id, "user_id": ctx.author.id})["len"]} см.\n⌚️ Продолжай играть через {tt}**', timestamp = ctx.message.created_at, color = 0x26cb00) 
                e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                await ctx.send(embed = e)
                self.game.update_one({"guild_id": ctx.guild.id, "user_id": ctx.author.id}, {"$set": {"status": 1}})
            elif n in b:
                if data['len'] == 0:
                    if lang == "Ukr":
                        e = discord.Embed(description = f'**😧 В тебе немає песюна.\n⌚️ Продовжуй грати через {tt}**', timestamp = ctx.message.created_at, color = 0xffa000)
                    else:
                        e = discord.Embed(description = f'**😧 У тебя нету пэсюна.\n⌚️ Продолжай играть через {tt}**', timestamp = ctx.message.created_at, color = 0xffa000)
                    e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                    await ctx.send(embed = e)
                    self.game.update_one({"guild_id": ctx.guild.id, "user_id": ctx.author.id}, {"$set": {"status": 1}})
                elif -lminus >= data["len"]:
                    self.game.update_one({"guild_id": ctx.guild.id, "user_id": ctx.author.id}, {"$inc": {"len": 1}})
                    if lang == "Ukr":
                        e = discord.Embed(description = f'** 📈Твій песюн виріс на 1 см.\n💎 Тепер його довжина: {self.game.find_one({"guild_id": ctx.guild.id, "user_id": ctx.author.id})["len"]} см.\n⌚️ Продовжуй грати через {tt}**', timestamp = ctx.message.created_at, color = 0x26cb00)
                    else:
                        e = discord.Embed(description = f'**📈 Твой пэсюн вырос на 1 см.\n💎 Теперь его длина: {self.game.find_one({"guild_id": ctx.guild.id, "user_id": ctx.author.id})["len"]} см.\n⌚️ Продолжай играть через {tt}**', timestamp = ctx.message.created_at, color = 0x26cb00)
                    e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                    await ctx.send(embed = e)
                    self.game.update_one({"guild_id": ctx.guild.id, "user_id": ctx.author.id}, {"$set": {"status": 1}})
                else:
                    self.game.update_one({"guild_id": ctx.guild.id, "user_id": ctx.author.id}, {"$inc": {"len": lminus}})
                    if lang == "Ukr":
                        e = discord.Embed(description = f'**✂️ Твій песюн скоротився на {-lminus} см.\n💎 Тепер його довжина: {self.game.find_one({"guild_id": ctx.guild.id, "user_id": ctx.author.id})["len"]} см.\n⌚️ Продовжуй грати через {tt}**', timestamp = ctx.message.created_at, color = 0xff1c00)
                    else:
                        e = discord.Embed(description = f'**✂️ Твой пэсюн уменьшился на {-lminus} см.\n💎 Теперь его длина: {self.game.find_one({"guild_id": ctx.guild.id, "user_id": ctx.author.id})["len"]} см.\n⌚️ Продолжай играть через {tt}**', timestamp = ctx.message.created_at, color = 0x26cb00)
                    e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                    await ctx.send(embed = e)
                    self.game.update_one({"guild_id": ctx.guild.id, "user_id": ctx.author.id}, {"$set": {"status": 1}})
            else:
                return
        else:
            if lang == "Ukr":
                await ctx.send(embed = discord.Embed(description = f'**❌ {ctx.author.mention}, ти сьогодні вже грав!**', color = 0xff0000))
            else:
                await ctx.send(embed = discord.Embed(description = f'**❌ {ctx.author.mention}, ты сегодня уже играл!**', color = 0xff0000))
        if ctx.guild.id == 722190594268725288:
            rolelist = ['Козак', 'Евростандарт', 'Шалун', 'Скромник', 'Брехун']
            memberroles = []
            obsh = []
            for r in ctx.author.roles:
                memberroles.append(r.name)
            for i in rolelist:
                for j in memberroles:
                    if i == j:
                        obsh.append(i)
                        break
            LEN = self.game.find_one({"guild_id": ctx.author.guild.id, "user_id":ctx.author.id})["len"] 
            if LEN >= 500:
                role = discord.utils.get(ctx.guild.roles, id = 798552885822226452)
                if not role in ctx.author.roles:
                    for n in obsh:
                        rol = discord.utils.get(ctx.guild.roles, name = n)
                        await ctx.author.remove_roles(rol)
                    await ctx.author.add_roles(role)
                else:
                    return
            elif (LEN >= 400 and LEN < 500):
                role = discord.utils.get(ctx.guild.roles, id = 798552887697211432)
                if not role in ctx.author.roles:
                    for n in obsh:
                        rol = discord.utils.get(ctx.guild.roles, name = n)
                        await ctx.author.remove_roles(rol)
                    await ctx.author.add_roles(role)
                else:
                    return
            elif (LEN >= 300 and LEN < 400):
                role = discord.utils.get(ctx.guild.roles, id = 798552889584254976)
                if not role in ctx.author.roles:
                    for n in obsh:
                        rol = discord.utils.get(ctx.guild.roles, name = n)
                        await ctx.author.remove_roles(rol)
                    await ctx.author.add_roles(role)
                else:
                    return            
            elif (LEN >= 200 and LEN < 300):
                role = discord.utils.get(ctx.guild.roles, id = 798552891660042270)
                if not role in ctx.author.roles:
                    for n in obsh:
                        rol = discord.utils.get(ctx.guild.roles, name = n)
                        await ctx.author.remove_roles(rol)
                    await ctx.author.add_roles(role)
                else:
                    return
            elif (LEN >= 100 and LEN < 200):
                role = discord.utils.get(ctx.guild.roles, id = 798552892059549727)
                if not role in ctx.author.roles:
                    for n in obsh:
                        rol = discord.utils.get(ctx.guild.roles, name = n)
                        await ctx.author.remove_roles(rol)
                    await ctx.author.add_roles(role)
                else:
                    return
            else:
                return                                          
        else:
            pass
                                          
    @commands.command()
    async def undick(self, ctx):
        lang = self.game.find_one({"guild_id": ctx.guild.id})["lang"]
        if not ctx.channel.id == self.game.find_one({"guild_id": ctx.guild.id})["channel_id"]:
            return
        self.game.update_one({"guild_id": ctx.guild.id, "user_id": ctx.author.id}, {"$set": {"in_game": 1}})
        if lang == "Ukr":
            await ctx.send(embed = discord.Embed(description = f"**{ctx.author.mention}, ти вийшов з гри! ✅**", color = 0x0073fe))
        else:
            await ctx.send(embed = discord.Embed(description = f"**{ctx.author.mention}, ты вышел из игры! ✅**", color = 0x0073fe))
        rolelist = ['Козак', 'Евростандарт', 'Шалун', 'Скромник', 'Брехун']
        memberroles = []
        obsh = []
        for r in ctx.author.roles:
            memberroles.append(r.name)
        for i in rolelist:
            for j in memberroles:
                if i == j:
                    obsh.append(i)
                    break
        for n in obsh:
            rol = discord.utils.get(ctx.guild.roles, name = n)
            await ctx.author.remove_roles(rol)

    @commands.command()
    async def top(self, ctx, count: int = None):
        prefix = self.prx.find_one({"_id": ctx.guild.id})["prefix"]
        lang = self.game.find_one({"guild_id": ctx.guild.id})["lang"]
        if not ctx.channel.id == self.game.find_one({"guild_id": ctx.guild.id})["channel_id"]:
            return
        if count is None:
            n = 30
        elif (count <= 0 or count > 30):
            await ctx.send(embed = discord.Embed(description = f"**{prefix}top[1-30]**", color = 0x667676))
        else:
            n = count
        top = self.game.find({"in_game": 0, "guild_id": ctx.guild.id}).sort("len", -1).limit(n)
        leaders = []
        i = 1
        for t in top:
            member = self.client.get_guild(ctx.guild.id).get_member(t['user_id'])
            if t['len'] == 0:
                if lang == "Ukr":    
                    leaders.append(f'**🔹 {i}. {member.display_name} — немає песюна**')
                else:
                    leaders.append(f'**🔹 {i}. {member.display_name} — нету пэсюна**')
            else:
                leaders.append(f'**🔹 {i}. {member.display_name} — {t["len"]} см**')
            i = i + 1
        if len(leaders) <= 0:
            if lang == "Ukr":
                await ctx.send(embed = discord.Embed(description = f'**Ніхто не грає...**', color = 0x667676))
            else:
                await ctx.send(embed = discord.Embed(description = f'**Никто не играет...**', color = 0x667676))
        else:
            e = discord.Embed(description = "\n".join(leaders), color = 0x32aafd, timestamp = ctx.message.created_at)
            e.set_author(name = f'{ctx.guild.name} | Рейтинг игроков', icon_url = ctx.guild.icon_url)
            e.set_footer(text = 'Opium Team', icon_url = 'https://cdn.discordapp.com/avatars/722921602026700861/654ff8c616269acc148f204c17670aaa.webp?size=1024')
            await ctx.send(embed = e)

def setup(client):
    client.add_cog(Dick(client))
