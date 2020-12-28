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

    #ON MEMBER JOIN
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not self.game.count_documents({"guild_id": member.guild.id, "user_id": member.id}) == 0:
            self.game.update_one({"guild_id": member.guild.id, "user_id": member.id}, {"$set": {"in_game": 0}})
        else:
            pass

    #ON MEMBER REMOVE
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if not self.game.count_documents({"guild_id": member.guild.id, "user_id": member.id}) == 0:
            self.game.update_one({"guild_id": member.guild.id, "user_id": member.id}, {"$set": {"in_game": 1}})
        else:
            pass

    #ON GUILD JOIN
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        ch = {
            "guild_id": guild.id,
            "guild_name": guild.name,
            "channel_id": 0
        }
        if self.game.count_documents({"guild_id": guild.id}) == 0:
            self.game.insert_one(ch)

    #SET CHANNEL
    @commands.command()
    async def set_channel(self, ctx, channel: discord.TextChannel):
        self.game.update_one({"guild_id": ctx.guild.id}, {"$set": {"channel_id": channel.id}})

    #DICK
    @commands.command()
    async def dick(self, ctx):
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
            await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, ти зареєструвався у грі "Найдовший песюн!"**', color = 0x0073fe))
        data = self.game.find_one({"guild_id": ctx.guild.id, "user_id": ctx.author.id})
        delta = datetime.timedelta(hours=2, minutes=0)
        now = datetime.datetime.now() + delta
        date = datetime.datetime(1990,1,1, hour=0, minute=0, second=0)
        d = date - now
        hr = time.strftime("%H", time.gmtime(d.seconds))
        mins = time.strftime("%M", time.gmtime(d.seconds))
        tt = '{} год. {} хв.'.format(int(hr), int(mins) + 1)
        n = randint(1, 20)
        lplus = randint(1, 10)
        lminus = randint(-5, -1)
        a = [18, 5, 2, 1, 4, 7, 12, 9, 15, 11, 8, 17, 3] 
        b = [10, 13, 19, 6, 16, 14, 20]
        if data["in_game"] == 0:
            pass
        else:
            await ctx.send(embed = discord.Embed(description = f"**{ctx.author.mention}, ти повернувся до гри!**", color = 0x0073fe))
            self.game.update_one({"guild_id": ctx.guild.id, "user_id": ctx.author.id}, {"$set": {"in_game": 0}})
        if data["status"] == 0:
            if n in a:
                self.game.update_one({"guild_id": ctx.guild.id, "user_id": ctx.author.id}, {"$inc": {"len": lplus}})
                e = discord.Embed(description = f'**Твій песюн виріс на {lplus} см. 😎\nТепер його довжина: {self.game.find_one({"guild_id": ctx.guild.id, "user_id": ctx.author.id})["len"]} см.\nПродовжуй грати через {tt}**', timestamp = ctx.message.created_at, color = 0x26cb00)
                e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                await ctx.send(embed = e)
                self.game.update_one({"guild_id": ctx.guild.id, "user_id": ctx.author.id}, {"$set": {"status": 1}})
            elif n in b:
                if data['len'] == 0:
                    e = discord.Embed(description = f'**В тебе немає песюна. 😧\nПродовжуй грати через {tt}**', timestamp = ctx.message.created_at, color = 0xffa000)
                    e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                    await ctx.send(embed = e)
                    self.game.update_one({"guild_id": ctx.guild.id, "user_id": ctx.author.id}, {"$set": {"status": 1}})
                elif -lminus >= data["len"]:
                    self.game.update_one({"guild_id": ctx.guild.id, "user_id": ctx.author.id}, {"$inc": {"len": 1}})
                    e = discord.Embed(description = f'**Твій песюн виріс на 1 см. 😎\nТепер його довжина: {self.game.find_one({"guild_id": ctx.guild.id, "user_id": ctx.author.id})["len"]} см.\nПродовжуй грати через {tt}**', timestamp = ctx.message.created_at, color = 0x26cb00)
                    e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                    await ctx.send(embed = e)
                    self.game.update_one({"guild_id": ctx.guild.id, "user_id": ctx.author.id}, {"$set": {"status": 1}})
                else:
                    self.game.update_one({"guild_id": ctx.guild.id, "user_id": ctx.author.id}, {"$inc": {"len": lminus}})
                    e = discord.Embed(description = f'**Твій песюн скоротився на {-lminus} см. 🤣\nТепер його довжина: {self.game.find_one({"guild_id": ctx.guild.id, "user_id": ctx.author.id})["len"]} см.\nПродовжуй грати через {tt}**', timestamp = ctx.message.created_at, color = 0xff1c00)
                    e.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                    await ctx.send(embed = e)
                    self.game.update_one({"guild_id": ctx.guild.id, "user_id": ctx.author.id}, {"$set": {"status": 1}})
            else:
                return
        else:
            await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, ти сьогодні вже грав!**', color = 0xff0000))

    #UNDICK
    @commands.command()
    async def undick(self, ctx):
        if not ctx.channel.id == self.game.find_one({"guild_id": ctx.guild.id})["channel_id"]:
            return
        self.game.update_one({"guild_id": ctx.guild.id, "user_id": ctx.author.id}, {"$set": {"in_game": 1}})
        await ctx.send(embed = discord.Embed(description = f"**{ctx.author.mention}, ти вийшов з гри!**", color = 0x0073fe))

    #TOP PLAYERS
    @commands.command()
    async def top(self, ctx, count: int = None):
        if not ctx.channel.id == self.game.find_one({"guild_id": ctx.guild.id})["channel_id"]:
            return
        if count is None:
            n = 10
        else:
            n = count
        top = self.game.find({"in_game": 0, "guild_id": ctx.guild.id}).sort("len", -1).limit(n)
        leaders = []
        i = 1
        for t in top:
            member = self.client.get_guild(ctx.guild.id).get_member(t['user_id'])
            if t['len'] == 0:
                leaders.append(f'**🔹 {i}. {member.display_name} — немає песюна**')
            else:
                leaders.append(f'**🔹 {i}. {member.display_name} — {t["len"]} см**')
            i = i + 1
        if len(leaders) <= 0:
            await ctx.send(embed = discord.Embed(description = f'**Ніхто не грає...**', color = 0x667676))
        else:
            e = discord.Embed(description = "\n".join(leaders), color = 0x32aafd, timestamp = ctx.message.created_at)
            e.set_author(name = f'{ctx.guild.name}| Leaderboard', icon_url = ctx.guild.icon_url)
            e.set_footer(text = 'Opium Team', icon_url = 'https://cdn.discordapp.com/avatars/722921602026700861/654ff8c616269acc148f204c17670aaa.webp?size=1024')
            await ctx.send(embed = e)

def setup(client):
    client.add_cog(Dick(client))
