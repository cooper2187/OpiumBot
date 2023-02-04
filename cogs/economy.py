import disnake
from disnake.ext import commands
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
from file1 import triada_num
from main import sets

dep_options = [
    disnake.SelectOption(label = 'Мой депозит', value = "info", description = "Информация о депозит", emoji = "💵"),
    disnake.SelectOption(label = 'Пополнить депозит', value = "put", description = "Положить Cooper Coins на депозит счет", emoji = "🪙"),
    disnake.SelectOption(label = 'Снять депозит', value = "take", description = "Снять Cooper Coins с депозит счёта", emoji = "🪙"),
    disnake.SelectOption(label = 'Расчитать депозит', value = "calc", description = "Калькулятор депозита", emoji = "📟")
]

dep_options1 = [
    disnake.SelectOption(label = 'Мой депозит', value = "info", description = "Информация о депозит", emoji = "💵"),
    disnake.SelectOption(label = 'Пополнить депозит', value = "put", description = "Положить Cooper Coins на депозит счет", emoji = "🪙"),
    disnake.SelectOption(label = 'Снять депозит', value = "take", description = "Снять Cooper Coins с депозит счёта", emoji = "🪙"),
    disnake.SelectOption(label = 'Расчитать депозит', value = "calc", description = "Калькулятор депозита", emoji = "📟"),
    disnake.SelectOption(label = 'Выход', value = "exit", description = "Вернуться в главное меню", emoji = "🔙")
]

class MyModal(disnake.ui.Modal):
    def __init__(self, title, components):
        self.cluster = MongoClient("mongodb+srv://andrewnobot:xuInmV8QmD9GRR5c@cluster0.28biu.mongodb.net/opiumdb?retryWrites=true&w=majority")
        self.coll = self.cluster.opiumdb.collopiumdb
        super().__init__(title = title, components = components)

    async def callback(self, interaction: disnake.ModalInteraction):
        try:
            amount = 0
            for a in dict.values(interaction.text_values):
                amount = int(a)
            money = self.coll.find_one({"_id": interaction.author.id})["cash"]
            if amount <= 0:
                await interaction.response.edit_message(embed = disnake.Embed(description = f'**{interaction.author.mention}, введены некорректные данные**', color = 0xff0000), view = Select1().add_item(MyDeposit(options = dep_options1, placeholder = "⚙️ Выберите опцию для управления счётом")))
            elif amount > money:
                await interaction.response.edit_message(embed = disnake.Embed(description = f'**{interaction.author.mention}, y вас недостаточно Cooper Coins!**', color = 0xff0000), view = Select1().add_item(MyDeposit(options = dep_options1, placeholder = "⚙️ Выберите опцию для управления счётом")))
            else:
                self.coll.update_one({"_id": interaction.author.id}, {"$inc": {"cash": -amount}})
                self.coll.update_one({"_id": interaction.author.id}, {"$inc": {"deposit": amount}})
                emb = disnake.Embed(description = f'**Вы положили `{amount}` Cooper Coins на ваш депозит счёт**', color = 0x28e91c)
                emb.set_author(name = f'{interaction.author} | Пополнение депозита', icon_url = interaction.author.avatar)
                emb.set_footer(text = f'Баланс депозита • {int(self.coll.find_one({"_id": interaction.author.id})["deposit"])} Cooper Coins')
                await interaction.response.edit_message(embed = emb, view = Select1().add_item(MyDeposit(options = dep_options1, placeholder = "⚙️ Выберите опцию для управления счётом")))
        except ValueError:
            await interaction.response.edit_message(embed = disnake.Embed(description = f'**{interaction.author.mention}, введены некорректные данные**', color = 0xff0000), view = Select1().add_item(MyDeposit(options = dep_options1, placeholder = "⚙️ Выберите опцию для управления счётом")))


class MyModal1(disnake.ui.Modal):
    def __init__(self, title, components):
        self.cluster = MongoClient("mongodb+srv://andrewnobot:xuInmV8QmD9GRR5c@cluster0.28biu.mongodb.net/opiumdb?retryWrites=true&w=majority")
        self.coll = self.cluster.opiumdb.collopiumdb
        super().__init__(title = title, components = components)

    async def callback(self, interaction: disnake.ModalInteraction):
        try:
            amount = 0
            for a in dict.values(interaction.text_values):
                amount = int(a)
            money = self.coll.find_one({"_id": interaction.author.id})["deposit"]
            if amount <= 0:
                await interaction.response.edit_message(embed = disnake.Embed(description = f'**{interaction.author.mention}, введены некорректные данные**', color = 0xff0000), view = Select1().add_item(MyDeposit(options = dep_options1, placeholder = "⚙️ Выберите опцию для управления счётом")))
            elif amount > money:
                await interaction.response.edit_message(embed = disnake.Embed(description = f'**{interaction.author.mention}, у вас недостаточно Cooper Coins на депозите**', color = 0xff0000), view = Select1().add_item(MyDeposit(options = dep_options1, placeholder = "⚙️ Выберите опцию для управления счётом")))
            else:
                self.coll.update_one({"_id": interaction.author.id}, {"$inc": {"deposit": -amount}})
                self.coll.update_one({"_id": interaction.author.id}, {"$inc": {"cash": amount}})
                emb = disnake.Embed(description = f'**Вы сняли `{amount}` Cooper Coins с вашего депозит счёта**', color = 0xd36262)
                emb.set_author(name = f'{interaction.author} | Снятие депозита', icon_url = interaction.author.avatar)
                emb.set_footer(text = f'Баланс депозита • {int(self.coll.find_one({"_id": interaction.author.id})["deposit"])} Cooper Coins')
                await interaction.response.edit_message(embed = emb, view = Select1().add_item(MyDeposit(options = dep_options1, placeholder = "⚙️ Выберите опцию для управления счётом")))
        except ValueError:
            await interaction.response.edit_message(embed = disnake.Embed(description = f'**{interaction.author.mention}, введены некорректные данные**', color = 0xff0000), view = Select1().add_item(MyDeposit(options = dep_options1, placeholder = "⚙️ Выберите опцию для управления счётом")))

