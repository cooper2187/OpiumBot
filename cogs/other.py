import discord
from discord.ext import commands
import os
import asyncio
import pymongo
from pymongo import MongoClient
from random import randint

class Other(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cluster = MongoClient("mongodb+srv://andrewnobot:xuInmV8QmD9GRR5c@cluster0.28biu.mongodb.net/opiumdb?retryWrites=true&w=majority", connect = False)
        self.prx = self.cluster.opiumdb.prefixcoll

    #ROLE ADD\REMOVE
    @commands.command()
    async def role(self, ctx, member: discord.Member, *, rolename: str):
        try:
            if rolename.startswith('-'):
                role = discord.utils.get(ctx.guild.roles, name = rolename[1:])
                if not role in ctx.guild.roles:
                    await ctx.send(embed = discord.Embed(description = '**<:opiumError:787690178730524672> Роль не найдена**', color = 0xff2020))
                elif role in member.roles:
                    await member.remove_roles(role)
                    await ctx.send(embed = discord.Embed(description = f'**<:opiumSuccess:787692787851067432> Смена ролей для {member.mention}, {rolename}**', color = 0x00ff5f))
                else:
                    await ctx.send(embed = discord.Embed(description = f'**<:opiumInfo:787694319292645426> У пользователя {member.mention} нету данной роли**', color = 0x009eff))
            elif rolename.startswith('+'):
                role = discord.utils.get(ctx.guild.roles, name = rolename[1:])
                if not role in ctx.guild.roles:
                    await ctx.send(embed = discord.Embed(description = '**<:opiumError:787690178730524672> Роль не найдена**', color = 0xff2020))
                elif not role in member.roles:
                    await member.add_roles(role)
                    await ctx.send(embed = discord.Embed(description = f'**<:opiumSuccess:787692787851067432> Смена ролей для {member.mention}, {rolename}**', color = 0x00ff5f))
                else:
                    await ctx.send(embed = discord.Embed(description = f'**<:opiumInfo:787694319292645426> У пользователя {member.mention} уже есть данная роли**', color = 0x009eff))  
            else:
                role = discord.utils.get(ctx.guild.roles, name = rolename)
                if not role in ctx.guild.roles:
                    await ctx.send(embed = discord.Embed(description = '**<:opiumError:787690178730524672> Роль не найдена**', color = 0xff2020))
                elif role in member.roles:
                    await member.remove_roles(role)
                    await ctx.send(embed = discord.Embed(description = f'**<:opiumSuccess:787692787851067432> Смена ролей для {member.mention}, -{rolename}**', color = 0x00ff5f))
                else:
                    await member.add_roles(role)
                    await ctx.send(embed = discord.Embed(description = f'**<:opiumSuccess:787692787851067432> Смена ролей для {member.mention}, +{rolename}**', color = 0x00ff5f))
        except discord.errors.Forbidden:
            await ctx.send(embed = discord.Embed(description = '**<:opiumError:787690178730524672> Я не могу выдать эту роль. Проверьте мои разрешения и позицию роли**', color = 0xff2020))

    @role.error
    async def role_error(self, ctx, error):
        prefix = self.prx.find_one({"_id": ctx.guild.id})["prefix"]
        if isinstance(error, discord.ext.commands.errors.MemberNotFound):
            await ctx.send(embed = discord.Embed(description = '**<:opiumError:787690178730524672> Пользователь не найден**', color = 0xff2020))
        if isinstance( error, discord.ext.commands.errors.MissingRequiredArgument ):
            emb = discord.Embed( title = '🔰 Command: {}role'.format(prefix), description = '🔹 **Описание:** Добавить/Убрать роль пользователю\n**🔹 Использование:** {}role [user] (+/-)[role]\n'.format(prefix) + f'🔹 **Пример:**\n🔸 {prefix}role cooooper Staff\n🔸 {prefix}role cooooper -Staff')
            await ctx.send(embed = emb)

    @commands.command()
    @commands.cooldown(2, 300, commands.BucketType.user)
    async def privat(self, ctx, member: discord.Member):
        await ctx.channel.purge(limit = 1)
        overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(view_channel = False, connect = False, speak = False, mute_members = False, deafen_members = False, move_members = False, manage_channels = False, manage_permissions = False, manage_webhooks = False, stream = False, create_instant_invite = False),
        ctx.author: discord.PermissionOverwrite(view_channel = True, connect = True, speak = True, mute_members = True, deafen_members = True, move_members = True, manage_channels = True, manage_permissions = True, manage_webhooks = True, stream = True, create_instant_invite = False),
        member: discord.PermissionOverwrite(view_channel = True, connect = True, speak = True, mute_members = True, deafen_members = True, move_members = True, manage_channels = True, manage_permissions = True, manage_webhooks = True, stream = True, create_instant_invite = False)
        }
        cat = discord.utils.get(ctx.guild.categories, id = 742434751499206736)
        channel =  await ctx.guild.create_voice_channel( name = '[🌌] - [Private]', overwrites = overwrites, user_limit = 2, category = cat )
        await asyncio.sleep(21600)
        await channel.delete()

    @privat.error
    async def privat_error(self, ctx, error):
        prefix = self.prx.find_one({"_id": ctx.guild.id})["prefix"]
        if isinstance( error, discord.ext.commands.errors.MissingRequiredArgument ):
            emb = discord.Embed( title = '🔰 Command: {}privat'.format(prefix), description = '🔹 **Описание:** Создание приватного канала на две персоны(Вы и пользователь которого вы упомяните) с полными правами на данный канал\n🔹 **Cooldown:** 5 минут\n🔹 **Использование:** {}privat [@Упоминание] \n'.format(prefix) + '🔹 **Пример:** {}privat @coooper#2187 \n'.format(prefix) + '🔹 **Примечание:** Канал будет удалён спустя 12 часов!' )
            await ctx.send(embed = emb)
        if isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
            emb = discord.Embed( title = '⛔️ Ошибка', color = 0xca1d1d, description = f'{ctx.author.mention}, You are on cooldown. Try again later ⏱' )
            await ctx.send(embed = emb)
            
    #AVATAR
    @commands.command()
    async def avatar(self, ctx, member: discord.Member):
        emb = discord.Embed(title = 'Avatar')
        emb.set_author(name = f'{member}', icon_url = member.avatar_url)
        emb.set_image(url = member.avatar_url)
        await ctx.send(embed = emb)

    @commands.command()
    async def av(self, ctx, member: discord.Member):
        emb = discord.Embed(title = 'Avatar')
        emb.set_author(name = f'{member}', icon_url = member.avatar_url)
        emb.set_image(url = member.avatar_url)
        await ctx.send(embed = emb)

    @avatar.error
    async def avatar_error(self, ctx, error):
        if isinstance( error, discord.ext.commands.errors.MissingRequiredArgument ):
            emb = discord.Embed(title = 'Avatar')
            emb.set_author(name = f'{ctx.author}', icon_url = ctx.author.avatar_url)
            emb.set_image(url = ctx.author.avatar_url)
            await ctx.send(embed = emb)

    @av.error
    async def av_error(self, ctx, error):
        if isinstance( error, discord.ext.commands.errors.MissingRequiredArgument ):
            emb = discord.Embed(title = 'Avatar')
            emb.set_author(name = f'{ctx.author}', icon_url = ctx.author.avatar_url)
            emb.set_image(url = ctx.author.avatar_url)
            await ctx.send(embed = emb)


    #ROle add\remove ADM
    @commands.command()
    @discord.ext.commands.has_permissions(administrator = True)
    async def role_adm(self, ctx, *, role: discord.Role):
        await ctx.channel.purge(limit = 1)
        for channel in self.client.get_guild(ctx.message.guild.id).channels:
            await channel.set_permissions(role, create_instant_invite = True, send_messages = True, speak = True, send_tts_messages = True, manage_channels = True, manage_permissions = True, manage_webhooks = True, read_messages = True, view_channel = True, manage_messages = True, embed_links = True, attach_files = True, read_message_history = True, mention_everyone = True, external_emojis = True, use_external_emojis = True, add_reactions = True, connect = True, stream = True, mute_members = True, deafen_members = True, move_members = True, use_voice_activation = True, priority_speaker = True, reason = f'By {ctx.message.author.display_name}')

    @commands.command()
    @discord.ext.commands.has_permissions(administrator = True)
    async def removerole_adm(self, ctx, *, role: discord.Role):
        await ctx.channel.purge(limit = 1)
        for channel in self.client.get_guild(ctx.message.guild.id).channels:
            await channel.set_permissions(role, overwrite = None, reason = f'By {ctx.message.author.display_name}')

            

    #User add\remove ADM
    @commands.command()
    @discord.ext.commands.has_permissions(administrator = True)
    async def adm_user(self, ctx, member: discord.Member):
        await ctx.channel.purge(limit = 1)
        for channel in self.client.get_guild(ctx.message.guild.id).channels:
            await channel.set_permissions(member, create_instant_invite = True, send_messages = True, speak = True, send_tts_messages = True, manage_channels = True, manage_permissions = True, manage_webhooks = True, read_messages = True, view_channel = True, manage_messages = True, embed_links = True, attach_files = True, read_message_history = True, mention_everyone = True, external_emojis = True, use_external_emojis = True, add_reactions = True, connect = True, stream = True, mute_members = True, deafen_members = True, move_members = True, use_voice_activation = True, priority_speaker = True, reason = f'By {ctx.message.author.display_name}')

    @commands.command()
    @discord.ext.commands.has_permissions(administrator = True)
    async def removeadm_user(self, ctx, member: discord.Member):
        await ctx.channel.purge(limit = 1)
        for channel in self.client.get_guild(ctx.message.guild.id).channels:
            await channel.set_permissions(member, overwrite = None, reason = f'By {ctx.message.author.display_name}')
            
    @commands.command()
    async def randname(self, ctx, count: int = None):
        if count is None:
            count = 1
        elif count > 52:
            count = 53
        else:
            count = count
        nicknames = [
            "Paula_Cooper", "Rafaella_Cooper", "Alicia_Cooper", "Amelia_Cooper", "Adriana_Cooper", "Manuela_Cooper", "Juliana_Cooper", "Elizabeth_Cooper",
            "Alicia_Cooper", "Maria_Cooper", "Adriana_Cooper", "Fiorella_Cooper", "Mariana_Cooper", "Mia_Cooper", "Paige_Cooper", "Brooke_Cooper", "Evelyn_Cooper", 
            "Gabriella_Cooper", "Sophia_Cooper", "Zoe_Cooper", "Natalie_Cooper", "Grace_Cooper", "Jasmine_Cooper", "Bailey_Cooper", "Leah_Cooper", "Avery_Cooper",
            "Olivia_Cooper", "Rebecca_Cooper", "Ella_Cooper", "Arianna_Cooper", "Ashley_Cooper", "Brooke_Cooper", "Victoria_Cooper", "Hailey_Cooper", "Mackenzie_Cooper", 
            "Leslie_Cooper", "Riley_Cooper", "Vanessa_Cooper", "Rachel_Cooper", "Ana_Cooper", "Kiara_Cooper", "Isabel_Cooper", "Michelle_Cooper", "Regina_Cooper",
            "Allison_Cooper", "Valentina_Cooper", "Olivia_Cooper", "Nicole_Cooper", "Emilia_Cooper", "Jose_Cooper", "Alessandra_Cooper", "Juana_Cooper", "Alessandra_Cooper"
        ]
        names = []
        a = 0
        while a < count:
            n = randint(1, (len(nicknames) - 1))
            names.append(nicknames[n])
            a += 1
        await ctx.send(embed = discord.Embed(description = "**\n**".join(names)))

def setup(client):
    client.add_cog(Other(client))
