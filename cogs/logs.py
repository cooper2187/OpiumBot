import discord
from discord.ext import commands
import datetime
import pytz

class Logs(commands.Cog):

    def __init__(self, client):
        self.client = client
        
    #ON MEMBER UPDATE
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        logchannel = self.client.get_channel(722457936051306596)
        if not before.guild.id == 722190594268725288:
            return
        if before.nick != after.nick:
            e = discord.Embed(title = f'{before.guild.name} | Смена никнейма', color = 0x546c9b, description = f'**Пользователь: {before.mention}\n\nДо: `{before.nick}`\n\nПосле: `{after.nick}`**')
            await logchannel.send(embed = e)
        try:
            ctx = self.client.get_channel(722457936051306596)
            rlist1 = []
            rlist2 = []
            for r in before.roles:
                rlist1.append(r.id)
            for r in after.roles:
                rlist2.append(r.id)
            if len(rlist1) > len(rlist2):
                res = list(set(rlist1) - set(rlist2))
                role = discord.utils.get(before.guild.roles, id = res[0])
                e = discord.Embed(description = f'**{before.mention} was removed from the `{role.name}` role**', color = discord.Colour.blue(), timestamp = datetime.datetime.now())
            elif len(rlist1) < len(rlist2):
                res = list(set(rlist2) - set(rlist1))
                role = discord.utils.get(before.guild.roles, id = res[0])
                e = discord.Embed(description = f'**{before.mention} was given the `{role.name}` role**', color = discord.Colour.blue(), timestamp = datetime.datetime.now())
            else:
                return
            e.set_author(name = f"{before} | Обновление ролей", icon_url = before.avatar_url)
            e.set_footer(text = f'Role ID: {role.id}')
            await ctx.send(embed = e)
        except IndexError:
            pass

    #ON MESSAGE EDIT
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        try:
            logchannel = self.client.get_channel(798248355888496642)
            if not before.guild.id == 722190594268725288:
                return
            elif before.channel == logchannel:
                return
            elif before.embeds or before.author.id == 382522784841990144:
                return
            else:
                e = discord.Embed(title = f'{before.guild.name} | Сообщение изменено ✉️ 🖊️', description = f'**{before.author.mention} отредактировал(а) своё сообщение\nв канале #{before.channel.name}. [Перейти к сообщению]({before.jump_url})**')
                e.add_field(name = 'До:', value = before.content, inline = False)
                e.add_field(name = 'После:', value = after.content, inline = False)
                e.set_footer(text = f'Message ID: {before.id} •  Author ID: {before.author.id}', icon_url = before.author.avatar_url)
                await logchannel.send(embed = e)
        except AttributeError:
            pass


    #ON MESSAGE DELETE
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        try:
            logchannel = self.client.get_channel(798248355888496642)
            if not message.guild.id == 722190594268725288:
                return
            elif message.channel == logchannel:
                return
            elif message.author.bot or message.author.id == 382522784841990144:
                return
            else:
                time = datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime("%A, %d %B %Y, %H:%M:%S")
                e = discord.Embed(title = f'{message.guild.name} | Сообщение удалено ✉️❌', description = f'**Отправитель: {message.author.mention}. Канал: {message.channel.mention}\nСообщение:** {message.content}')
                e.set_footer(text = f'{time}', icon_url = message.author.avatar_url)
                await logchannel.send(embed = e)
        except AttributeError:
            pass
            
    #ON MEMBER JOIN
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        emb = discord.Embed(title = '☑️⠀Новый пользователь', color = 0x951fad, description = f'\n\n**{member}** присоединился(-ась) к серверу!')
        emb.set_thumbnail(url = member.avatar_url)
        emb.set_footer(text = f'Всего пользователей: {member.guild.member_count}')
        await channel.send(embed = emb)

    #ON MEMBER REMOVE
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = member.guild.system_channel
        emb = discord.Embed(title = '❌⠀До скорой встречи', color = 0x951fad, description = f'\n\n**{member}** покинул(-а) сервер!')
        emb.set_thumbnail(url = member.avatar_url)
        emb.set_footer(text = f'Пользователей осталось: {member.guild.member_count}')
        await channel.send(embed = emb)

def setup(client):
    client.add_cog(Logs(client))