class MyModal3(disnake.ui.Modal):
    def __init__(self, title, components):
        self.cluster = MongoClient("mongodb+srv://andrewnobot:xuInmV8QmD9GRR5c@cluster0.28biu.mongodb.net/opiumdb?retryWrites=true&w=majority")
        self.coll = self.cluster.opiumdb.collopiumdb
        super().__init__(title = title, components = components)

    async def callback(self, interaction: disnake.ModalInteraction):
        try:
            var_list = []
            for a in dict.values(interaction.text_values):
                var_list.append(int(a))
            hours = var_list[0]
            summ = var_list[1]
            if hours > 2160 and interaction.author.id != 382522784841990144:
                await interaction.response.edit_message(embed = disnake.Embed(description = f'**{interaction.author.mention}, не более 2160 часов!**', color = 0xff0000), view = Select1().add_item(MyDeposit(options = dep_options1, placeholder = "⚙️ Выберите опцию для управления счётом")))
            elif hours <= 0:
                await interaction.response.edit_message(embed = disnake.Embed(description = f'**{interaction.author.mention}, введены некорректные данные**', color = 0xff0000), view = Select1().add_item(MyDeposit(options = dep_options1, placeholder = "⚙️ Выберите опцию для управления счётом")))
            else:
                dep = summ
                s = []
                i = 0
                while i < hours:
                    if (dep >= 1 and dep <= 99999):
                        procent = 1.02
                    elif (dep >= 100000 and dep <= 999999):
                        procent = 1.01
                    elif (dep >= 1000000 and dep <= 9999999):
                        procent = 1.005
                    elif (dep >= 10000000 and dep <= 99999999):
                        procent = 1.0025
                    elif (dep >= 100000000 and dep <= 1000000000):
                        procent = 1.000625
                    elif (dep >= 1000000000 and dep <= 10000000000):
                        procent = 1.00015
                    elif (dep >= 10000000000 and dep <= 100000000000):
                        procent = 1.00004
                    elif (dep >= 100000000000 and dep <= 1000000000000):
                        procent = 1.000005
                    else:
                        break
                    s.append(dep * procent)
                    i = i + 1
                    dep = dep * procent
                sn = int(s[hours - 1])
                if summ is None:
                    z = int(sn - (self.coll.find_one({"_id": interaction.author.id})["deposit"]))
                else:
                    z = int(sn - summ)
                await interaction.response.edit_message(embed = disnake.Embed(description = f'**На вашем депозит счёте будет:** {triada_num(sn)} **Cooper Coins\n(разница** {triada_num(z)} **cc)**', color = 0xcd14d3), view = Select1().add_item(MyDeposit(options = dep_options1, placeholder = "⚙️ Выберите опцию для управления счётом")))
        except ValueError:
            await interaction.response.edit_message(embed = disnake.Embed(description = f'**{interaction.author.mention}, введены некорректные данные**', color = 0xff0000), view = Select1().add_item(MyDeposit(options = dep_options1, placeholder = "⚙️ Выберите опцию для управления счётом")))

class MyDeposit(disnake.ui.Select):
    def __init__(self, options, placeholder):
        self.cluster = MongoClient("mongodb+srv://andrewnobot:xuInmV8QmD9GRR5c@cluster0.28biu.mongodb.net/opiumdb?retryWrites=true&w=majority")
        self.coll = self.cluster.opiumdb.collopiumdb
        super().__init__(placeholder = placeholder, options = options, max_values = 1)
    async def callback(self, interaction: disnake.Interaction):
        data = self.coll.find_one({"_id": interaction.author.id})
        for val in self.values:
            if val == "info":
                data = self.coll.find_one({"_id": interaction.author.id})
                dep = data["deposit"]
                emb = disnake.Embed(description = f'**Баланс вашего депозит счёта: `{int(dep)}` Cooper Coins**', timestamp = interaction.created_at, color = 0x6117e0)
                emb.set_author(name = f'{interaction.author} | Депозит', icon_url = interaction.author.avatar)
                emb.set_footer(text = f'Opium 🌴 Bot')
                await interaction.response.edit_message(embed = emb, view = Select1().add_item(MyDeposit(options = dep_options1, placeholder = "💵 Мой депозит")))
            elif val == 'put':
                await interaction.response.send_modal(MyModal(title = "Пополнение депозита", components = [disnake.ui.TextInput(label = f"Баланс • {triada_num(data['cash'])} Cooper Coins", placeholder = "Введите количество монет", style = disnake.TextInputStyle.short, value = None, custom_id = "ttss", min_length = 1, max_length = 20)]))
            elif val == 'take':
                await interaction.response.send_modal(MyModal1(title = "Снятие депозита", components = [disnake.ui.TextInput(label = f"Баланс депозита • {triada_num(int(data['deposit']))} Cooper Coins", placeholder = "Введите количество монет", style = disnake.TextInputStyle.short, value = None, custom_id = "ttss", min_length = 1, max_length = 20)]))
            elif val == 'calc':
                options = [
                        disnake.ui.TextInput(label = "Не более 2 160 часов!", placeholder = "Введите количество часов", style = disnake.TextInputStyle.short, value = None, custom_id = "dc", min_length = 1, max_length = 4),
                        disnake.ui.TextInput(label = "Сумма от которой будет рассчитываться депозит", placeholder = "Введите сумму депозита", style = disnake.TextInputStyle.short, value = int(data['deposit']), custom_id = 'dc1', min_length = 1, max_length = 20)
                    ]
                await interaction.response.send_modal(MyModal3(title = "Калькулятор депозита", components = options))
            elif val == 'exit':
                dep = int(self.coll.find_one({"_id": interaction.author.id})['deposit'])
                i = 0
                n = 10
                el = ['🔹']
                while i < 7:
                    if (dep >= 10000 * n and dep <= 99999 * n):
                        el.append('🔸')
                    else:
                        el.append('🔹')
                    i += 1
                    n = n * 10
                if (dep >= 1 and dep <= 99999):
                    el = ['🔸', '🔹', '🔹', '🔹' ,'🔹' ,'🔹' ,'🔹' ,'🔹']
                emb = disnake.Embed(description = "**⏳ Депозит начисляется 1 раз в час.\n\n🔋 Процентная ставка:**\n ", color = 0x6117e0, timestamp = interaction.created_at)
                emb.set_author(name = f"{interaction.author.name}#{interaction.author.discriminator} | Депозит меню", icon_url = interaction.author.display_avatar)
                emb.add_field(name = '🔰 Уровень', value = f"{el[0]} 1 LVL\n{el[1]} 2 LVL\n{el[2]} 3 LVL\n{el[3]} 4 LVL\n{el[4]} 5 LVL\n{el[5]} 6 LVL\n{el[6]}7 LVL\n{el[7]} 8 LVL")
                emb.add_field(name = "💰 Баланс", value = f"{el[0]} 1 - 100K\n{el[1]} 100K - 1M\n{el[2]} 1M - 10M\n{el[3]} 10M - 100M\n{el[4]} 100M - 1B\n{el[5]} 1B - 10B\n{el[6]} 10B - 100B\n{el[7]} 100B - 1T")
                emb.add_field(name = "🔋 Процент", value = f"{el[0]} 2%\n{el[1]} 1%\n{el[2]} 0.5%\n{el[3]} 0.25%\n{el[4]} 0.0625%\n{el[5]}0.015%\n{el[6]} 0.004%\n{el[7]} 0.0005%")
                emb.set_thumbnail(url = "https://img.freepik.com/free-vector/money-bag-with-pile-coins-and-bills-cash_24877-63660.jpg?w=2000")
                emb.set_footer(text = "Opium 🌴 Team", icon_url = "https://images-ext-2.discordapp.net/external/0k7jh0lZJpaJSxawcHt4wV3kF2D7Eltmso22nbAhIPM/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/722921602026700861/654ff8c616269acc148f204c17670aaa.png?width=671&height=671")
                placeholder = "⚙️ Выберите опцию для управления счётом"
                await interaction.response.edit_message(embed = emb, view = Select1().add_item(MyDeposit(options = dep_options, placeholder = placeholder)))
            else:
                pass

class Select1(disnake.ui.View):
    def __init__(self):
        super().__init__()

