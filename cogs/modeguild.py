import disnake
from disnake.ext import commands
import os
import pymongo
from pymongo import MongoClient
from disnake import Activity, ActivityType
from main import sets

class ModeGuild(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cluster = MongoClient("mongodb+srv://andrewnobot:xuInmV8QmD9GRR5c@cluster0.28biu.mongodb.net/opiumdb?retryWrites=true&w=majority", connect = False)
        self.prx = self.cluster.opiumdb.prefixcoll


    #CLEAR CHAT
    @commands.slash_command(description = "Moderators: Очистить чат")
    @commands.default_member_permissions(view_audit_log = True)
    async def clear(self, ctx, amount : int = commands.Param(gt = 0, lt = 50)):
        await ctx.channel.purge(limit = amount)
        await ctx.send(f"Clear {amount} messages")
        await ctx.delete_original_response(delay = 2)

    #KICK
    @commands.slash_command(description = "Moderators: Выгнать участника")
    @commands.default_member_permissions(administrator = True)
    async def kick(self, ctx, member:disnake.Member, *,  reason):
        if member.id == 382522784841990144:
            e = disnake.Embed(title = '📛 Error', description = '**Вы не можете выгнать данного пользователя!**')
            await ctx.send(embed = e)
        else:	
            e = disnake.Embed(timestamp = ctx.created_at, color = 0x045f00, description = f'**👨🏽‍💻 Модератор _{ctx.author.mention}_  выгнал 🚫 пользователя\n_{member.mention}_. Причинa: {reason}**')
            e.set_author(name = f'{ctx.guild.name} | Kick User', icon_url = ctx.guild.icon)
            e.set_footer(text = 'Opium 🌴 Bot')
            await ctx.send(embed = e)
            await member.kick(reason = f'{reason} | Выгнал: {ctx.author.display_name}')


    #BAN
    @commands.slash_command(description = "Moderators: Забанить участника")
    @commands.default_member_permissions(administrator = True)
    async def ban(self, ctx, member:disnake.Member, *,  reason = None):
        if member.id == 382522784841990144:
            e = disnake.Embed(title = '📛 Error', description = '**Вы не можете забанить данного пользователя!**')
            await ctx.send(embed = e)
        else:
            e = disnake.Embed(timestamp = ctx.created_at, color = 0x045f00, description = f'**👨🏽‍💻 Модератор _{ctx.author.mention}_  забанил 🚫 пользователя\n_{member.mention}_. Причинa: {reason}**')
            e.set_author(name = f'{ctx.guild.name} | Ban User', icon_url = ctx.guild.icon)
            e.set_footer(text = 'Opium 🌴 Bot')
            await ctx.send(embed = e)
            await member.ban(reason = f'{reason} | Забанил: {ctx.author.display_name}')



    #ACCOUNT INFORMATION
    @commands.slash_command(description = "Информация о пользователе")
    async def info(self, ctx, *, member: disnake.Member = None):
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
        e = disnake.Embed(color = col, timestamp = ctx.created_at)
        e.set_author(name = f'Информация о пользователе', icon_url = member.avatar)
        e.add_field(name = 'Имя пользователя:', value = member)
        if member.nick is None:
            n = member.name
        else:
            n = member.nick
        e.add_field(name = 'Никнейм на сервере:', value = n, inline = False)
        e.add_field(name = 'Присоединился к серверу:', value = member.joined_at.strftime("%a, %d.%m.%Y в %H:%M"), inline = False)
        e.add_field(name = 'Аккаунт был создан:', value = member.created_at.strftime("%a, %d.%m.%Y в %H:%M"), inline = True)
        e.add_field(name = f'Роли [{len(rlist)}]:', value = rolelist, inline = False)
        e.set_thumbnail(url = member.avatar)
        e.set_footer(text = f'Account ID: {member.id}')
        await ctx.send(embed = e)

    #SET NICK
    @sets.sub_command(name = "nick", description = "Сменить никнейм пользователю")
    async def setnick(self, ctx, member: disnake.Member, *, nick: commands.String[1, 32]):
        emb = disnake.Embed(title = 'Смена ника', color = 0x46c046, timestamp = ctx.created_at) 
        emb.set_author(name = member, icon_url = member.avatar)
        emb.add_field(name = 'До: ', value = member.display_name, inline = False)
        emb.set_footer(text = 'Opium 🌴 Bot')
        await member.edit(nick = nick, reason = f'Changed by {ctx.author}')
        emb.add_field(name = 'После: ', value = member.display_name, inline = False)
        await ctx.send(embed = emb)


    #CHANGENICK
    @commands.slash_command(description = "Сменить ник на сервере")
    async def changenick(self, ctx, *, nick: commands.String[1, 32]):
        emb = disnake.Embed(title = 'Смена ника', color = 0x46c046, timestamp = ctx.created_at)
        emb.set_author(name = ctx.author, icon_url = ctx.author.avatar)
        emb.add_field(name = 'До: ', value = ctx.author.display_name, inline = False)
        emb.set_footer(text = 'Opium 🌴 Bot')
        await ctx.message.author.edit(nick = nick)
        emb.add_field(name = 'После: ', value = ctx.author.display_name, inline = False)
        await ctx.send(embed = emb)

    #SERVER INFO
    @commands.slash_command(description = "Информация о сервере")
    async def serverinfo(self, ctx):
        guild = ctx.guild
        emb = disnake.Embed(title = 'Информация о серевере', color = 0x0086d8, timestamp = ctx.created_at)
        emb.set_author(name =  f'{guild.name}', icon_url = guild.icon)
        emb.add_field(name = 'Сервер создан:', value = guild.created_at.strftime('%a, %#d %B %Y **•** %X MSK'), inline = False)
        emb.add_field(name = 'Владелец сервера:', value = f'{guild.owner.mention}', inline = False)
        emb.add_field(name = 'Server ID:', value = guild.id)
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
        emb.set_thumbnail(url = guild.icon)
        await ctx.send(embed = emb)


def setup(client):
    client.add_cog(ModeGuild(client))