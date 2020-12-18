import discord
from discord.ext import commands
import os
import pymongo
from pymongo import MongoClient
import asyncio

class Mute(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cluster = MongoClient("mongodb+srv://andrewnobot:xuInmV8QmD9GRR5c@cluster0.28biu.mongodb.net/opiumdb?retryWrites=true&w=majority")
        self.cmute = self.cluster.opiumdb.mutecoll
        self.prx = self.cluster.opiumdb.prefixcoll
    

    #ON GUILD JOIN
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        mute = {
            "_id": guild.id,
            "name": guild.name,
            "role_id": 0
        }
        if self.cmute.count_documents({"_id": guild.id}) == 0:
            self.cmute.insert_one(mute)

    #ON GUILD ROLE DELETE
    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        rol = self.cmute.find_one({"_id": role.guild.id})["role_id"]
        if role.id == rol:
            self.cmute.update_one({"_id": role.guild.id}, {"$set": {"role_id": 0}})
        else:
            return      

    #MUTE
    @commands.command()
    @discord.ext.commands.has_permissions(view_audit_log = True)
    async def mute(self, ctx, member: discord.Member, time: int, *, reason):
        r_id = self.cmute.find_one({"_id": ctx.guild.id})["role_id"]
        if r_id == 0:
            perm = discord.Permissions(change_nickname = True, read_messages = True, view_channel = True, send_messages = False, send_tts_messages = True, embed_links = True, attach_files = True, read_message_history = True, mention_everyone = True, external_emojis = True, connect = True, speak = False, stream = True, use_voice_activation = True)
            mute_role = await ctx.guild.create_role(name = 'Muted', permissions = perm, colour = discord.Colour(0x9b0b55))
            self.cmute.update_one({"_id": ctx.guild.id}, {"$set": {"role_id": mute_role.id}})
            e = discord.Embed(timestamp = ctx.message.created_at, color = 0x4e6100, description = f'**👨🏽‍💻 Модератор _{ctx.author.mention}_  заглушил 🔇 пользователя\n\n      _{member.mention}_ на {time} мин. Причинa: {reason}**')
            e.set_author(name = f'{ctx.guild.name} | Muted 🔇', icon_url = ctx.guild.icon_url)
            e.set_footer(text = 'Opium 🌴 Bot')
            await ctx.send(embed = e)
            await member.add_roles(mute_role, reason = f'Muted by {ctx.message.author.display_name}')
            for channel in ctx.guild.channels:
                await channel.set_permissions(mute_role, send_messages=False, speak = False, add_reactions = False)
            await asyncio.sleep(time * 60)
            await member.remove_roles(mute_role, reason = f'Auto Unmute')
        else:
            role = self.cmute.find_one({"_id": ctx.guild.id})["role_id"]
            mute_role1 = discord.utils.get(ctx.guild.roles, id = role)
            e1 = discord.Embed(timestamp = ctx.message.created_at, color = 0x4e6100, description = f'**👨🏽‍💻 Модератор _{ctx.author.mention}_  заглушил 🔇 пользователя\n_{member.mention}_ на {time} мин. Причинa: {reason}**')
            e1.set_author(name = f'{ctx.guild.name} | Muted 🔇', icon_url = ctx.guild.icon_url)
            e1.set_footer(text = 'Opium 🌴 Bot')
            await ctx.send(embed = e1)
            await member.add_roles(mute_role1, reason = f'Muted by {ctx.message.author.display_name}')
            for channel in ctx.guild.channels:
                await channel.set_permissions(mute_role1, send_messages=False, speak = False, add_reactions = False)
            await asyncio.sleep(time * 60)
            await member.remove_roles(mute_role1, reason = f'Auto Unmute')

    #UNMUTE
    @commands.command()
    @discord.ext.commands.has_permissions(view_audit_log = True)
    async def unmute(self, ctx, member:discord.Member):
        role = self.cmute.find_one({"_id": ctx.guild.id})["role_id"]
        mute_role = discord.utils.get(ctx.guild.roles, id = role) 
        await member.add_roles(mute_role)
        emb = discord.Embed(color = 0x479114, timestamp = ctx.message.created_at, description = f"**👨🏽‍💻 Модератор _{ctx.author.mention}_  снял заглушку 🔈 с пользователя\n_{member.mention}_**")
        emb.set_author(name = f'{ctx.guild.name} | Unmuted 🔈', icon_url = ctx.guild.icon_url)
        emb.set_footer(text = 'Opium 🌴 Bot')
        await ctx.send(embed = emb)
        await member.remove_roles(mute_role, reason = f'Unmuted by {ctx.message.author.display_name}')

    #ERROR MUTE
    @mute.error
    @discord.ext.commands.has_permissions(view_audit_log = True)
    async def mute_error(self, ctx, error):
        prefix = self.prx.find_one({"_id": ctx.guild.id})["prefix"]
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            emb = discord.Embed(title = '🔰 Command: {}mute'.format(prefix), description = '🔹 **Описание:** Ограничение доступа к текстовым/голосовым чатам\n🔹 **Использование:** {}mute [@Упоминание] [Время(минуты)] [Причина]\n'.format(prefix) + '🔹 **Пример:** {}mute @coooper#2187 30 offtop'.format(prefix))
            await ctx.send(embed = emb)
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            emb = discord.Embed(title = '⛔️ Ошибка', color = 0xca1d1d, description = f'**{ctx.author.mention}, у вас недостаточно прав! 😓**')
            await ctx.send(embed = emb)

    #ERROR UNMUTE
    @unmute.error
    @discord.ext.commands.has_permissions(view_audit_log = True)
    async def unmute_error(self, ctx, error):
        prefix = self.prx.find_one({"_id": ctx.guild.id})["prefix"]
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            emb = discord.Embed(title = '🔰 Command: {}unmute'.format(prefix), description = '🔹 **Описание:** Снять ограничение к текстовым/голосовым чатам\n🔹 **Использование:** {}unmute [@Упоминание]\n'.format(prefix) + '🔹 **Пример:** {}unmute @coooper#2187'.format(prefix))
            await ctx.send(embed = emb)
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            emb = discord.Embed(title = '⛔️ Ошибка', color = 0xca1d1d, description = f'**{ctx.author.mention}, у вас недостаточно прав! 😓**')
            await ctx.send(embed = emb)

def setup(client):
    client.add_cog(Mute(client))