class EconomyNew(commands.Cog):

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
            "deposit": 0,
            "jpwin": 2500
        }
        if self.coll.count_documents({"_id": member.id}) == 0:
            self.coll.insert_one(post)


    #ON MESSAGE
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if not message.guild.id == 430772415480594443:
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
            await message.channel.send(embed = disnake.Embed(description = f'**Пользователь {user.mention} получил новый уровень: `{data["lvl"] + 1}` (+{cash_up} cc)**', color = 0xd7ff5d))
   
    #BALANCE
    @commands.slash_command(description = "Economy: Баланс пользователя")
    async def balance(self, ctx: disnake.AppCmdInter, member: disnake.Member = None):
        if member is None:
            await ctx.send(embed = disnake.Embed(description = f'**Баланс пользователя {ctx.author.mention}: {triada_num(self.coll.find_one({"_id": ctx.author.id})["cash"])} Cooper Coins**', color = 0x00a5ff))
        else:
            await ctx.send(embed = disnake.Embed(description = f'**Баланс пользователя {member.mention}: {triada_num(self.coll.find_one({"_id": member.id})["cash"])} Cooper Coins**', color = 0x00a5ff))

    #STATS
    @commands.slash_command(description = "Economy: Статистика пользователя")
    async def stats(self, ctx: disnake.AppCmdInter, member: disnake.Member = None):
        if member is None:
            m = ctx.author
            data = self.coll.find_one({"_id": ctx.author.id})
        else:
            data = self.coll.find_one({"_id": member.id})
            m = member
        a_xp = data["xp"]
        a_cash = triada_num(data["cash"])
        d_cash = triada_num(int(data['deposit']))
        a_lvl = data["lvl"]
        sbonus = data["sbonus"]
        spot = data["spot"]
        dsbonus = data["dsbonus"]
        lvl_xp = 10 + 10 * data["lvl"]
        emb = disnake.Embed(description = f'**Пользователь: {m.mention}\n\nУровень: `{a_lvl}` Lvl\nОпыт: `{a_xp}`/`{lvl_xp}` Xp\nБаланс: `{a_cash}` Cooper Coins\nБаланс депозита: `{d_cash}` Cooper Coins**', color = 0x00ffd5)
        emb.set_author(name = f'{m} | Статистика', icon_url = m.avatar)
        emb.add_field(name = 'Навыки:', value = f'\n**💿 Рулетка(выигрыш): от `{round((sbonus - 9) * 0.7)}` до `{sbonus}` cc\n💿 Рулетка(процент Jackpot): `{spot}%`\n📀 Ежедневная рулетка(выигрыш): от `{round((dsbonus - 20) * 0.7)}` до `{dsbonus}` cc**')
        emb.set_footer(text = 'Opium 🌴 Team', icon_url = 'https://images-ext-2.disnakeapp.net/external/0k7jh0lZJpaJSxawcHt4wV3kF2D7Eltmso22nbAhIPM/%3Fsize%3D1024/https/cdn.disnakeapp.com/avatars/722921602026700861/654ff8c616269acc148f204c17670aaa.png?width=671&height=671')
        await ctx.send(embed = emb)
  
    #PAY
    @commands.slash_command(description = "Economy: Передать Cooper Coins другому пользователю")
    async def pay(self, ctx: disnake.AppCmdInter, member: disnake.Member, amount: int = commands.Param(gt = 0)):
        acash = self.coll.find_one({"_id": ctx.author.id})["cash"]
        mcash = self.coll.find_one({"_id": member.id})["cash"]
        if amount > acash:
            ctx.send(embed = disnake.Embed(description = f'**{ctx.author.mention}, y вас недостаточно Cooper Coins!**', color = 0xff0000), ephemeral = True)
        elif ctx.author == member:
            await ctx.send(embed = disnake.Embed(description = f'**{ctx.author.mention}, нельзя передавть самому себе!**', color = 0xff0000), ephemeral = True)
        else:
            self.coll.update_one({"_id": ctx.author.id},
            {"$set": {"cash": acash - amount}})

            self.coll.update_one({"_id": member.id},
            {"$set": {"cash": mcash + amount}})

            self.coll.update_one({"_id": 1}, {"$inc": {"cash": amount}})
            await ctx.send(embed = disnake.Embed(description = f'**{ctx.author.mention} передал(a) {member.mention} `{amount}` Cooper Coins**', color = 0xbeff00))
    

    #SET BALANCE
    @sets.sub_command(name = "balance", description = "Economy: Установить баланс")
    async def set_balance(self, ctx: disnake.AppCmdInter, member: disnake.Member, amount: int):
        if amount < 0:
            await ctx.send(embed = disnake.Embed(description = f'**{ctx.author.mention}, введены некорректные данные**', color = 0xff0000), ephemeral = True)
        else:
            self.coll.update_one({"_id": member.id},
            {"$set": {"cash": amount}})
            await ctx.send(embed = disnake.Embed(description = f'**Модератор `{ctx.author.display_name}` установил баланс пользователю\n`{member.display_name}`: `{self.coll.find_one({"_id": member.id})["cash"]}` сс**', color = 0x20947a))

    #SET LVL
    @sets.sub_command(name = "lvl", description = "Economy: Установить уровень")
    async def set_lvl(self, ctx: disnake.AppCmdInter, member: disnake.Member, lvl: int):
        if lvl <= 0:
            await ctx.send(embed = disnake.Embed(description = f'**{ctx.author.mention}, введены некорректные данные**', color = 0xff0000), ephemeral = True)
        else:
            self.coll.update_one({"_id": member.id}, {"$set": {"lvl": lvl}})
            await ctx.send(embed = disnake.Embed(description = f'**Модератор `{ctx.author.display_name}` установил `{self.coll.find_one({"_id": member.id})["lvl"]}` уровень\nпользователю `{member.display_name}`**', color = 0x20947a))

    #DELETE STATS
    @commands.slash_command(description = "Economy: Обнулить статистику участнику")
    @commands.default_member_permissions(administrator = True)
    async def delete_stats(self, ctx: disnake.AppCmdInter, member: disnake.Member):
        await ctx.send(embed = disnake.Embed(description = f'**Модератор {ctx.author.mention} обнулил статистику пользователю {member.mention}**', color = 0xc98224))
        up = self.coll.update_one
        m = {"_id": member.id}
        up(m, {"$set": {"cash": 10}})
        up(m, {"$set": {"xp": 0}})
        up(m, {"$set": {"lvl": 1}})
        up(m, {"$set": {"daily": 1}})
        up(m, {"$set": {"sbonus": 10}})
        up(m, {"$set": {"spot": 0}})
        up(m, {"$set": {"dsbonus": 50}})
        up(m, {"$set": {"splist": [0]}})
        up(m, {"$set": {"sprice": 50}})
        up(m, {"$set": {"dsprice": 50}})
        up(m, {"$set": {"loan": 0}})
        up(m, {"$set": {"deposit": 0}})
        up(m, {"$set": {"jpwin": 2500}})

    #SPIN
    @commands.slash_command(description = "Economy: Рулетка(1 раз в час)")
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def spin(self, ctx: disnake.AppCmdInter):
        prefix = self.prx.find_one({"_id": ctx.guild.id})["prefix"]
        sbonus = self.coll.find_one({"_id": ctx.author.id})["sbonus"]
        splist = self.coll.find_one({"_id": ctx.author.id})["splist"]
        n1 = randint(1, 101)
        if n1 in splist:
            self.coll.update_one({"_id": ctx.author.id}, {"$inc": {"cash": 2500}})
            self.coll.update_one({"_id": 1}, {"$inc": {"cash": -2500}})
            self.coll.update_one({"_id": 1}, {"$inc": {"bonus_cash": 25}})
            emb = disnake.Embed(title = 'Джекпот 🤩 🥳 🎉',description = f'**Выигрыш: {triada_num(2500)} cc**', color = 0xffa000)
            emb.set_author(name = ctx.author, icon_url = ctx.author.avatar)
            emb.set_footer(text = f'Баланс • {triada_num(self.coll.find_one({"_id": ctx.author.id})["cash"])} Cooper Coins')
            await ctx.send(embed = emb)
            channel = self.client.get_channel(789806580891123752)
            com = ', '
            await channel.send(embed = disnake.Embed(description = f"**User {ctx.author.mention} got a jackpot with code number: `{n1}`\nList of his lucky numbers:\n`{com.join(map(str, splist))}`**", color = 0xffa000))
        else:
            msb = round((sbonus - 9) * 0.7)
            n = randint(msb, sbonus)
            self.coll.update_one({"_id": ctx.author.id}, {"$inc": {"cash": n}})
            self.coll.update_one({"_id": 1}, {"$inc": {"cash": -n}})
            self.coll.update_one({"_id": 1}, {"$inc": {"bonus_cash": n * 0.01}})
            emb = disnake.Embed(description = f'**Выигрыш: `{triada_num(n)}` cc**', color = 0x00ff2e)
            emb.set_author(name = ctx.author, icon_url = ctx.author.avatar)
            emb.set_footer(text = f'Баланс • {triada_num(self.coll.find_one({"_id": ctx.author.id})["cash"])} Cooper Coins')
            await ctx.send(embed = emb)

    #SPIN ERROR
    @spin.error
    async def spin_error(self, ctx, error):
        if isinstance(error, disnake.ext.commands.errors.CommandOnCooldown):
            m = time.strftime("%M", time.gmtime(error.retry_after))
            s = time.strftime("%S", time.gmtime(error.retry_after))
            if int(m) < 10:
                m = m[1:]
            else:
                pass
            await ctx.send(embed = disnake.Embed(description = '**Ты уже сыграл. Следующая попытка через {} мин. {} сек.**'.format(m, s), color = 0xff0000), ephemeral = True)

    #TRY
    @commands.slash_command(description = "Economy: Удвоить сумму. Шанс 50%", name = 'try')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def _try(self, ctx, amount: int = commands.Param(gt = 0, lt = 1000)):
        cs = ctx.send
        de = disnake.Embed
        money = self.coll.find_one({"_id": ctx.author.id})["cash"]
        if amount > money:
            await cs(embed = de(description = f'**{ctx.author.mention}, y вас недостаточно Cooper Coins!**', color = 0xff0000), ephemeral = True)
        else:
            n = randint(1, 20)
            a = [10, 5, 2, 1, 4, 7, 12, 9, 15, 11] 
            b = [18, 17, 19, 6, 16, 3, 14, 20, 8, 13]
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
            self.coll.update_one({"_id": 1}, {"$inc": {"cash": -x}})
            emb = de(description = win, color = clr)
            emb.set_author(name = ctx.author, icon_url = ctx.author.avatar)
            emb.set_footer(text = f'Баланс • {triada_num(self.coll.find_one({"_id": ctx.author.id})["cash"])} Cooper Coins')
            await cs(embed = emb)

    #TRY ERROR
    @_try.error
    async def _try_error(self, ctx, error):
        if isinstance(error, disnake.ext.commands.errors.CommandOnCooldown):
            await ctx.send(f"**{ctx.author.mention}, воу, воу, не так бысто!**", ephemeral = True)

    #SPIN UP
    @commands.slash_command(description = "Economy: Повышение макс. выигрыша в рулетке")
    async def spin_up(self, ctx, count: int = None):
        if count is None:
            data = self.coll.find_one({"_id": ctx.author.id})
            cash = data["cash"]
            sbonus = data["sbonus"]
            sprice = data["sprice"]
            if cash < sprice:
                await ctx.send(embed = disnake.Embed(description = f'**{ctx.author.mention}, у вас недостаточно Cooper Coins. {cash}/{sprice} cc**', color = 0xff0000), ephemeral = True)
            else:
                self.coll.update_one({"_id": ctx.author.id}, {"$inc": {"cash": -sprice}})
                emb = disnake.Embed(title = f'Повышение навыка x1 🔼 (-{sprice} cc)', description  = f'**💿 Рулетка(макс. выигрыш): `{sbonus}` -> `{sbonus + 1}` cc**', color = 0xfdff4b)
                emb.set_author(name = ctx.author, icon_url = ctx.author.avatar)
                emb.set_footer(text = f'Баланс • {triada_num(self.coll.find_one({"_id": ctx.author.id}))["cash"]} cc | Next update • {sprice + 5} cc')
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
            if cash < s:
                await ctx.send(embed = disnake.Embed(description = f'**{ctx.author.mention}, у вас недостаточно Cooper Coins. {cash}/{s} cc**', color = 0xff0000), ephemeral = True)
            else:
                self.coll.update_one({"_id": ctx.author.id}, {"$inc": {"cash": -s}})
                emb = disnake.Embed(title = f'Повышение навыка x{count} 🔼 (-{s} cc)', description  = f'**💿 Рулетка(макс. выигрыш): `{sbonus}` -> `{sbonus + (count * 1)}` cc**', color = 0xfdff4b)
                emb.set_author(name = ctx.author, icon_url = ctx.author.avatar)
                emb.set_footer(text = f'Баланс • {triada_num(self.coll.find_one({"_id": ctx.author.id})["cash"])} cc | Next update • {a + 5} cc')
                await ctx.send(embed = emb)
                self.coll.update_one({"_id": ctx.author.id}, {"$inc": {"sbonus": count * 1}})
                self.coll.update_one({"_id": ctx.author.id}, {"$set": {"sprice": a + 5}})

    #DAILY SPIN UP        
    @commands.slash_command(description = "Economy: Повышение макс. выигрыша в ежедневной рулетке")
    async def daily_spin_up(self, ctx, count: int = None):
        if count is None:
            data = self.coll.find_one({"_id": ctx.author.id})
            cash = data["cash"]
            dsbonus = data["dsbonus"]
            dsprice = data["dsprice"]
            if cash < dsprice:
                await ctx.send(embed = disnake.Embed(description = f'**{ctx.author.mention}, у вас недостаточно Cooper Coins. {cash}/{dsprice} cc**', color = 0xff0000), ephemeral = True)
            else:
                self.coll.update_one({"_id": ctx.author.id}, {"$inc": {"cash": -dsprice}})
                emb = disnake.Embed(title = f'Повышение навыка x1 🔼 (-{dsprice} cc)', description  = f'**📀 Ежедневная рулетка(макс. выигрыш): `{dsbonus}` -> `{dsbonus + 5}` cc**', color = 0xfdff4b)
                emb.set_author(name = ctx.author, icon_url = ctx.author.avatar)
                emb.set_footer(text = f'Баланс • {triada_num(self.coll.find_one({"_id": ctx.author.id})["cash"])} cc | Next update • {dsprice + 5} cc')
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
            if cash < s:
                await ctx.send(embed = disnake.Embed(description = f'**{ctx.author.mention}, у вас недостаточно Cooper Coins. {cash}/{s} cc**', color = 0xff0000), ephemeral = True)
            else:
                self.coll.update_one({"_id": ctx.author.id}, {"$inc": {"cash": -s}})
                emb = disnake.Embed(title = f'Повышение навыка x{count} 🔼 (-{s} cc)', description  = f'**💿 Рулетка(макс. выигрыш): `{dsbonus}` -> `{dsbonus + (count * 5)}` cc**', color = 0xfdff4b)
                emb.set_author(name = ctx.author, icon_url = ctx.author.avatar)
                emb.set_footer(text = f'Баланс • {triada_num(self.coll.find_one({"_id": ctx.author.id})["cash"])} cc | Next update • {a + 5} cc')
                await ctx.send(embed = emb)
                self.coll.update_one({"_id": ctx.author.id}, {"$inc": {"dsbonus": count * 5}})
                self.coll.update_one({"_id": ctx.author.id}, {"$set": {"dsprice": a + 5}})

    #GIVE
    @commands.slash_command(description = "Economy: Передать деньги из банка участнику")
    @commands.default_member_permissions(administrator = True)
    async def give(self, ctx, member: disnake.Member, amount: int, *, reason = None):
        if amount <= 0:
            await ctx.send(embed = disnake.Embed(description = f'**{ctx.author.mention}, введены некорректные данные**', color = 0xff0000), ephemeral = True)
        else:
            self.coll.update_one({"_id": member.id}, {"$inc": {"cash": amount}})
            self.coll.update_one({"_id": 1}, {"$inc": {"cash": -amount}})
            emb = disnake.Embed(description = f'**`{ctx.author.display_name}` начислил `{amount}` Cooper Coins\nпользователю`{member.display_name}`. Причина: {reason}**', color = 0x20947a)
            await ctx.send(embed = emb)

    #BANK
    @commands.slash_command(description = "Economy: Состояние банка")
    async def bank(self, ctx):
        money = self.coll.find_one({"_id": 1})["cash"]
        bonus_cash = int(self.coll.find_one({"_id": 1})["bonus_cash"])
        e = disnake.Embed(description = f'**💸 Состояние банка: `{triada_num(money)}` Cooper Coins**\n**🤑 Состояние бонусного счёта: `{triada_num(bonus_cash)}` Cooper Coins**', timestamp = ctx.created_at, color = 0x5797af)
        e.set_author(name = f'{ctx.guild.name} | Genesis Bank', icon_url = ctx.guild.icon)
        e.set_footer(text = 'Opium Team')
        await ctx.send(embed = e)		

    #DAILY SPIN
    @commands.slash_command(description = "Ежеднеыная рулетка")
    async def daily_spin(self, ctx):
        data = self.coll.find_one({"_id": ctx.author.id})
        dsbonus = data["dsbonus"]
        spot = data["spot"]
        sp = spot + 1
        sbonus = data["sbonus"]
        daily = self.coll.find_one({"_id": ctx.author.id})["daily"]
        if daily == 1:
            mdsb = round((dsbonus - 20) * 0.7)
            n = randint(mdsb, dsbonus)
            data = self.coll.find_one({"_id": ctx.author.id})
            x = 2 + 2 * data["lvl"]
            self.coll.update_one({"_id": ctx.author.id}, {"$inc": {"xp": x}})
            self.coll.update_one({"_id": ctx.author.id}, {"$inc": {"cash": n}})
            emb = disnake.Embed(title = 'Ежедневный бонус ✅', description = f'**Награды:\n💰 {triada_num(n)} Cooper Coins\n💎 {x} Xp**\n', color = 0x00ff2e)
            if spot < 15:
                emb.add_field(name = 'Повышение навыков ⬆️', value = f'**💿 Рулетка(макс. выигрыш): `{sbonus}` -> `{sbonus + 5}` cc\n💿 Рулетка(процент Jackpot): `{spot}%` -> `{sp}%`\n📀 Ежедневная рулетка(макс. выигрыш): `{dsbonus}` -> `{dsbonus + 10}` cc**')
                lst = sample(range(1, 102), sp)
                self.coll.update_one({"_id": ctx.author.id}, {"$set": {"splist": lst}})
                self.coll.update_one({"_id": ctx.author.id}, {"$set": {"spot": sp}})
            else:
                emb.add_field(name = 'Повышение навыков ⬆️', value = f'**💿 Рулетка(макс. выигрыш): `{sbonus}` -> `{sbonus + 5}` cc\n💿 Рулетка(процент Jackpot): `{spot}%` Max Lvl\n📀 Ежедневная рулетка(макс. выигрыш): `{dsbonus}` -> `{dsbonus + 10}` cc**')
            emb.set_author(name = ctx.author, icon_url = ctx.author.avatar)
            emb.set_footer(text = f'Баланс • {triada_num(self.coll.find_one({"_id": ctx.author.id})["cash"])} Cooper Coins')
            await ctx.send(embed = emb)
            self.coll.update_one({"_id": ctx.author.id}, {"$set": {"sbonus": sbonus + 5}})
            self.coll.update_one({"_id": ctx.author.id}, {"$set": {"dsbonus": dsbonus + 10}})
            self.coll.update_one({"_id": ctx.author.id}, {"$set": {"daily": 2}})
            self.coll.update_one({"_id": 1}, {"$inc": {"cash": -n}})
            self.coll.update_one({"_id": 1}, {"$inc": {"bonus_cash": n * 0.01}})
        else:
            await ctx.send(embed = disnake.Embed(description = '**Ты сегодня уже играл!**', color = 0xff0004))

    #TOP PLAYERS [COOPER COINS\LEVEL]
    @commands.slash_command(name = 'topplayers', description = "Списки лидеров")
    async def topplayers(self, ctx, name = commands.Param(choices = ["По уровню", "По балансу"])):
        prefix = self.prx.find_one({"_id": ctx.guild.id})["prefix"]
        if name == 'По балансу':
            top = self.coll.find().sort("cash", -1).limit(6).skip(2)
            leaders = []
            for t in top:
                leaders.append(f"<@{t['_id']}>: {t['cash']}")
            emb = disnake.Embed(description = f"**1. {leaders[0]} Cooper Coins\n\n2. {leaders[1]} Cooper Coins\n\n3. {leaders[2]} Cooper Coins\n\n4. {leaders[3]} Cooper Coins\n\n5. {leaders[4]} Cooper Coins**", color = 0x32aafd, timestamp = ctx.created_at)
            emb.set_author(name = f'{ctx.guild.name} | Leaderboard (Balance)', icon_url = ctx.guild.icon)
            emb.set_footer(text = 'Opium Team', icon_url = 'https://cdn.disnakeapp.com/avatars/722921602026700861/654ff8c616269acc148f204c17670aaa.webp?size=1024')
            await ctx.send(embed = emb)
        elif name == 'По уровню':
            top = self.coll.find().sort("lvl", -1).limit(6).skip(1)
            leaders = []
            for t in top:
                leaders.append(f"<@{t['_id']}>: {t['lvl']}")
            emb = disnake.Embed(description = f"**1. {leaders[0]} уровень\n\n2. {leaders[1]} уровень\n\n3. {leaders[2]} уровень\n\n4. {leaders[3]} уровень\n\n5. {leaders[4]} уровень**", color = 0x32aafd, timestamp = ctx.created_at)
            emb.set_author(name = f'{ctx.guild.name} | Leaderboard (Lvl)', icon_url = ctx.guild.icon)
            emb.set_footer(text = 'Opium Team', icon_url = 'https://cdn.disnakeapp.com/avatars/722921602026700861/654ff8c616269acc148f204c17670aaa.webp?size=1024')
            await ctx.send(embed = emb)
        else:
            pass

    #UP INFO            
    @commands.slash_command(description = "Информация о повышении навыков")
    async def up_info(self, ctx):
        data = self.coll.find_one({"_id": ctx.author.id})
        sp = data["sprice"]
        dsp = data["dsprice"]
        cash = data["cash"]
        discr = (2 * sp - 5) ** 2 + 40 * cash
        n1 = (-(2 * sp - 5) + math.sqrt(discr)) / (10)
        discr1 = (2 * dsp - 5) ** 2 + 40 * cash
        n2 = (-(2 * dsp - 5) + math.sqrt(discr1)) / (10)
        emb = disnake.Embed(title = f'Цены на повышение навыков для {ctx.author.display_name}', description = f'**💿 Рулетка. Цена: {sp} Cooper Coins**\n        (Можно улучшить {int(n1)} раз)\n**📀 Ежедневная рулетка. Цена: {dsp} Cooper Coins**\n        (Можно улучшить {int(n2)} раз)', color = 0x256845)
        emb.set_author(name = ctx.author, icon_url = ctx.author.avatar)
        emb.set_footer(text = f'Баланс • {triada_num(self.coll.find_one({"_id": ctx.author.id})["cash"])} Cooper Coins')
        await ctx.send(embed = emb)

    #CREDIR
    @commands.slash_command(description = "Economy: Выдать кредит ")
    @commands.default_member_permissions(administrator = True)
    async def credit(self, ctx, member: disnake.Member, amount: int):
        proc = round(amount * 1.3)
        self.coll.update_one({"_id": member.id}, {"$inc": {"loan": proc}})
        self.coll.update_one({"_id": member.id}, {"$inc": {"cash": amount}})
        self.coll.update_one({"_id": 1}, {"$inc": {"cash": -amount}})
        self.coll.update_one({"_id": 1}, {"$inc": {"bonus_cash": amount * 0.01}})
        await ctx.send(embed = disnake.Embed(description  = f'**Модератор {ctx.author.mention} выдал кередит пользователю {member.mention} в размере `{amount}` Cooper Coins. Вернуть: {proc}**', color = 0xb9ff00))

    #MYCREDIT
    @commands.slash_command(description = "Economy: Информация о кредите")
    async def mycredit(self, ctx):
        loan = self.coll.find_one({"_id": ctx.author.id})['loan']
        if loan == 0:
            await ctx.send(embed = disnake.Embed(description = f'**{ctx.author.mention}, у вас нету непогашенных кредитов!**', color = 0x854be8))
        else:
            emb = disnake.Embed(description = f'**{ctx.author.mention}, у вас имеется непогашенный кредит!**', timestamp = ctx.created_at, color = 0x007cc0)
            emb.set_author(name = ctx.author, icon_url = ctx.author.avatar)
            emb.add_field(name = 'Сумма:', value = f'{loan} Cooper Coins')
            emb.set_footer(text = 'Opium 🌴 Bot')
            await ctx.send(embed = emb)

    #RETURN CREDIT
    @commands.slash_command(description = "Economy: Погасить кредит")
    async def return_credit(self, ctx, amount: int):
        loan = self.coll.find_one({"_id": ctx.author.id})['loan']
        money = self.coll.find_one({"_id": ctx.author.id})["cash"]
        if amount > money:
            await ctx.send(embed = disnake.Embed(description = f'**{ctx.author.mention}, y вас недостаточно Cooper Coins!**', color = 0xff0000), ephemeral = True)
        elif loan == 0:
            await ctx.send(embed = disnake.Embed(description = f'**{ctx.author.mention}, у вас нету непогашенных кредитов!**', color = 0x854be8), ephemeral = True)
        elif amount <= 0:
            await ctx.send(embed = disnake.Embed(description = f'**{ctx.author.mention}, введены некорректные данные**', color = 0xff0000), ephemeral = True)
        elif amount == loan:
            self.coll.update_one({"_id": ctx.author.id}, {"$inc": {"loan": -amount}})
            self.coll.update_one({"_id": ctx.author.id}, {"$inc": {"cash": -amount}})
            self.coll.update_one({"_id": 1}, {"$inc": {"cash": amount}})
            await ctx.send(embed = disnake.Embed(description = '**Кредит погашен. Поздравляю!**', color = 0xffec00))
        elif amount < loan:
            self.coll.update_one({"_id": ctx.author.id}, {"$inc": {"loan": -amount}})
            self.coll.update_one({"_id": ctx.author.id}, {"$inc": {"cash": -amount}})
            self.coll.update_one({"_id": 1}, {"$inc": {"cash": amount}})
            await ctx.send(embed = disnake.Embed(description = f'**Вы внесли `{amount}` Cooper Coins. Осталось: `{self.coll.find_one({"_id": ctx.author.id})["loan"]}`**', color = 0xffec00))
        else:
            self.coll.update_one({"_id": ctx.author.id}, {"$inc": {"cash": -loan}})
            amount = amount - loan
            await ctx.send(embed = disnake.Embed(description = f'**Воу, вы внесли даже больше чем нужно. Кредит погашен. Возвращаю вам: `{amount}` Cooper Coins**', color = 0xffec00))
            self.coll.update_one({"_id": 1}, {"$inc": {"cash": loan}})
            self.coll.update_one({"_id": ctx.author.id}, {"$set": {"loan": 0}})

    #MYDEPOSIT
    @commands.slash_command(name = 'deposit', description = "Economy: Информация о депозите")
    async def mydeposit(self, ctx):
        depc = int(self.coll.find_one({"_id": ctx.author.id})['deposit'])
        i = 0
        n = 10
        el = ['🔹']
        while i < 7:
            if (depc >= 10000 * n and depc <= 99999 * n):
                el.append('🔸')
            else:
                el.append('🔹')
            i += 1
            n = n * 10
        if (depc >= 1 and depc <= 99999):
            el = ['🔸', '🔹', '🔹', '🔹' ,'🔹' ,'🔹' ,'🔹' ,'🔹']
        emb = disnake.Embed(description = "**⏳ Депозит начисляется 1 раз в час.\n\n🔋 Процентная ставка:**\n ", color = 0x6117e0, timestamp = ctx.created_at)
        emb.set_author(name = f"{ctx.author.name}#{ctx.author.discriminator} | Депозит меню", icon_url = ctx.author.display_avatar)
        emb.add_field(name = '🔰 Уровень', value = f"{el[0]} 1 LVL\n{el[1]} 2 LVL\n{el[2]} 3 LVL\n{el[3]} 4 LVL\n{el[4]} 5 LVL\n{el[5]} 6 LVL\n{el[6]}7 LVL\n{el[7]} 8 LVL")
        emb.add_field(name = "💰 Баланс", value = f"{el[0]} 1 - 100K\n{el[1]} 100K - 1M\n{el[2]} 1M - 10M\n{el[3]} 10M - 100M\n{el[4]} 100M - 1B\n{el[5]} 1B - 10B\n{el[6]} 10B - 100B\n{el[7]} 100B - 1T")
        emb.add_field(name = "🔋 Процент", value = f"{el[0]} 2%\n{el[1]} 1%\n{el[2]} 0.5%\n{el[3]} 0.25%\n{el[4]} 0.0625%\n{el[5]}0.015%\n{el[6]} 0.004%\n{el[7]} 0.0005%")
        emb.set_thumbnail(url = "https://img.freepik.com/free-vector/money-bag-with-pile-coins-and-bills-cash_24877-63660.jpg?w=2000")
        emb.set_footer(text = "Opium 🌴 Team", icon_url = "https://images-ext-2.discordapp.net/external/0k7jh0lZJpaJSxawcHt4wV3kF2D7Eltmso22nbAhIPM/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/722921602026700861/654ff8c616269acc148f204c17670aaa.png?width=671&height=671")
        placeholder = "⚙️ Выберите опцию для управления счётом"
        await ctx.response.send_message(embed = emb, view = Select1().add_item(MyDeposit(options = dep_options, placeholder = placeholder)), ephemeral = True)

    # #STATS(moderation)
    # @commands.slash_command(name = 'astats', description = "Economy: Полная статистика из БД")
    # @commands.default_member_permissions(administrator = True)
    # async def __astats(self, ctx, *, member: disnake.Member = None):
    #     if member is None:
    #         member = ctx.author
    #     else:
    #         member = member
    #     data = self.coll.find_one({"_id": member.id})
    #     u_id = data["_id"]
    #     g_id = data["g_id"]
    #     name = f"{member.name}#{member.discriminator}"
    #     g_name = self.client.get_guild(g_id).name
    #     cash = data["cash"] 
    #     xp = data["xp"]
    #     lvl = data["lvl"]
    #     daily = data["daily"]
    #     sbonus = data["sbonus"]
    #     spot = data["spot"]
    #     dsbonus = data["dsbonus"]
    #     splist = data["splist"]
    #     sprice = data["sprice"]
    #     dsprice = data["dsprice"]
    #     loan = data["loan"]
    #     deposit = data["deposit"]
    #     jpwin = data["jpwin"]
    #     tires = '— — — — — — — — — — — — — — — — — — — — — — — — —'
    #     emb = disnake.Embed(
    #         title = 'DB Document', 
    #         description = f'**User ID:** {u_id}\n**Guild ID:** {g_id}\n{tires}\n**User name:** {name}\n**Guild name:** {g_name}\n{tires}\n**Balance:** {cash}\n'
    #         f'**Xp:** {xp}\n**Lvl:** {lvl}\n{tires}\n**Spin(max. win):** {sbonus}\n**Daily spin(max. win):** {dsbonus}\n{tires}\n'
    #         f'**Jackpot(drop chance):** {spot}\n**Jackpot(win):** {jpwin}\n**Jackpot(list):** {splist}\n{tires}\n**Spin up(price):** {sprice}\n'
    #         f'**Daily spin up(price):** {dsprice}\n{tires}\n**Daily(status):** {daily}\n**Loan:** {loan}\n**Deposit:** {deposit}',
    #         timestamp = ctx.created_at,
    #         color = disnake.Colour.blue()
    #         )
    #     await ctx.send(embed = emb)

    #РАЗИГРАТЬ БОНУСНЫЙ СЧЁТ
    @commands.slash_command(description = 'Economy: Разиграть бонусный счёт')
    @commands.default_member_permissions(administrator = True)
    async def play_bonuses(self, ctx):
        a = []
        for  i in self.coll.find({'deposit': {"$gt": 1}}):
            a.append(i['_id'])
        bc = self.coll.find_one({'_id': 1})["bonus_cash"]
        bonus_cash = int(bc / len(a))
        self.coll.update_many({'deposit': {"$gt": 1}}, {"$inc": {"cash": bonus_cash}})
        e = disnake.Embed(description = f"**💰** `{triada_num(int(bc))}` **Cooper Coins были разделены среди всех участников с активным депозитом**", color = 0x00fc0b, timestamp = ctx.created_at)
        e.set_author(name = f"{ctx.guild.name} | Розигрыш бонусного счёта", icon_url = ctx.guild.icon)
        e.set_footer(text = f"Opium 🌴 Bot", icon_url = "https://images-ext-2.disnakeapp.net/external/pqiZeryT3Hca0OgN9xevXnYrrApiVErU_TRWGXrc7SI/%3Fsize%3D4096/https/cdn.disnakeapp.com/avatars/722921602026700861/654ff8c616269acc148f204c17670aaa.png?width=671&height=671")
        self.coll.update_one({"_id": 1}, {"$set": {"bonus_cash": 0}})
        await ctx.send(embed = e)


    # #OREL
    # @commands.slash_command(description = "Economy: Сыграть с другим пользователем в орел-решка как Орел")
    # async def orel(self, ctx, member: disnake.Member, cc: int):
    #     global content
    #     content = 'orel'
    #     global orauthor
    #     orauthor = ctx.author
    #     global ormember
    #     ormember = member
    #     global ccg
    #     ccg = cc
    #     aut_cash = self.coll.find_one({"_id": orauthor.id})["cash"]
    #     mem_cash = self.coll.find_one({"_id": ormember.id})["cash"]
    #     if ctx.author.id == member.id:
    #         await ctx.send(embed = disnake.Embed(description = f'**{ctx.author.mention}, вы не можете сыграть сам с собой!**', color = 0xff0000), ephemeral = True)
    #     elif aut_cash < cc:
    #         await ctx.send(embed = disnake.Embed(description = f'**{ctx.author.mention}, y вас недостаточно Cooper Coins!**', color = 0xff0000), ephemeral = True)
    #     elif mem_cash < cc:
    #         await ctx.send(embed = disnake.Embed(description = f'**У {member.mention} недостаточно Cooper Coins**', color = 0xff0000), ephemeral = True)
    #     elif cc <= 0:
    #         await ctx.send(embed = disnake.Embed(description = f'**{ctx.author.mention}, введены некорректные данные**', color = 0xff0000), ephemeral = True)
    #     else:
    #         emb = disnake.Embed(description = f'**{ctx.author.mention} предложил {member.mention} игру на {cc} cc\n\n{ctx.author.display_name} - <:verified:768155762425462784>\n{member.display_name} - <:unverified:768155761171234887>**', color = 0x425be0)
    #         emb.set_author(name = f'{ctx.guild.name} | Орёл - Решка', icon_url = ctx.guild.icon)
    #         emb.set_footer(text = f'(Орёл) {ctx.author.name} x {member.name} (Решка)')
    #         global ormsg
    #         await ctx.send(embed = emb)
    #         ormsg = await ctx.original_response()
    #         await ormsg.add_reaction('<:verified:768155762425462784>')
    #         await ormsg.add_reaction('<:unverified:768155761171234887>')

    # #RESHKA
    # @commands.slash_command(description = "Economy: Сыграть с другим пользователем в орел-решка как Решка")
    # async def reshka(self, ctx, member: disnake.Member, cc: int):
    #     global content
    #     content = 'reshka'
    #     global orauthor1
    #     orauthor1 = ctx.author
    #     global ormember1
    #     ormember1 = member
    #     global ccg1
    #     ccg1 = cc
    #     aut_cash = self.coll.find_one({"_id": orauthor1.id})["cash"]
    #     mem_cash = self.coll.find_one({"_id": ormember1.id})["cash"]
    #     if ctx.author.id == member.id:
    #         await ctx.send(embed = disnake.Embed(description = f'**{ctx.author.mention}, вы не можете сыграть сам с собой!**', color = 0xff0000), ephemeral = True)
    #     elif aut_cash < cc:
    #         await ctx.send(embed = disnake.Embed(description = f'**{ctx.author.mention}, y вас недостаточно Cooper Coins!**', color = 0xff0000), ephemeral = True)
    #     elif mem_cash < cc:
    #         await ctx.send(embed = disnake.Embed(description = f'**У {member.mention} недостаточно Cooper Coins**', color = 0xff0000), ephemeral = True)
    #     elif cc <= 0:
    #         await ctx.send(embed = disnake.Embed(description = f'**{ctx.author.mention}, введены некорректные данные**', color = 0xff0000), ephemeral = True)
    #     else:
    #         emb = disnake.Embed(description = f'**{ctx.author.mention} предложил {member.mention} игру на {cc} cc\n\n{ctx.author.display_name} - <:verified:768155762425462784>\n{member.display_name} - <:unverified:768155761171234887>**', color = 0x425be0)
    #         emb.set_author(name = f'{ctx.guild.name} | Орёл - Решка', icon_url = ctx.guild.icon)
    #         emb.set_footer(text = f'(Решка) {ctx.author.name} x {member.name} (Орёл)')
    #         global ormsg1
    #         await ctx.send(embed = emb)
    #         ormsg1 = await ctx.original_response()
    #         await ormsg1.add_reaction('<:verified:768155762425462784>')
    #         await ormsg1.add_reaction('<:unverified:768155761171234887>')


    # #ON RAW REACTION ADD
    # @commands.Cog.listener()
    # async def on_raw_reaction_add(self, payload):
    #     try:
    #         channel = self.client.get_channel(1053199351264059453)
    #         if payload.member.bot:
    #             return
    #         if content == 'orel':
    #             if payload.member.id == ormember.id:
    #                 if payload.message_id == ormsg.id:
    #                     if payload.emoji.id == 768155762425462784:
    #                         emb = disnake.Embed(description = f'**{orauthor.mention} предложил {ormember.mention} игру на {ccg} cc\n\n{orauthor.display_name} - <:verified:768155762425462784>\n{ormember.display_name} - <:verified:768155762425462784>**', color = 0x425be0)
    #                         emb.set_author(name = f'{payload.member.guild.name} | Орёл - Решка', icon_url = payload.member.guild.icon)
    #                         emb.set_footer(text = f'(Орёл) {orauthor.name} x {ormember.name} (Решка)')
    #                         await ormsg.edit(embed = emb)
    #                         await asyncio.sleep(1)
    #                         n = randint(0, 1)
    #                         if n == 0:
    #                             self.coll.update_one({"_id": orauthor.id}, {"$inc": {"cash": ccg}})
    #                             self.coll.update_one({"_id": ormember.id}, {"$inc": {"cash": -ccg}})
    #                             self.coll.update_one({"_id": 1}, {"$inc": {"cash": ccg}})
    #                             e1 = disnake.Embed(description = f'**Выпало: Орёл\nПобеда {orauthor.mention}, + {ccg} Cooper Coins**', color = 0x1b7fdf)
    #                             e1.set_author(name = f'{payload.member.guild.name} | Орёл - Решка', icon_url = payload.member.guild.icon)
    #                             e1.set_footer(text = f'(Орёл) {orauthor.name} x {ormember.name} (Решка)')
    #                             await channel.send(embed = e1)
    #                             await ormsg.delete()
    #                         elif n == 1:
    #                             self.coll.update_one({"_id": ormember.id}, {"$inc": {"cash": ccg}})
    #                             self.coll.update_one({"_id": orauthor.id}, {"$inc": {"cash": -ccg}})
    #                             self.coll.update_one({"_id": 1}, {"$inc": {"cash": ccg}})
    #                             e2 = disnake.Embed(description = f'**Выпало: Решка\nПобеда {ormember.mention}, + {ccg} Cooper Coins**', color = 0x1b7fdf)
    #                             e2.set_author(name = f'{payload.member.guild.name} | Орёл - Решка', icon_url = payload.member.guild.icon)
    #                             e2.set_footer(text = f'(Орёл) {orauthor.name} x {ormember.name} (Решка)')
    #                             await channel.send(embed = e2)
    #                             await ormsg.delete()
    #                         else:
    #                             return
    #             if (payload.member.id == ormember.id or payload.member.id == orauthor.id):
    #                 if payload.message_id == ormsg.id:
    #                     if payload.emoji.id == 768155761171234887:
    #                         await ormsg.delete()
    #         if content == 'reshka':
    #             if payload.member.id == ormember1.id:
    #                 if payload.message_id == ormsg1.id:
    #                     if payload.emoji.id == 768155762425462784:
    #                         emb = disnake.Embed(description = f'**{orauthor1.mention} предложил {ormember1.mention} игру на {ccg1} cc\n\n{orauthor1.display_name} - <:verified:768155762425462784>\n{ormember1.display_name} - <:verified:768155762425462784>**', color = 0x425be0)
    #                         emb.set_author(name = f'{payload.member.guild.name} | Орёл - Решка', icon_url = payload.member.guild.icon)
    #                         emb.set_footer(text = f'(Решка) {orauthor1.name} x {ormember1.name} (Орёл)')
    #                         await ormsg1.edit(embed = emb)
    #                         await asyncio.sleep(1)
    #                         n = randint(0, 1)
    #                         if n == 0:
    #                             self.coll.update_one({"_id": ormember1.id}, {"$inc": {"cash": ccg1}})
    #                             self.coll.update_one({"_id": orauthor1.id}, {"$inc": {"cash": -ccg1}})
    #                             self.coll.update_one({"_id": 1}, {"$inc": {"cash": ccg1}})
    #                             e1 = disnake.Embed(description = f'**Выпало: Орёл\nПобеда {ormember1.mention}, + {ccg1} Cooper Coins**', color = 0x1b7fdf)
    #                             e1.set_author(name = f'{payload.member.guild.name} | Орёл - Решка', icon_url = payload.member.guild.icon)
    #                             e1.set_footer(text = f'(Решка) {orauthor1.name} x {ormember1.name} (Орёл)')
    #                             await channel.send(embed = e1)
    #                             await ormsg1.delete()
    #                         elif n == 1:
    #                             self.coll.update_one({"_id": orauthor1.id}, {"$inc": {"cash": ccg1}})
    #                             self.coll.update_one({"_id": ormember1.id}, {"$inc": {"cash": -ccg1}})
    #                             self.coll.update_one({"_id": 1}, {"$inc": {"cash": ccg1}})
    #                             e2 = disnake.Embed(description = f'**Выпало: Решка\nПобеда {orauthor1.mention}, + {ccg1} Cooper Coins**', color = 0x1b7fdf)
    #                             e2.set_author(name = f'{payload.member.guild.name} | Орёл - Решка', icon_url = payload.member.guild.icon)
    #                             e2.set_footer(text = f'(Решка) {orauthor1.name} x {ormember1.name} (Орёл)')
    #                             await channel.send(embed = e2)
    #                             await ormsg1.delete()
    #                         else:
    #                             return
    #             if (payload.member.id == ormember1.id or payload.member.id == orauthor1.id):
    #                 if payload.message_id == ormsg1.id:
    #                     if payload.emoji.id == 768155761171234887:
    #                         await ormsg1.delete()
    #     except NameError:
    #         return

def setup(client):
    client.add_cog(EconomyNew(client))