import discord
from discord.ext import commands
import os
import asyncio
import pymongo
from pymongo import MongoClient

class Aid(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cluster = MongoClient("mongodb+srv://andrewnobot:xuInmV8QmD9GRR5c@cluster0.28biu.mongodb.net/opiumdb?retryWrites=true&w=majority", connect = False)
        self.prx = self.cluster.opiumdb.prefixcoll

    #ON MESSAGE
    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            prefix = self.prx.find_one({"_id": message.guild.id})["prefix"]
            if message.author == self.client.user:
                return
            if message.content.lower().startswith('$help$'):
                await message.delete()
                emb = discord.Embed(description = '**Список команд:** ' + '`{}commands`\n'.format(prefix) + '**Help: [Support Server](https://discord.gg/sWHrXQT)\nAdd Opium: [Invite Opium to your Server](https://discord.com/api/oauth2/authorize?client_id=722921602026700861&permissions=8&scope=bot)**')
                emb.set_author(name = f"Префикс на {message.guild.name} =  ' {prefix} '", icon_url = message.guild.icon_url)
                await message.author.send(embed = emb)
            if message.content.startswith('prefix'):
                await message.channel.send(f'**Prefix on {message.guild.name}: `{prefix}`**')
        except AttributeError:
            pass
                
    #HELP
    @commands.command()
    async def helpp(self, ctx, name = None):
        prefix = self.prx.find_one({"_id": ctx.guild.id})["prefix"]
        if name is None:
            await ctx.message.delete()
            emb = discord.Embed(description = '**Список команд:** ' + '`{}commands`\n'.format(prefix) + '**Help: [Support Server](https://discord.gg/sWHrXQT)\nAdd Opium: [Invite Opium to your Server](https://discord.com/api/oauth2/authorize?client_id=722921602026700861&permissions=8&scope=bot)**')
            emb.set_author(name = f"Префикс на {ctx.guild.name} =  ' {prefix} '", icon_url = ctx.guild.icon_url)
            await ctx.author.send(embed = emb)
        elif (name == 'spin' or name == 'спин' or name == 'ызшт' or name == 'спін'):
            await ctx.send(embed = discord.Embed(title = f'Команда: {prefix}spin', description = '**Псевдонимы**: {}спин, {}спін, {}ызшт\n**Описание**: Крутить рулетку\n**Перезарядка**: 60 минут\n**Использование**:\n{}spin\n{}спін\n{}спин\n{}ызшт'.format(prefix, prefix, prefix, prefix, prefix, prefix, prefix), color = discord.Colour.dark_gray()))
        elif (name == 'true' or name == 'try'):
            await ctx.send(embed = discord.Embed(title = f'Команда: {prefix}true', description = '**Псевдонимы**: {}try\n**Описание**: Удвоить сумму. Шанс 50%\n**Перезарядка**: 1 секунда\n**Использование**:\n{}true [сумма]\n{}try [сумма]\n**Пример**:\n{}true 15\n{}try 25'.format(prefix, prefix, prefix, prefix, prefix), color = discord.Colour.dark_gray()))
        elif name == 'balance':
            await ctx.send(embed = discord.Embed(title = f'Команда: {prefix}balance', description = '**Описание**: Посмотреть баланс\n**Использование**:\n{}balance\n{}balance [пользователь]\n**Пример**:\n{}balance\n{}balance cooooper'.format(prefix, prefix, prefix, prefix), color = discord.Colour.dark_gray()))
        elif name == 'stats':
            await ctx.send(embed = discord.Embed(title = f'Команда: {prefix}stats', description = '**Описание**: Статистика пользователя\n**Перезарядка**: 3 секунды\n**Использование**:\n{}stats\n{}stats [пользователь]\n**Пример**:\n{}stats\n{}stats cooooper'.format(prefix, prefix, prefix, prefix), color = discord.Colour.dark_gray()))
        elif name == 'pay':
            await ctx.send(embed = discord.Embed(title = f'Команда: {prefix}pay', description = '**Описание**: Передать Cooper Coins\n**Перезарядка**: 10 секунд\n**Использование**: {}pay [пользователь] [сумма]\n**Пример**: {}pay cooooper 200'.format(prefix, prefix), color = discord.Colour.dark_gray()))
        elif name == 'spin_up':
            await ctx.send(embed = discord.Embed(title = f'Команда: {prefix}spin_up', description = '**Описание**: Рулетка повышение макс. выигрыша\n**Перезарядка**: 1 секунда\n**Использование**:\n{}spin_up\n{}spin_up [кол-во раз]\n**Пример**:\n{}spin_up\n{}spin_up 4'.format(prefix, prefix, prefix, prefix), color = discord.Colour.dark_gray()))
        elif name == 'daily_spin_up':
            await ctx.send(embed = discord.Embed(title = f'Команда: {prefix}daily_spin_up', description = '**Описание**: Ежедневная рулетка повышение макс. выигрыша\n**Перезарядка**: 1 секунда\n**Использование**:\n{}daily_spin_up\n{}daily_spin_up [кол-во раз]\n**Пример**:\n{}daily_spin_up\n{}daily_spin_up 6'.format(prefix, prefix, prefix, prefix), color = discord.Colour.dark_gray()))
        elif name == 'daily_spin':
            await ctx.send(embed = discord.Embed(title = f'Команда: {prefix}daily_spin', description = '**Описание**: Крутить ежедневную рулетку\n**Попытки**: 1 раз в сутки\n**Использование**: {}daily_spin'.format(prefix), color = discord.Colour.dark_gray()))
        elif name == 'top':
            await ctx.send(embed = discord.Embed(title = f'Команда: {prefix}top', description = f'**Описание:** Список лидеров по Уровню/Баналансу\n**Перезарядка:** 5 секунд\n**Использование:**\n{prefix}top lvl - Leaderboard (Lvl)\n{prefix}top cc - Leaderboard (Balance)\n**Пример:**\n{prefix}top lvl\n{prefix}top cc', color = discord.Colour.dark_gray()))
        elif name == 'up_info':
            await ctx.send(embed = discord.Embed(title = f'Команда: {prefix}up_info', description = '**Описание**: Информация о прокачке навыков\n**Использование**: {}up_info'.format(prefix), color = discord.Colour.dark_gray()))
        elif name == 'set':
            await ctx.send(embed = discord.Embed(title = f'Command: {prefix}set', description = '**Описание:**\n{}set balance - Установить баланс\n{}set lvl - Установить уровень\n{}set xp - Установить опыт\n{}set daily - Установить статус ежедневной рулетки(1 или 2)\n{}set sbonus - Установить макс. выигрыш(spin)\n{}set dsbonus - Установить макс. выигрыш(daily_spin)\n{}set spot - Установить процент Jackpot\n{}set sprice - Установить цену на повышение макс. выигрыша(spin)\n{}set dsprice - Установить цену на повышение макс. выигрыша(daily_spin)\n{}set loan - Установить кредит\n{}set deposit - Установить депозит\n**Использование:**\n{}set balance [user] [amount]\n{}set lvl [user] [lvl]\n{}set xp [user] [xp]\n{}set daily [user] [value(1 or 2)]\n{}set sbonus [user] [amount]\n{}set dsbonus [user] [amount]\n{}set spot [user] [value(1-15)]\n{}set sprice [user] [amount]\n{}set dsprice [user] [amount]\n{}set loan [user] [amount]\n{}set deposit [user] [amount]\n**Пример:**\n{}set balance @cooooper#5265 3000\n{}set lvl @cooooper#5265 13\n{}set xp @cooooper#5265 226\n{}set daily @cooooper#5265 2\n{}set sbonus @cooooper#5265 332\n{}set dsbonus @cooooper#5265 165\n{}set spot @cooooper#5265 12\n{}set sprice @cooooper#5265 165\n{}set dsprice @cooooper#5265 95\n{}set loan @хэллоу#9006 5000\n{}set deposit @cooper#5265 1200'.format(prefix, prefix, prefix, prefix, prefix, prefix, prefix, prefix, prefix, prefix, prefix, prefix, prefix, prefix, prefix, prefix, prefix, prefix, prefix, prefix, prefix, prefix, prefix, prefix, prefix, prefix, prefix, prefix, prefix, prefix, prefix, prefix, prefix), color = discord.Colour.dark_gray()))
        elif name == 'give':
            await ctx.send(embed = discord.Embed(title = f'Команда: {prefix}give', description = '**Описание**: Начислить Cooper Coins пользователю\n**Перезарядка**: 60 секунд\n**Использование**: {}give [пользователь] [сумма] [причина(необязательно)]\n**Пример**:\n{}give cooooper 150\n{}give cooooper 150 Компенсация'.format(prefix, prefix, prefix), color = discord.Colour.dark_gray()))
        elif name == 'bank':
            await ctx.send(embed = discord.Embed(title = f'Команда: {prefix}bank', description = '**Описание**: Состояние Genesis счёта\n**Перезарядка**: 3 секунды\n**Использование**: {}bank'.format(prefix), color = discord.Colour.dark_gray()))
        elif name == 'credit':
            await ctx.send(embed = discord.Embed(title = f'Команда: {prefix}credit', description = '**Описание**: Выдать кредит пользователю\n**Перезарядка**: 30 секунд\n**Использование**: {}credit [пользователь] [сумма]\n**Пример**: {}credit cooooper 10000'.format(prefix, prefix), color = discord.Colour.dark_gray()))
        elif name == 'mycredit':
            await ctx.send(embed = discord.Embed(title = f'Команда: {prefix}mycredit', description = '**Описание**: Информация о кредите\n**Перезарядка**: 3 секунды\n**Использование**: {}mycredit'.format(prefix), color = discord.Colour.dark_gray()))
        elif name == 'return_credit':
            await ctx.send(embed = discord.Embed(title = f'Команда: {prefix}return_credit', description = '**Описание**: Вернуть кредит\n**Перезарядка**: 3 секунды\n**Использование**: {}return_credit [сумма]\n**Пример**: {}retunr_credit 15000'.format(prefix, prefix), color = discord.Colour.dark_gray()))
        elif (name == 'mydeposit' or name == 'мойдепозит' or name == 'депозит' or name == 'депозитинфо' or name == 'md'):
            await ctx.send(embed = discord.Embed(title = f'Команда: {prefix}mydeposit', description = '**Псевдонимы**: {}мойдепозит, {}депозит, {}депозитинфо, {}md\n**Описание**: Информаия о вашем депозите\n**Перезарядка**: 3 секунды\n**Использование**:\n{}mydeposit\n{}мойдепозит\n{}депозит\n{}депозитинфо\n{}md'.format(prefix, prefix, prefix, prefix, prefix, prefix, prefix, prefix, prefix), color = discord.Colour.dark_gray()))
        elif (name == 'put_on_deposit' or name == 'положитьнадепозит' or name == 'pod'):
            await ctx.send(embed = discord.Embed(title = f'Команда: {prefix}put_on_deposit', description = '**Псевдонимы**: {}положитьнадепозит, {}pod\n**Описание**: Положить Cooper Coins на депозит(0.05% в час)\n**Перезарядка**: 3 секунды\n**Использование**:\n{}put_on_deposit [сумма]\n{}положитьнадепозит [сумма]\n{}pod [сумма]\n**Пример**:\n{}put_on_deposit 900\n{}положитьнадепозит 350\n{}pod 865'.format(prefix, prefix, prefix, prefix, prefix, prefix, prefix, prefix), color = discord.Colour.dark_gray()))
        elif (name == 'take_from_deposit' or name == 'снятьдепозит' or name == 'take_deposit' or name == 'tfd'):
            pass
        else:
            await ctx.message.delete()
            emb = discord.Embed(description = '**Список команд:** ' + '`{}commands`\n'.format(prefix) + '**Help: [Support Server](https://discord.gg/sWHrXQT)\nAdd Opium: [Invite Opium to your Server](https://discord.com/api/oauth2/authorize?client_id=722921602026700861&permissions=8&scope=bot)**')
            emb.set_author(name = f"Префикс на {ctx.guild.name} =  ' {prefix} '", icon_url = ctx.guild.icon_url)
            await ctx.author.send(embed = emb)  

    #COMMAND
    @commands.command(aliases = ["commands"])
    async def __commands(self, ctx):
        prefix = self.prx.find_one({"_id": ctx.guild.id})["prefix"]
        emb = discord.Embed ( title = '🌴 Команды Opium 🌴', color = 0x17a891, description = '🔰 **Пользовательские команды:**\n\n🔹 **{}info - **'.format(prefix) + 'Информация  о пользователе\n🔹 **{}serverinfo - **'.format(prefix) + 'Информация о сервере\n🔹 **{}changenick - **'.format(prefix) + 'Смена ника на сервере\n🔹 **{}time - **'.format(prefix) + 'Дата и время (MSK)\n🔹 **{}privat - **'.format(prefix) + 'Создание приватной голосовой комнаты на две персоны\n\n🔰 **Для модераторов:**\n\n🔹 **{}clear - **'.format(prefix) + 'Очистка чата\n🔹 **{}setnick - **'.format(prefix) + 'Сменить ник пользователю\n🔹 **{}mute - **'.format(prefix) + 'Ограничить доступ к текстовым и голосовым чатам\n🔹 **{}unmute - **'.format(prefix) + 'Снять ограничение к текстовым и голосовым чатам\n🔹 **{}kick - **'.format(prefix) + 'Выгнать участника с сервера\n🔹 **{}ban - **'.format(prefix) + 'Забанить участника\n🔹 **{}setmoderator - **'.format(prefix) + 'Назначить пользователя модератором')
        await ctx.message.delete()
        await ctx.author.send(embed = emb)



def setup(client):
    client.add_cog(Aid(client))
