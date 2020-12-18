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

    #SET MODERATOR
    @commands.command()
    @commands.has_role( 743183085331415110 )
    async def setmoderator(self, ctx, member: discord.Member, amount: int):
        await ctx.message.delete()
        role4 = discord.utils.get(ctx.guild.roles, id = 739527889514528819)
        role5 = discord.utils.get(ctx.guild.roles, id = 739527888096722955)
        role6 = discord.utils.get(ctx.guild.roles, id = 739527768790007851)
        role7 = discord.utils.get(ctx.guild.roles, id = 740658081037418577)
        crole = discord.utils.get(ctx.guild.roles, id = 749334354085543936)
        crole1 = discord.utils.get(ctx.guild.roles, id = 749634295945101422)
        if amount == 1:
            role1 = discord.utils.get(ctx.guild.roles, id = 739527889514528819)
            await member.remove_roles(role4)
            await member.remove_roles(role5)
            await member.remove_roles(role6)
            await member.remove_roles(role7)
            await member.remove_roles(crole)
            await member.remove_roles(crole1)
            await member.add_roles(role1)
            await member.add_roles(crole)
            e = discord.Embed(color = 0x82d89a, description = f'**Главный модератор {ctx.author.mention} назначил {member.mention} Модератором 1 уровня**',timestamp = ctx.message.created_at)
            e.set_author(name = f'{ctx.guild.name} | Назначение модератора', icon_url = ctx.guild.icon_url)
            e.set_footer(text = 'Moderators Team')
            await ctx.send(embed = e)
        if amount == 2:
            role2 = discord.utils.get(ctx.guild.roles, id = 739527888096722955)
            await member.remove_roles(role4)
            await member.remove_roles(role5)
            await member.remove_roles(role6)
            await member.remove_roles(role7)
            await member.remove_roles(crole)
            await member.remove_roles(crole1)
            await member.add_roles(role2)
            await member.add_roles(crole)
            e = discord.Embed(color = 0x1a7233, description = f'**Главный модератор {ctx.author.mention} назначил {member.mention} Модератором 2 уровня**',timestamp = ctx.message.created_at)
            e.set_author(name = f'{ctx.guild.name} | Назначение модератора', icon_url = ctx.guild.icon_url)
            e.set_footer(text = 'Moderators Team')
            await ctx.send(embed = e)
        if amount == 3:
            role3 = discord.utils.get(ctx.guild.roles, id = 739527768790007851)
            await member.remove_roles(role4)
            await member.remove_roles(role5)
            await member.remove_roles(role6)
            await member.remove_roles(role7)
            await member.remove_roles(crole)
            await member.remove_roles(crole1)
            await member.add_roles(role3)
            await member.add_roles(crole)
            e = discord.Embed(color = 0x0aa2a2, description = f'**Главный модератор {ctx.author.mention} назначил {member.mention} Модератором 3 уровня**',timestamp = ctx.message.created_at)
            e.set_author(name = f'{ctx.guild.name} | Назначение модератора', icon_url = ctx.guild.icon_url)
            e.set_footer(text = 'Moderators Team')
            await ctx.send(embed = e)
        if amount == 4:
            role4 = discord.utils.get(ctx.guild.roles, id = 740658081037418577)
            await member.remove_roles(role4)
            await member.remove_roles(role5)
            await member.remove_roles(role6)
            await member.remove_roles(role7)
            await member.remove_roles(crole)
            await member.remove_roles(crole1)
            await member.add_roles(role4)
            await member.add_roles(crole1)
            e = discord.Embed(color = 0x0aa2a2, description = f'**Главный модератор {ctx.author.mention} назначил {member.mention} Старшим Модератором**',timestamp = ctx.message.created_at)
            e.set_author(name = f'{ctx.guild.name} | Назначение модератора', icon_url = ctx.guild.icon_url)
            e.set_footer(text = 'Moderators Team')
            await ctx.send(embed = e)	
        if amount == 0:
            await member.remove_roles(role4)
            await member.remove_roles(role5)
            await member.remove_roles(role6)
            await member.remove_roles(role7)
            await member.remove_roles(crole)
            await member.remove_roles(crole1)
            e = discord.Embed(color = 0xff0000, description = f'**Главный модератор {ctx.author.mention} снял {member.mention} с поста Модератора**',timestamp = ctx.message.created_at)
            e.set_author(name = f'{ctx.guild.name} | Снятие модератора', icon_url = ctx.guild.icon_url)
            e.set_footer(text = 'Moderators Team')
            await ctx.send(embed = e)
            

    @setmoderator.error
    async def setmoderator_error(self, ctx, error):
        prefix = self.prx.find_one({"_id": ctx.guild.id})["prefix"]
        if isinstance( error, discord.ext.commands.errors.MissingRequiredArgument ):
            emb = discord.Embed( title = '🔰 Command: {}setmoderator'.format(prefix), description = '🔹 **Описание:** Назначение модератора\n🔹 **Использование:** {}setmoderator [@Упоминание] [Уровень(0-4)]\n'.format(prefix) + '🔹 **Пример:** {}setmoderator @coooper#0001 2'.format(prefix) )
            await ctx.send(embed = emb)
        if isinstance( error, discord.ext.commands.errors.MissingRole ):
            emb = discord.Embed(title = '⛔️ Ошибка', color = 0xca1d1d, description = f'{ctx.author.mention}, у вас недостаточно прав! 😓')
            await ctx.send(embed = emb)

def setup(client):
    client.add_cog(Mods(client))