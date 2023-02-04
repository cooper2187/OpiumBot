import disnake
from disnake.ext import commands
import os
import pymongo
from pymongo import MongoClient
import time
import datetime
from datetime import timezone, tzinfo, timedelta
from main import sets

class Logs(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cluster = MongoClient("mongodb+srv://andrewnobot:xuInmV8QmD9GRR5c@cluster0.28biu.mongodb.net/opiumdb?retryWrites=true&w=majority")
        self.coll = self.cluster.opiumdb.prefixcoll

    @sets.sub_command(name = "log-channel", description = 'Установить канал для логов')
    async def set_log_channel(self, ctx, textchannel: disnake.TextChannel):
        logchannel = textchannel.id
        self.coll.update_one({"_id": ctx.guild.id}, {"$set": {"logchannel": logchannel}})
        await ctx.send(f"**Канал для логов установлено: #{textchannel}**")

    @sets.sub_command(name = "welcome-channel", description = 'Установить приветственный канал')
    async def set_welcome_channel(self, ctx, textchannel: disnake.TextChannel):
        welcomechannel = textchannel.id
        self.coll.update_one({"_id": ctx.guild.id}, {"$set": {"welcomechannel": welcomechannel}})
        await ctx.send(f"**Приветственный канал установлено: {textchannel.mention}**")


    #ON MEMBER UPDATE
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        logchannel = self.coll.find_one({"_id": before.guild.id})["logchannel"]
        if logchannel is None:
            return
        else:
            try:
                logch = self.client.get_channel(logchannel)
                if before.display_name != after.display_name:
                    e = disnake.Embed(title = f'{before.guild.name} | Смена никнейма', color = 0x546c9b, description = f'**Пользователь: {before.mention}\n\nДо: `{before.display_name}`\n\nПосле: `{after.display_name}`**')
                    await logch.send(embed = e)
            except AttributeError:
                return
                    

    #ON MESSAGE EDIT
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        logchannel= self.coll.find_one({"_id": before.guild.id})["logchannel"]
        if logchannel is None:
            return
        else:
            try:
                logch = self.client.get_channel(logchannel)
                if before.channel == logch:
                    return
                elif before.embeds or after.embeds:
                    return
                else:
                    e = disnake.Embed(title = f'{before.guild.name} | Сообщение изменено ✉️ 🖊️', description = f'**{before.author.mention} отредактировал(а) своё сообщение\nв канале #{before.channel.name}. [Перейти к сообщению]({before.jump_url})**')
                    e.add_field(name = 'До:', value = before.content, inline = False)
                    e.add_field(name = 'После:', value = after.content, inline = False)
                    e.set_footer(text = f'Message ID: {before.id} •  Author ID: {before.author.id}', icon_url = before.author.avatar)
                    await logch.send(embed = e)
            except AttributeError:
                pass
            except disnake.errors.HTTPException:
                pass


    #ON MESSAGE DELETE
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        logchannel= self.coll.find_one({"_id": message.guild.id})["logchannel"]
        if logchannel is None:
            return
        else:
            try:
                logch = self.client.get_channel(logchannel)
                if message.channel == logch:
                    return
                elif message.author.bot:
                    return
                async for event in message.guild.audit_logs(limit = 1, action = disnake.AuditLogAction.message_delete):
                    if getattr(event.target, "id") == message.author.id:
                        e = disnake.Embed(description = f'**Отправитель: {message.author.mention}. Канал: {message.channel.mention}\nСообщение:** {message.content}')
                        e.set_author(name = f'{message.guild.name} | Сообщение удалено ✉️❌', icon_url = message.author.avatar)
                        e.set_footer(text = f'Message ID: {message.id} •  Delete by: {event.user.display_name}', icon_url = event.user.avatar)
                        await logch.send(embed = e)
                    else:
                        e = disnake.Embed(description = f'**Отправитель: {message.author.mention}. Канал: {message.channel.mention}\nСообщение:** {message.content}')
                        e.set_author(name = f'{message.guild.name} | Сообщение удалено ✉️❌', icon_url = message.author.avatar)
                        e.set_footer(text = f'Message ID: {message.id} •  Delete by: {message.author.display_name}', icon_url = message.author.avatar)
                        await logch.send(embed = e)
                else:
                    return
            except AttributeError:
                pass
            
    #ON MEMBER JOIN
    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcomechannel= self.coll.find_one({"_id": member.guild.id})["welcomechannel"]
        if welcomechannel is None:
            return
        else:
            try:
                logch = self.client.get_channel(welcomechannel)
                emb = disnake.Embed(title = '☑️⠀Новый пользователь', color = 0x951fad, description = f'\n\n**{member}** присоединился(-ась) к серверу!')
                emb.set_thumbnail(url = member.avatar)
                emb.set_footer(text = f'Всего пользователей: {member.guild.member_count}')
                await logch.send(embed = emb)
            except AttributeError:
                pass

    #ON MEMBER REMOVE
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        welcomechannel= self.coll.find_one({"_id": member.guild.id})["welcomechannel"]
        if welcomechannel is None:
            return
        else:
            try:
                logch = self.client.get_channel(welcomechannel)
                emb = disnake.Embed(title = '❌⠀До скорой встречи', color = 0x951fad, description = f'\n\n**{member}** покинул(-а) сервер!')
                emb.set_thumbnail(url = member.avatar)
                emb.set_footer(text = f'Пользователей осталось: {member.guild.member_count}')
                await logch.send(embed = emb)
            except AttributeError:
                pass
def setup(client):
    client.add_cog(Logs(client))