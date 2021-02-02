import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient
import os
from random import randint
import asyncio
import time
import datetime
from datetime import timezone, tzinfo, timedelta
from random import sample
import array
import math

class Economy(commands.Cog):

    def __init__(self, client):
        self.client = client    
        self.cluster = MongoClient("mongodb+srv://andrewnobot:xuInmV8QmD9GRR5c@cluster0.28biu.mongodb.net/opiumdb?retryWrites=true&w=majority")
        self.coll = self.cluster.opiumdb.collopiumdb
        self.prx = self.cluster.opiumdb.prefixcoll

    #ON MEMBER JOIN
    @commands.Cog.listener()
    async def on_member_join(self, member):
        post = {
            "_id": member.id,
            "g_id": member.guild.id,
            "name": f"{member.name}#{member.discriminator}",
            "cash": 10,
            "xp": 0,
            "lvl": 1,
            "daily": 1,
            "sbonus": 10,
            "spot": 0,
            "dsbonus": 50,
            "splist": [0],
            "sprice": 50,
            "dsprice": 50,
            "loan": 0,
            "deposit": 0
        }
        if self.coll.count_documents({"_id": member.id}) == 0:
            self.coll.insert_one(post)

    #ON MESSAGE
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if not message.guild.id == 722190594268725288:
            return
        user = message.author
        data = self.coll.find_one({"_id": user.id})
        lvl_xp = 8 + 10 * data["lvl"]
        cash_up = 10 + 10 * data["lvl"]
        if data["xp"] < lvl_xp:
            self.coll.update_one({"_id": user.id}, {"$set": {"xp": data["xp"] + 1}})
        if data["xp"] >= lvl_xp:
            self.coll.update_one({"_id": user.id}, {"$set": {"lvl": data["lvl"] + 1}})
            self.coll.update_one({"_id": user.id}, {"$set": {"xp": 0}})
            self.coll.update_one({"_id": user.id}, {"$inc": {"cash": cash_up}})
            self.coll.update_one({"_id": 1}, {"$inc": {"cash": -cash_up}})
            await message.channel.send(embed = discord.Embed(description = f'**Пользователь {user.mention} получил новый уровень: `{data["lvl"] + 1}` (+{cash_up} cc)**', color = 0xd7ff5d))

    #BALANCE
    @commands.command()
    async def balance(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send(embed = discord.Embed(description = f'**Баланс пользователя {ctx.author.mention}: {self.coll.find_one({"_id": ctx.author.id})["cash"]} Cooper Coins**', color = 0x00a5ff))
        else:
            await ctx.send(embed = discord.Embed(description = f'**Баланс пользователя {member.mention}: {self.coll.find_one({"_id": member.id})["cash"]} Cooper Coins**', color = 0x00a5ff))

    #STATS
    @commands.command()
    async def stats(self, ctx, member: discord.Member = None):
        if member is None:
            m = ctx.author
            data = self.coll.find_one({"_id": ctx.author.id})
        else:
            data = self.coll.find_one({"_id": member.id})
            m = member
        a_xp = data["xp"]
        a_cash = data["cash"]
        d_cash = round(data['deposit'])
        a_lvl = data["lvl"]
        sbonus = data["sbonus"]
        spot = data["spot"]
        dsbonus = data["dsbonus"]
        lvl_xp = 10 + 10 * data["lvl"]
        emb = discord.Embed(description = f'**Пользователь: {m.mention}\n\nУровень: `{a_lvl}` Lvl\nОпыт: `{a_xp}`/`{lvl_xp}` Xp\nБаланс: `{a_cash}` Cooper Coins\nБаланс депозита: `{d_cash}` Cooper Coins**', timestamp = ctx.message.created_at, color = 0x00ffd5)
        emb.set_author(name = f'{m} | Статистика', icon_url = m.avatar_url)
        emb.add_field(name = 'Навыки:', value = f'\n**💿 Рулетка(выигрыш): от `{round((sbonus - 9) * 0.7)}` до `{sbonus}` cc\n💿 Рулетка(процент Jackpot): `{spot}%`\n📀 Ежедневная рулетка(выигрыш): от `{round((dsbonus - 20) * 0.7)}` до `{dsbonus}` cc**')
        emb.set_footer(text = 'Opium 🌴 Team', icon_url = 'https://cdn.discordapp.com/avatars/722921602026700861/654ff8c616269acc148f204c17670aaa.webp?size=1024')
        await ctx.send(embed = emb)

    #PAY
    @commands.command()
    async def pay(self, ctx, member: discord.Member, amount: int):
        acash = self.coll.find_one({"_id": ctx.author.id})["cash"]
        mcash = self.coll.find_one({"_id": member.id})["cash"]
        if amount <= 0:
            await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, введены некорректные данные**', color = 0xff0000))
        elif amount > acash:
            ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, y вас недостаточно Cooper Coins!**', color = 0xff0000))
        elif ctx.author == member:
            await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, нельзя передавть самому себе!**', color = 0xff0000))
        else:
            self.coll.update_one({"_id": ctx.author.id},
            {"$set": {"cash": acash - amount}})

            self.coll.update_one({"_id": member.id},
            {"$set": {"cash": mcash + amount}})

            self.coll.update_one({"_id": 1}, {"$inc": {"cash": amount}})
            await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention} передал(a) {member.mention} `{amount}` Cooper Coins**', color = 0xbeff00))

    #SET BALANCE
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def set_balance(self, ctx, member: discord.Member, amount: int):
        if amount < 0:
            await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, введены некорректные данные**', color = 0xff0000))
        else:
            self.coll.update_one({"_id": member.id},
            {"$set": {"cash": amount}})
            await ctx.send(embed = discord.Embed(description = f'**Модератор `{ctx.author.display_name}` установил баланс пользователю\n`{member.display_name}`: `{self.coll.find_one({"_id": member.id})["cash"]}` сс**', color = 0x20947a))

    #SET LVL
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def set_lvl(self, ctx, member: discord.Member, lvl: int):
        if lvl <= 0:
            await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, введены некорректные данные**', color = 0xff0000))
        else:
            self.coll.update_one({"_id": member.id}, {"$set": {"lvl": lvl}})
            await ctx.send(embed = discord.Embed(description = f'**Модератор `{ctx.author.display_name}` установил `{self.coll.find_one({"_id": member.id})["lvl"]}` уровень\nпользователю `{member.display_name}`**', color = 0x20947a))

    #DELETE STATS
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def delete_stats(self, ctx, member: discord.Member):
        await ctx.send(embed = discord.Embed(description = f'**Модератор {ctx.author.mention} обнулил статистику пользователю {member.mention}**', color = 0xc98224))
        up = self.coll.update_one
        m = {"_id": member.id}
        up(m, {"$set": {"cash": 10}})
        up(m, {"$set": {"xp": 0}})
        up(m, {"$set": {"lvl": 1}})
        up(m, {"$set": {"sbonus": 10}})
        up(m, {"$set": {"spot": 0}})
        up(m, {"$set": {"dsbonus": 50}})
        up(m, {"$set": {"splist": [0]}})
        up(m, {"$set": {"sprice": 50}})
        up(m, {"$set": {"dsprice": 50}})
        up(m, {"$set": {"deposit": 0}})

    #SPIN
    @commands.command(aliases = ['спін', 'спин', 'ызшт'])
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def spin(self, ctx):
        sbonus = self.coll.find_one({"_id": ctx.author.id})["sbonus"]
        splist = self.coll.find_one({"_id": ctx.author.id})["splist"]
        if not ctx.message.channel.id == 781042512532996116:
            return 
        else:
            n1 = randint(1, 101)
            if n1 in splist:
                self.coll.update_one({"_id": ctx.author.id}, {"$inc": {"cash": 2500}})
                self.coll.update_one({"_id": 1}, {"$inc": {"cash": -2500}})
                emb = discord.Embed(title = 'Джекпот 🤩 🥳 🎉',description = f'**Выигрыш: 2500 cc**', color = 0xffa000)
                channel = self.client.get_channel(789806580891123752)
                com = ', '
                await channel.send(embed = discord.Embed(description = f"**User {ctx.author.mention} got a jackpot with code number: `{n1}`\nList of his lucky numbers:\n`{com.join(map(str, splist))}`**", color = 0xffa000))
            else:
                msb = round((sbonus - 9) * 0.7)
                n = randint(msb, sbonus)
                self.coll.update_one({"_id": ctx.author.id}, {"$inc": {"cash": n}})
                self.coll.update_one({"_id": 1}, {"$inc": {"cash": -n}})
                emb = discord.Embed(description = f'**Выигрыш: `{n}` cc**', color = 0x00ff2e)
            emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            emb.set_footer(text = f'Баланс • {self.coll.find_one({"_id": ctx.author.id})["cash"]} Cooper Coins')
            await ctx.send(embed = emb)

    #SPIN ERROR
    @spin.error
    async def spin_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
            m = time.strftime("%M", time.gmtime(error.retry_after))
            s = time.strftime("%S", time.gmtime(error.retry_after))
            if int(m) < 10:
                m = m[1:]
            else:
                pass
            await ctx.send(embed = discord.Embed(description = '**Ты уже сыграл. Следующая попытка через {} мин. {} сек.**'.format(m, s), color = 0xff0000))

    #TRY
    @commands.command(aliases = ['try', 'true', 'false'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def __true(self, ctx, amount: int):
        cs = ctx.send
        de = discord.Embed
        money = self.coll.find_one({"_id": ctx.author.id})["cash"]
        if (money > 10000 and amount > 100):
            await cs(embed = de(title = 'Ошибка ⛔', description = f'**При балансе свыше 10 000 сс сумма не может быть выше 100 сс**', color = 0xff0000))
        elif amount > 1000:
            await cs(embed = de(title = 'Ошибка ⛔', description = f'**Сумма не может быть выше 1000 сс**', color = 0xff0000))        
        elif amount <= 0:
            await cs(embed = de(description = f'**{ctx.author.mention}, введены некорректные данные**', color = 0xff0000))
        elif amount > money:
            await cs(embed = de(description = f'**{ctx.author.mention}, y вас недостаточно Cooper Coins!**', color = 0xff0000))
        else:
            n = randint(1, 20)
            a = [10, 5, 2, 1, 4, 7, 12, 9, 15, 11] 
            b = [18, 17, 19, 6, 16, 3, 14, 20, 8, 13]
            self.coll.update_one({"_id": 1}, {"$inc": {"cash": -amount}})
            if n in a:
                win = f'**Win 😜, +{amount} Cooper Coins**'
                clr = 0x26cb00
                x = amount
            elif n in b:
                win = f'**Lose 😭, -{amount} Cooper Coins**'
                clr = 0xd50000
                x = -amount
            else:
                pass
            self.coll.update_one({"_id": ctx.author.id}, {"$inc": {"cash": x}})
            emb = de(description = win, color = clr)
            emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            emb.set_footer(text = f'Баланс • {self.coll.find_one({"_id": ctx.author.id})["cash"]} Cooper Coins')
            await cs(embed = emb)

    #TRY ERROR
    @__true.error
    async def __true_error(self, ctx, error):
        prefix = self.prx.find_one({"_id": ctx.guild.id})["prefix"]
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send(embed = discord.Embed(title = f'Команда: {prefix}try', description = '**Псевдонимы**: {}true, {}false\n**Описание**: Удвоить сумму. Шанс 50%\n**Перезарядка**: 1 секунда\n**Использование**:\n{}true [сумма]\n{}try [сумма]\n{}false [сумма]\n**Пример**:\n{}true 15\n{}try 25\n{}false 50'.format(prefix, prefix, prefix, prefix, prefix, prefix, prefix, prefix), color = discord.Colour.dark_gray()))
        if isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
            await ctx.send(f"**{ctx.author.mention}, воу, воу, не так бысто!**")
                           
    #SPIN UP
    @commands.command()
    async def spin_up(self, ctx, count: int = None):
        if count is None:
            data = self.coll.find_one({"_id": ctx.author.id})
            cash = data["cash"]
            sbonus = data["sbonus"]
            sprice = data["sprice"]
            if not ctx.message.channel.id == 781042512532996116:
                return
            elif cash < sprice:
                await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, у вас недостаточно Cooper Coins. {cash}/{sprice} cc**', color = 0xff0000))
            else:
                self.coll.update_one({"_id": ctx.author.id}, {"$inc": {"cash": -sprice}})
                emb = discord.Embed(title = f'Повышение навыка x1 🔼 (-{sprice} cc)', description  = f'**💿 Рулетка(макс. выигрыш): `{sbonus}` -> `{sbonus + 1}` cc**', color = 0xfdff4b)
                emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                emb.set_footer(text = f'Баланс • {self.coll.find_one({"_id": ctx.author.id})["cash"]} cc | Next update • {sprice + 5} cc')
                await ctx.send(embed = emb)
                self.coll.update_one({"_id": ctx.author.id}, {"$inc": {"sbonus": 1}})
                self.coll.update_one({"_id": ctx.author.id}, {"$inc": {"sprice": 5}})
        else:
            data = self.coll.find_one({"_id": ctx.author.id})
            cash = data["cash"]
            sbonus = data["sbonus"]
            sprice = data["sprice"]
            a = round(sprice + ((count - 1) * 5))
            s = round(((sprice + a) / 2) * count)
            if not ctx.message.channel.id == 781042512532996116:
                return
            elif cash < s:
                await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, у вас недостаточно Cooper Coins. {cash}/{s} cc**', color = 0xff0000))
            else:
                self.coll.update_one({"_id": ctx.author.id}, {"$inc": {"cash": -s}})
                emb = discord.Embed(title = f'Повышение навыка x{count} 🔼 (-{s} cc)', description  = f'**💿 Рулетка(макс. выигрыш): `{sbonus}` -> `{sbonus + (count * 1)}` cc**', color = 0xfdff4b)
                emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                emb.set_footer(text = f'Баланс • {self.coll.find_one({"_id": ctx.author.id})["cash"]} cc | Next update • {a + 5} cc')
                await ctx.send(embed = emb)
                self.coll.update_one({"_id": ctx.author.id}, {"$inc": {"sbonus": count * 1}})
                self.coll.update_one({"_id": ctx.author.id}, {"$set": {"sprice": a + 5}})


    #DAILY SPIN UP        
    @commands.command()
    async def daily_spin_up(self, ctx, count: int = None):
        if count is None:
            data = self.coll.find_one({"_id": ctx.author.id})
            cash = data["cash"]
            dsbonus = data["dsbonus"]
            dsprice = data["dsprice"]
            if not ctx.message.channel.id == 781042512532996116:
                return
            elif cash < dsprice:
                await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, у вас недостаточно Cooper Coins. {cash}/{dsprice} cc**', color = 0xff0000))
            else:
                self.coll.update_one({"_id": ctx.author.id}, {"$inc": {"cash": -dsprice}})
                emb = discord.Embed(title = f'Повышение навыка x1 🔼 (-{dsprice} cc)', description  = f'**📀 Ежедневная рулетка(макс. выигрыш): `{dsbonus}` -> `{dsbonus + 5}` cc**', color = 0xfdff4b)
                emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                emb.set_footer(text = f'Баланс • {self.coll.find_one({"_id": ctx.author.id})["cash"]} cc | Next update • {dsprice + 5} cc')
                await ctx.send(embed = emb)
                self.coll.update_one({"_id": ctx.author.id}, {"$inc": {"dsbonus": 5}})
                self.coll.update_one({"_id": ctx.author.id}, {"$inc": {"dsprice": 5}})
        else:
            data = self.coll.find_one({"_id": ctx.author.id})
            cash = data["cash"]
            dsbonus = data["dsbonus"]
            dsprice = data["dsprice"]
            a = round(dsprice + ((count - 1) * 5))
            s = round(((dsprice + a) / 2) * count)
            if not ctx.message.channel.id == 781042512532996116:
                return
            elif cash < s:
                await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, у вас недостаточно Cooper Coins. {cash}/{s} cc**', color = 0xff0000))
            else:
                self.coll.update_one({"_id": ctx.author.id}, {"$inc": {"cash": -s}})
                emb = discord.Embed(title = f'Повышение навыка x{count} 🔼 (-{s} cc)', description  = f'**💿 Рулетка(макс. выигрыш): `{dsbonus}` -> `{dsbonus + (count * 5)}` cc**', color = 0xfdff4b)
                emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                emb.set_footer(text = f'Баланс • {self.coll.find_one({"_id": ctx.author.id})["cash"]} cc | Next update • {a + 5} cc')
                await ctx.send(embed = emb)
                self.coll.update_one({"_id": ctx.author.id}, {"$inc": {"dsbonus": count * 5}})
                self.coll.update_one({"_id": ctx.author.id}, {"$set": {"dsprice": a + 5}})

    #GIVE
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def give(self, ctx, member: discord.Member, amount: int, *, reason = None):
        if amount <= 0:
            await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, введены некорректные данные**', color = 0xff0000))
        else:
            self.coll.update_one({"_id": member.id}, {"$inc": {"cash": amount}})
            self.coll.update_one({"_id": 1}, {"$inc": {"cash": -amount}})
            emb = discord.Embed(description = f'**`{ctx.author.display_name}` начислил `{amount}` Cooper Coins\nпользователю`{member.display_name}`. Причина: {reason}**', color = 0x20947a)
            await ctx.send(embed = emb)

    #BANK
    @commands.command()
    async def bank(self, ctx):
        money = self.coll.find_one({"_id": 1})["cash"]
        e = discord.Embed(description = f'**💸 Состояние банка: `{money}` Cooper Coins**', timestamp = ctx.message.created_at, color = 0x5797af)
        e.set_author(name = f'{ctx.guild.name} | Genesis Bank', icon_url = ctx.guild.icon_url)
        e.set_footer(text = 'Opium Team')
        await ctx.send(embed = e)			   

    #DAILY SPIN
    @commands.command()
    async def daily_spin(self, ctx):
        data = self.coll.find_one({"_id": ctx.author.id})
        dsbonus = data["dsbonus"]
        spot = data["spot"]
        sp = spot + 1
        sbonus = data["sbonus"]
        if not ctx.message.channel.id == 781042512532996116:
            return
        daily = self.coll.find_one({"_id": ctx.author.id})["daily"]
        if daily == 1:
            mdsb = round((dsbonus - 20) * 0.7)
            n = randint(mdsb, dsbonus)
            data = self.coll.find_one({"_id": ctx.author.id})
            x = 2 + 2 * data["lvl"]
            self.coll.update_one({"_id": ctx.author.id}, {"$inc": {"xp": x}})
            self.coll.update_one({"_id": ctx.author.id}, {"$inc": {"cash": n}})
            emb = discord.Embed(title = 'Ежедневный бонус ✅', description = f'**Награды:\n💰 {n} Cooper Coins\n💎 {x} Xp**\n', color = 0x00ff2e)
            if spot < 15:
                emb.add_field(name = 'Повышение навыков ⬆️', value = f'**💿 Рулетка(макс. выигрыш): `{sbonus}` -> `{sbonus + 5}` cc\n💿 Рулетка(процент Jackpot): `{spot}%` -> `{sp}%`\n📀 Ежедневная рулетка(макс. выигрыш): `{dsbonus}` -> `{dsbonus + 10}` cc**')
                lst = sample(range(1, 102), sp)
                self.coll.update_one({"_id": ctx.author.id}, {"$set": {"splist": lst}})
                self.coll.update_one({"_id": ctx.author.id}, {"$set": {"spot": sp}})
            else:
                emb.add_field(name = 'Повышение навыков ⬆️', value = f'**💿 Рулетка(макс. выигрыш): `{sbonus}` -> `{sbonus + 5}` cc\n💿 Рулетка(процент Jackpot): `{spot}%` Max Lvl\n📀 Ежедневная рулетка(макс. выигрыш): `{dsbonus}` -> `{dsbonus + 10}` cc**')
            emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            emb.set_footer(text = f'Баланс • {self.coll.find_one({"_id": ctx.author.id})["cash"]} Cooper Coins')
            await ctx.send(embed = emb)
            self.coll.update_one({"_id": ctx.author.id}, {"$set": {"sbonus": sbonus + 5}})
            self.coll.update_one({"_id": ctx.author.id}, {"$set": {"dsbonus": dsbonus + 10}})
            self.coll.update_one({"_id": ctx.author.id}, {"$set": {"daily": 2}})
            self.coll.update_one({"_id": 1}, {"$inc": {"cash": -n}})
        else:
            await ctx.send(embed = discord.Embed(description = '**Ты сегодня уже играл!**', color = 0xff0004))

    #TOP PLAYERS [COOPER COINS\LEVEL]
    @commands.command()
    async def topplayers(self, ctx, name = None):
        prefix = self.prx.find_one({"_id": ctx.guild.id})["prefix"]
        if name == 'cc':
            top = self.coll.find().sort("cash", -1).limit(6).skip(2)
            leaders = []
            for t in top:
                leaders.append(f"<@{t['_id']}>: {t['cash']}")
            emb = discord.Embed(description = f"**1. {leaders[0]} Cooper Coins\n\n2. {leaders[1]} Cooper Coins\n\n3. {leaders[2]} Cooper Coins\n\n4. {leaders[3]} Cooper Coins\n\n5. {leaders[4]} Cooper Coins**", color = 0x32aafd, timestamp = ctx.message.created_at)
            emb.set_author(name = f'{ctx.guild.name} | Leaderboard (Balance)', icon_url = ctx.guild.icon_url)
            emb.set_footer(text = 'Opium Team', icon_url = 'https://cdn.discordapp.com/avatars/722921602026700861/654ff8c616269acc148f204c17670aaa.webp?size=1024')
            await ctx.send(embed = emb)
        elif name == 'lvl':
            top = self.coll.find().sort("lvl", -1).limit(6).skip(1)
            leaders = []
            for t in top:
                leaders.append(f"<@{t['_id']}>: {t['lvl']}")
            emb = discord.Embed(description = f"**1. {leaders[0]} уровень\n\n2. {leaders[1]} уровень\n\n3. {leaders[2]} уровень\n\n4. {leaders[3]} уровень\n\n5. {leaders[4]} уровень**", color = 0x32aafd, timestamp = ctx.message.created_at)
            emb.set_author(name = f'{ctx.guild.name} | Leaderboard (Lvl)', icon_url = ctx.guild.icon_url)
            emb.set_footer(text = 'Opium Team', icon_url = 'https://cdn.discordapp.com/avatars/722921602026700861/654ff8c616269acc148f204c17670aaa.webp?size=1024')
            await ctx.send(embed = emb)
        elif name is None:
            await ctx.send(embed = discord.Embed(description = f'**{prefix}topplayers cc - Leaderboard (Balance)\n{prefix}topplayers lvl - Leaderboard (Lvl)**', color = 0x667676))
        else:
            await ctx.send(embed = discord.Embed(description = f'**{prefix}topplayers cc - Leaderboard (Balance)\n{prefix}topplayers lvl - Leaderboard (Lvl)**', color = 0x667676))

    #UP INFO            
    @commands.command()
    async def up_info(self, ctx):
        data = self.coll.find_one({"_id": ctx.author.id})
        sp = data["sprice"]
        dsp = data["dsprice"]
        cash = data["cash"]
        discr = (2 * sp - 5) ** 2 + 40 * cash
        n1 = (-(2 * sp - 5) + math.sqrt(discr)) / (10)
        discr1 = (2 * dsp - 5) ** 2 + 40 * cash
        n2 = (-(2 * dsp - 5) + math.sqrt(discr1)) / (10)
        emb = discord.Embed(title = f'Цены на повышение навыков для {ctx.author.display_name}', description = f'**💿 Рулетка. Цена: {sp} Cooper Coins**\n        (Можно улучшить {int(n1)} раз)\n**📀 Ежедневная рулетка. Цена: {dsp} Cooper Coins**\n        (Можно улучшить {int(n2)} раз)', color = 0x256845)
        emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        emb.set_footer(text = f'Баланс • {self.coll.find_one({"_id": ctx.author.id})["cash"]} Cooper Coins')
        await ctx.send(embed = emb)

    #CREDIR
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def credit(self, ctx, member: discord.Member, amount: int):
        proc = round(amount * 1.3)
        self.coll.update_one({"_id": member.id}, {"$inc": {"loan": proc}})
        self.coll.update_one({"_id": member.id}, {"$inc": {"cash": amount}})
        await ctx.send(embed = discord.Embed(description  = f'**Модератор {ctx.author.mention} выдал кередит пользователю {member.mention} в размере `{amount}` Cooper Coins. Вернуть: {proc}**', color = 0xb9ff00))

    #MYCREDIT
    @commands.command()
    async def mycredit(self, ctx):
        loan = self.coll.find_one({"_id": ctx.author.id})['loan']
        if loan == 0:
            await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, у вас нету непогашенных кредитов!**', color = 0x854be8))
        else:
            emb = discord.Embed(description = f'**{ctx.author.mention}, у вас имеется непогашенный кредит!**', timestamp = ctx.message.created_at, color = 0x007cc0)
            emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            emb.add_field(name = 'Сумма:', value = f'{loan} Cooper Coins')
            emb.set_footer(text = 'Opium 🌴 Bot')
            await ctx.send(embed = emb)

    #RETURN CREDIT
    @commands.command()
    async def return_credit(self, ctx, amount: int):
        loan = self.coll.find_one({"_id": ctx.author.id})['loan']
        money = self.coll.find_one({"_id": ctx.author.id})["cash"]
        if amount > money:
            await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, y вас недостаточно Cooper Coins!**', color = 0xff0000))
        elif loan == 0:
            await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, у вас нету непогашенных кредитов!**', color = 0x854be8))
        elif amount <= 0:
            await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, введены некорректные данные**', color = 0xff0000))
        elif amount == loan:
            self.coll.update_one({"_id": ctx.author.id}, {"$inc": {"loan": -amount}})
            self.coll.update_one({"_id": ctx.author.id}, {"$inc": {"cash": -amount}})
            await ctx.send(embed = discord.Embed(description = '**Кредит погашен. Поздравляю!**', color = 0xffec00))
        elif amount < loan:
            self.coll.update_one({"_id": ctx.author.id}, {"$inc": {"loan": -amount}})
            self.coll.update_one({"_id": ctx.author.id}, {"$inc": {"cash": -amount}})
            await ctx.send(embed = discord.Embed(description = f'**Вы внесли `{amount}` Cooper Coins. Осталось: `{self.coll.find_one({"_id": ctx.author.id})["loan"]}`**', color = 0xffec00))
        else:
            self.coll.update_one({"_id": ctx.author.id}, {"$inc": {"cash": -loan}})
            await ctx.send(embed = discord.Embed(description = f'**Воу, вы внесли даже больше чем нужно. Кредит погашен. Возвращаю вам: `{amount - loan}` Cooper Coins**', color = 0xffec00))
            self.coll.update_one({"_id": ctx.author.id}, {"$set": {"loan": 0}})
                                                 
    #MYDEPOSIT
    @commands.command(aliases = ['мойдепозит', 'депозит', 'депозитинфо', 'md'])
    async def mydeposit(self, ctx):
        data = self.coll.find_one({"_id": ctx.author.id})
        dep = data["deposit"]
        emb = discord.Embed(description = f'**Баланс вашего депозит счёта: `{round(dep)}` Cooper Coins**', color = 0x02c4fa, timestamp = ctx.message.created_at)
        emb.set_author(name = f'{ctx.author} | Депозит', icon_url = ctx.author.avatar_url)
        emb.set_footer(text = f'Opium 🌴 Bot')
        await ctx.send(embed = emb)

    #PUT DEPOSIT
    @commands.command(aliases = ['положитьнадепозит', 'put_on_deposit', 'pod'])
    async def _put_on_deposit(self, ctx, amount: int):
        money = self.coll.find_one({"_id": ctx.author.id})["cash"]
        if amount <= 0:
            await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, введены некорректные данные**', color = 0xff0000))
        elif amount > money:
            await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, y вас недостаточно Cooper Coins!**', color = 0xff0000))
        else:
            self.coll.update_one({"_id": ctx.author.id}, {"$inc": {"cash": -amount}})
            self.coll.update_one({"_id": ctx.author.id}, {"$inc": {"deposit": amount}})
            emb = discord.Embed(description = f'**Вы положили `{amount}` Cooper Coins на ваш депозит счёт**', color = 0x28e91c)
            emb.set_author(name = f'{ctx.author} | Пополнение депозита', icon_url = ctx.author.avatar_url)
            emb.set_footer(text = f'Баланс депозита • {round(self.coll.find_one({"_id": ctx.author.id})["deposit"])} Cooper Coins')
            await ctx.send(embed = emb)

    #GET DEPOSIT
    @commands.command(aliases = ['снятьдепозит', 'take_deposit', 'tfd'])
    async def take_from_deposit(self, ctx, amount: int):
        money = self.coll.find_one({"_id": ctx.author.id})["deposit"]
        if amount <= 0:
            await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, введены некорректные данные**', color = 0xff0000))
        elif amount > money:
            await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, у вас недостаточно Cooper Coins на депозите**', color = 0xff0000))
        else:
            self.coll.update_one({"_id": ctx.author.id}, {"$inc": {"deposit": -amount}})
            self.coll.update_one({"_id": ctx.author.id}, {"$inc": {"cash": amount}})
            emb = discord.Embed(description = f'**Вы сняли `{amount}` Cooper Coins с вашего депозит счёта**', color = 0xd36262)
            emb.set_author(name = f'{ctx.author} | Снятие депозита', icon_url = ctx.author.avatar_url)
            emb.set_footer(text = f'Баланс депозита • {round(self.coll.find_one({"_id": ctx.author.id})["deposit"])} Cooper Coins')
            await ctx.send(embed = emb)

    #DEPOSIT CALCULATOR
    @commands.command()
    async def dep_calc(self, ctx, hours: int = None, summ: int = None):
        prefix = self.prx.find_one({"_id": ctx.guild.id})["prefix"]
        if hours is None:
            await ctx.send(embed = discord.Embed(title = f'Command: {prefix}dep_calc', description = f'**Описание:** Калькулятор депозита\n**Использование:** {prefix}dep_calc <кол-во часов>\n**Пример:** {prefix}dep_cacl 12'))
        elif hours > 720 and ctx.author.id != 382522784841990144:
            await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, не более 120 часов!**', color = 0xff0000))
        elif hours <= 0:
            await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, введены некорректные данные**', color = 0xff0000))
        else:
            if summ is None:
                dep = round(self.coll.find_one({"_id": ctx.author.id})["deposit"])
            else:
                dep = summ
            s = []
            i = 0
            while i < hours:
                s.append(round(dep * 1.005))
                i = i + 1
                dep = round(dep * 1.005)
            sn = s[hours - 1]
            z = sn - round(dep)
            await ctx.send(embed = discord.Embed(description = f'**На вашем депозит счёте будет: `{sn} Cooper Coins` (разница `{z} cc`)**', color = 0xcd14d3))
                           
    #OREL
    @commands.command()
    async def orel(self, ctx, member: discord.Member, cc: int):
        global content
        content = 'orel'
        global orauthor
        orauthor = ctx.author
        global ormember
        ormember = member
        global ccg
        ccg = cc
        aut_cash = self.coll.find_one({"_id": orauthor.id})["cash"]
        mem_cash = self.coll.find_one({"_id": ormember.id})["cash"]
        if not ctx.channel.id == 781042512532996116:
            return
        elif ctx.author.id == member.id:
            await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, вы не можете сыграть сам с собой!**', color = 0xff0000))
        elif aut_cash < cc:
            await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, y вас недостаточно Cooper Coins!**', color = 0xff0000))
        elif mem_cash < cc:
            await ctx.send(embed = discord.Embed(description = f'**У {member.mention} недостаточно Cooper Coins**', color = 0xff0000))
        elif cc <= 0:
            await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, введены некорректные данные**', color = 0xff0000))
        else:
            emb = discord.Embed(description = f'**{ctx.author.mention} предложил {member.mention} игру на {cc} cc\n\n{ctx.author.display_name} - <:verified:768155762425462784>\n{member.display_name} - <:unverified:768155761171234887>**', color = 0x425be0)
            emb.set_author(name = f'{ctx.guild.name} | Орёл - Решка', icon_url = ctx.guild.icon_url)
            emb.set_footer(text = f'(Орёл) {ctx.author.name} x {member.name} (Решка)')
            global ormsg
            ormsg = await ctx.send(embed = emb)
            await ormsg.add_reaction('<:verified:768155762425462784>')
            await ormsg.add_reaction('<:unverified:768155761171234887>')

    #RESHKA
    @commands.command()
    async def reshka(self, ctx, member: discord.Member, cc: int):
        global content
        content = 'reshka'
        global orauthor1
        orauthor1 = ctx.author
        global ormember1
        ormember1 = member
        global ccg1
        ccg1 = cc
        aut_cash = self.coll.find_one({"_id": orauthor1.id})["cash"]
        mem_cash = self.coll.find_one({"_id": ormember1.id})["cash"]
        if not ctx.channel.id == 781042512532996116:
            return
        elif ctx.author.id == member.id:
            await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, вы не можете сыграть сам с собой!**', color = 0xff0000))
        elif aut_cash < cc:
            await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, y вас недостаточно Cooper Coins!**', color = 0xff0000))
        elif mem_cash < cc:
            await ctx.send(embed = discord.Embed(description = f'**У {member.mention} недостаточно Cooper Coins**', color = 0xff0000))
        elif cc <= 0:
            await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, введены некорректные данные**', color = 0xff0000))
        else:
            emb = discord.Embed(description = f'**{ctx.author.mention} предложил {member.mention} игру на {cc} cc\n\n{ctx.author.display_name} - <:verified:768155762425462784>\n{member.display_name} - <:unverified:768155761171234887>**', color = 0x425be0)
            emb.set_author(name = f'{ctx.guild.name} | Орёл - Решка', icon_url = ctx.guild.icon_url)
            emb.set_footer(text = f'(Решка) {ctx.author.name} x {member.name} (Орёл)')
            global ormsg1
            ormsg1 = await ctx.send(embed = emb)
            await ormsg1.add_reaction('<:verified:768155762425462784>')
            await ormsg1.add_reaction('<:unverified:768155761171234887>')

    #ON RAW REACTION ADD
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        try:
            channel = self.client.get_channel(781042512532996116)
            if payload.member.bot:
                return
            if content == 'orel':
                if payload.member.id == ormember.id:
                    if payload.message_id == ormsg.id:
                        if payload.emoji.id == 768155762425462784:
                            emb = discord.Embed(description = f'**{orauthor.mention} предложил {ormember.mention} игру на {ccg} cc\n\n{orauthor.display_name} - <:verified:768155762425462784>\n{ormember.display_name} - <:verified:768155762425462784>**', color = 0x425be0)
                            emb.set_author(name = f'{payload.member.guild.name} | Орёл - Решка', icon_url = payload.member.guild.icon_url)
                            emb.set_footer(text = f'(Орёл) {orauthor.name} x {ormember.name} (Решка)')
                            await ormsg.edit(embed = emb)
                            await asyncio.sleep(1)
                            n = randint(0, 1)
                            if n == 0:
                                self.coll.update_one({"_id": orauthor.id}, {"$inc": {"cash": ccg}})
                                self.coll.update_one({"_id": ormember.id}, {"$inc": {"cash": -ccg}})
                                self.coll.update_one({"_id": 1}, {"$inc": {"cash": ccg}})
                                e1 = discord.Embed(description = f'**Выпало: Орёл\nПобеда {orauthor.mention}, + {ccg} Cooper Coins**', color = 0x00ff05)
                                e1.set_author(name = f'{payload.member.guild.name} | Орёл - Решка', icon_url = payload.member.guild.icon_url)
                                e1.set_footer(text = f'(Орёл) {orauthor.name} x {ormember.name} (Решка)')
                                await channel.send(embed = e1)
                                await ormsg.delete()
                            elif n == 1:
                                self.coll.update_one({"_id": ormember.id}, {"$inc": {"cash": ccg}})
                                self.coll.update_one({"_id": orauthor.id}, {"$inc": {"cash": -ccg}})
                                self.coll.update_one({"_id": 1}, {"$inc": {"cash": ccg}})
                                e2 = discord.Embed(description = f'**Выпало: Решка\nПобеда {ormember.mention}, + {ccg} Cooper Coins**', color = 0x00ff05)
                                e2.set_author(name = f'{payload.member.guild.name} | Орёл - Решка', icon_url = payload.member.guild.icon_url)
                                e2.set_footer(text = f'(Орёл) {orauthor.name} x {ormember.name} (Решка)')
                                await channel.send(embed = e2)
                                await ormsg.delete()
                            else:
                                return
                if (payload.member.id == ormember.id or payload.member.id == orauthor.id):
                    if payload.message_id == ormsg.id:
                        if payload.emoji.id == 768155761171234887:
                            await ormsg.delete()
            if content == 'reshka':
                if payload.member.id == ormember1.id:
                    if payload.message_id == ormsg1.id:
                        if payload.emoji.id == 768155762425462784:
                            emb = discord.Embed(description = f'**{orauthor1.mention} предложил {ormember1.mention} игру на {ccg1} cc\n\n{orauthor1.display_name} - <:verified:768155762425462784>\n{ormember1.display_name} - <:verified:768155762425462784>**', color = 0x425be0)
                            emb.set_author(name = f'{payload.member.guild.name} | Орёл - Решка', icon_url = payload.member.guild.icon_url)
                            emb.set_footer(text = f'(Решка) {orauthor1.name} x {ormember1.name} (Орёл)')
                            await ormsg1.edit(embed = emb)
                            await asyncio.sleep(1)
                            n = randint(0, 1)
                            if n == 0:
                                self.coll.update_one({"_id": ormember1.id}, {"$inc": {"cash": ccg1}})
                                self.coll.update_one({"_id": orauthor1.id}, {"$inc": {"cash": -ccg1}})
                                self.coll.update_one({"_id": 1}, {"$inc": {"cash": ccg1}})
                                e1 = discord.Embed(description = f'**Выпало: Орёл\nПобеда {ormember1.mention}, + {ccg1} Cooper Coins**', color = 0x00ff05)
                                e1.set_author(name = f'{payload.member.guild.name} | Орёл - Решка', icon_url = payload.member.guild.icon_url)
                                e1.set_footer(text = f'(Решка) {orauthor1.name} x {ormember1.name} (Орёл)')
                                await channel.send(embed = e1)
                                await ormsg1.delete()
                            elif n == 1:
                                self.coll.update_one({"_id": orauthor1.id}, {"$inc": {"cash": ccg1}})
                                self.coll.update_one({"_id": ormember1.id}, {"$inc": {"cash": -ccg1}})
                                self.coll.update_one({"_id": 1}, {"$inc": {"cash": ccg1}})
                                e2 = discord.Embed(description = f'**Выпало: Решка\nПобеда {orauthor1.mention}, + {ccg1} Cooper Coins**', color = 0x00ff05)
                                e2.set_author(name = f'{payload.member.guild.name} | Орёл - Решка', icon_url = payload.member.guild.icon_url)
                                e2.set_footer(text = f'(Решка) {orauthor1.name} x {ormember1.name} (Орёл)')
                                await channel.send(embed = e2)
                                await ormsg1.delete()
                            else:
                                return
                if (payload.member.id == ormember1.id or payload.member.id == orauthor1.id):
                    if payload.message_id == ormsg1.id:
                        if payload.emoji.id == 768155761171234887:
                            await ormsg1.delete()
        except NameError:
            return

def setup(client):
    client.add_cog(Economy(client))
