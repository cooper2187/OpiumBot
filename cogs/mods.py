import discord
from discord.ext import commands
import os
import pymongo
from pymongo import MongoClient
from discord import Activity, ActivityType

class Mods(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cluster = MongoClient("mongodb+srv://andrewnobot:xuInmV8QmD9GRR5c@cluster0.28biu.mongodb.net/opiumdb?retryWrites=true&w=majority", connect = False)
        self.prx = self.cluster.opiumdb.prefixcoll


    #CLEAR CHAT
    @commands.command()
    @commands.has_permissions(view_audit_log = True)
    async def clear(self, ctx, amount : int):
        await ctx.message.delete()
        if amount <= 50:
            await ctx.message.channel.purge(limit = amount)
        else:
            emb = discord.Embed(title = '⛔️ Ошибка', color = 0xca1d1d, description = f'**{ctx.author.mention}, не более 50 сообщений❗**')
            await ctx.send(embed = emb)

    #ERROR CLEAR
    @clear.error
    @commands.has_permissions(view_audit_log = True)
    async def clear_error(self, ctx, error):
        prefix = self.prx.find_one({"_id": ctx.guild.id})["prefix"]
        if isinstance( error, discord.ext.commands.errors.MissingRequiredArgument ):
            emb = discord.Embed( title = '🔰 Command: {}clear'.format(prefix), description = '🔹 **Описание:** Очистка чата\n**🔹 Использование:** {}clear [1-50]\n'.format(prefix) + '🔹 **Пример:** {}clear 15'.format(prefix))
            await ctx.send(embed = emb)
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            emb = discord.Embed(title = '⛔️ Ошибка', color = 0xca1d1d, description = f'**{ctx.author.mention}, у вас недостаточно прав! 😓**')
            await ctx.send(embed = emb)

    #KICK
    @commands.command()
    @commands.has_permissions(view_audit_log = True)
    async def kick(self, ctx, member:discord.Member, *,  reason):
        if member.id == 382522784841990144:
            e = discord.Embed(title = '📛 Error', description = '**Вы не можете выгнать данного пользователя!**')
            await ctx.send(embed = e)
        else:	
            e = discord.Embed(timestamp = ctx.message.created_at, color = 0x045f00, description = f'**👨🏽‍💻 Модератор _{ctx.author.mention}_  выгнал 🚫 пользователя\n_{member.mention}_. Причинa: {reason}**')
            e.set_author(name = f'{ctx.guild.name} | Kick User', icon_url = ctx.guild.icon_url)
            e.set_footer(text = 'Opium 🌴 Bot')
            await ctx.send(embed = e)
            await member.kick(reason = f'{reason} | Выгнал: {ctx.author.display_name}')


    #ERROR KICK
    @kick.error
    @commands.has_permissions(view_audit_log = True)
    async def kick_error(self, ctx, error):
        prefix = self.prx.find_one({"_id": ctx.guild.id})["prefix"]
        if isinstance( error, discord.ext.commands.errors.MissingRequiredArgument ):
            emb = discord.Embed( title = '🔰 Command: {}kick'.format(prefix), description = '🔹 **Описание:** Выгнать участника с сервера\n🔹 **Использование:** {}kick [@Упоминание] [Причина]\n'.format(prefix) + '🔹 **Пример:** {}kick @coooper#2187 Массовый флуд'.format(prefix) )
            await ctx.send(embed = emb)
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            emb = discord.Embed(title = '⛔️ Ошибка', color = 0xca1d1d, description = f'{ctx.author.mention}, у вас недостаточно прав! 😓')
            await ctx.send(embed = emb)


    #BAN
    @commands.command()
    @commands.has_permissions(view_audit_log = True)
    async def ban(self, ctx, member:discord.Member, *,  reason = None):
        if member.id == 382522784841990144:
            e = discord.Embed(title = '📛 Error', description = '**Вы не можете забанить данного пользователя!**')
            await ctx.send(embed = e)
        else:
            e = discord.Embed(timestamp = ctx.message.created_at, color = 0x045f00, description = f'**👨🏽‍💻 Модератор _{ctx.author.mention}_  забанил 🚫 пользователя\n_{member.mention}_. Причинa: {reason}**')
            e.set_author(name = f'{ctx.guild.name} | Ban User', icon_url = ctx.guild.icon_url)
            e.set_footer(text = 'Opium 🌴 Bot')
            await ctx.send(embed = e)
            await member.ban(reason = f'{reason} | Забанил: {ctx.author.display_name}')


    #ERROR BAN
    @ban.error
    @commands.has_permissions(view_audit_log = True)
    async def ban_error(self, ctx, error):
        prefix = self.prx.find_one({"_id": ctx.guild.id})["prefix"]
        if isinstance( error, discord.ext.commands.errors.MissingRequiredArgument ):
            emb = discord.Embed( title = '🔰 Command: {}ban'.format(prefix), description = '🔹 **Описание:** Забанить участника\n🔹 **Использование:** {}ban [@Упоминание] [Причина]\n'.format(prefix) + '🔹 **Пример:** {}ban @coooper#2187 Неадекват'.format(prefix) )
            await ctx.send(embed = emb)
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            emb = discord.Embed(title = '⛔️ Ошибка', color = 0xca1d1d, description = f'{ctx.author.mention}, у вас недостаточно прав! 😓')
            await ctx.send(embed = emb)


    #ACCOUNT INFORMATION
    @commands.command()
    async def info(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author
        else:
            member = member
        rlist = []
        roles = []
        for r in member.roles:
            if r.name == '@everyone':
                continue
            roles.append(r)
            rlist.append(r.mention)
        if len(roles) > 0:
            rolelist = ', '.join(rlist)
            col = roles[len(roles) - 1].color
            i = 2
            while col.value == 000000:
                if i > len(roles):
                    col = 0x6bff00
                    break
                col = roles[len(roles) - i].color
                i += 1
        else:
            rolelist = 'None'
            col = 0x6bff00
        e = discord.Embed(color = col, timestamp = ctx.message.created_at)
        e.set_author(name = f'Информация о пользователе', icon_url = member.avatar_url)
        e.add_field(name = 'Имя пользователя:', value = member)
        e.add_field(name = 'Никнейм на сервере:', value = member.display_name, inline = False)
        e.add_field(name = 'Присоединился к серверу:', value = member.joined_at.strftime("%a, %d.%m.%Y в %H:%M"), inline = False)
        e.add_field(name = 'Аккаунт был создан:', value = member.created_at.strftime("%a, %d.%m.%Y в %H:%M"), inline = True)
        e.add_field(name = f'Роли [{len(rlist)}]:', value = rolelist, inline = False)
        e.set_thumbnail(url = member.avatar_url)
        e.set_footer(text = f'Account ID: {member.id}')
        await ctx.send(embed = e)

    #SET NICK
    @commands.command()
    @discord.ext.commands.has_permissions(view_audit_log = True)
    async def setnick(self, ctx, member: discord.Member, *, nick):
        emb = discord.Embed(title = 'Смена ника', color = 0x46c046, timestamp = ctx.message.created_at) 
        emb.set_author(name = member, icon_url = member.avatar_url)
        emb.add_field(name = 'До: ', value = member.display_name, inline = False)
        emb.set_footer(text = 'Opium 🌴 Bot')
        await member.edit(nick = nick, reason = f'Changed by {ctx.message.author}')
        emb.add_field(name = 'После: ', value = member.display_name, inline = False)
        await ctx.send(embed = emb)


    #ERROR SET NICK
    @setnick.error
    @discord.ext.commands.has_permissions(view_audit_log = True)
    async def setnick_error(self, ctx, error):
        prefix = self.prx.find_one({"_id": ctx.guild.id})["prefix"]
        if isinstance( error, discord.ext.commands.errors.MissingRequiredArgument ):
            emb = discord.Embed( title = '🔰 Command: {}setnick'.format(prefix), description = '🔹 **Описание:** Смена никйнейма пользователю\n🔹 **Использование:** {}setnick [@Упоминание] [Nick Name]\n'.format(prefix) + '🔹 **Пример:** {}setnick @coooper#2187 Anthony Cooper'.format(prefix) )
            await ctx.send(embed = emb)
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            emb = discord.Embed(title = '⛔️ Ошибка', color = 0xca1d1d, description = f'{ctx.author.mention}, у вас недостаточно прав! 😓')
            await ctx.send(embed = emb)


    #CHANGENICK
    @commands.command()
    async def changenick(self, ctx, *, nick):
        emb = discord.Embed(title = 'Смена ника', color = 0x46c046, timestamp = ctx.message.created_at)
        emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        emb.add_field(name = 'До: ', value = ctx.author.display_name, inline = False)
        emb.set_footer(text = 'Opium 🌴 Bot')
        await ctx.message.author.edit(nick = nick)
        emb.add_field(name = 'После: ', value = ctx.author.display_name, inline = False)
        await ctx.send(embed = emb)

    @changenick.error
    async def changenick_error(self, ctx, error):
        if isinstance( error, discord.ext.commands.errors.MissingRequiredArgument ):
            guild = ctx.message.guild
            emb = discord.Embed(description = f'{ctx.author.mention}**, Ваш никнейм на сервере был сброшен. ✔️**', timestamp = ctx.message.created_at)
            emb.set_author(name = f'{guild.name} | ✏️ Смена ника', icon_url = guild.icon_url)
            await ctx.message.author.edit(nick = None)
            await ctx.send(embed = emb)
        if isinstance( error, discord.ext.commands.errors.CommandInvokeError ):
            emb = discord.Embed( title = '⛔️ Ошибка', description = f'{ctx.author.mention}, Ник должен содержать не более 32 символов! 🤯', color = 0xca1d1d)
            await ctx.send(embed = emb)

    #SERVER INFO
    @commands.command()
    async def serverinfo(self, ctx):
        guild = ctx.message.guild
        emb = discord.Embed(title = 'Информация о серевере', color = 0x0086d8, timestamp = ctx.message.created_at)
        emb.set_author(name =  f'{guild.name}', icon_url = guild.icon_url)
        emb.add_field(name = 'Сервер создан:', value = guild.created_at.strftime('%a, %#d %B %Y **•** %X MSK'), inline = False)
        emb.add_field(name = 'Владелец сервера:', value = f'{guild.owner.mention}', inline = False)
        emb.add_field(name = 'Server ID:', value = guild.id, inline = False)
        emb.add_field(name = 'Регион:', value = guild.region)
        emb.add_field(name = 'Пользователи:', value = guild.member_count)
        emb.add_field(name = 'Роли:', value = f'{len(guild.roles)}')
        emb.add_field(name = 'Категории:', value = f'{len(guild.categories)}')
        emb.add_field(name = 'Голосовые каналы:', value = f'{len(guild.voice_channels)}')
        emb.add_field(name = 'Текстовые каналы:', value = f'{len(guild.text_channels)}')
        roless = []
        for role in ctx.guild.roles:
            roless.append(role.name)
        rols = len(roless)
        if rols <= 25:
            emb.add_field(name = f'Список ролей', value = ', '.join(roless))
        else:
            pass
        emb.set_thumbnail(url = guild.icon_url)
        await ctx.send(embed = emb)


def setup(client):
    client.add_cog(Mods(client))
