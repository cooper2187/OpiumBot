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
        prefix = self.prx.find_one({"_id": message.guild.id})["prefix"]
        if message.author == self.client.user:
            return
        if message.content.startswith('$help$'):
            await message.delete()
            emb = discord.Embed(description = '**Список команд:** ' + '`{}commands`\n'.format(prefix) + '**Help: [Support Server](https://discord.gg/sWHrXQT)\nAdd Opium: [Invite Opium to your Server](https://discord.com/api/oauth2/authorize?client_id=722921602026700861&permissions=8&scope=bot)**')
            emb.set_author(name = f"Префикс на {message.guild.name} =  ' {prefix} '", icon_url = message.guild.icon_url)
            await message.author.send(embed = emb)
        if message.content.startswith('prefix'):
            await message.channel.send(f'**Prefix on {message.guild.name}: `{prefix}`**')

    #HELP
    @commands.command()
    async def help(self, ctx):
        prefix = self.prx.find_one({"_id": ctx.guild.id})["prefix"]
        await ctx.message.delete()
        emb = discord.Embed(description = '**Список команд:** ' + '`{}command`\n'.format(prefix) + '**Help: [Support Server](https://discord.gg/sWHrXQT)\nAdd Opium: [Invite Opium to your Server](https://discord.com/api/oauth2/authorize?client_id=722921602026700861&permissions=8&scope=bot)**')
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
