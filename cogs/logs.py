import discord
from discord.ext import commands
import datetime
import locale
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
        if before.display_name != after.display_name:
            e = discord.Embed(title = f'{before.guild.name} | Смена никнейма', color = 0x546c9b, description = f'**Пользователь: {before.mention}\n\nДо: `{before.display_name}`\n\nПосле: `{after.display_name}`**')
            await logchannel.send(embed = e)

    #ON MESSAGE EDIT
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        try:
            logchannel = self.client.get_channel(798248355888496642)
            if not before.guild.id == 722190594268725288:
                return
            elif before.channel == logchannel:
                return
            elif before.embeds:
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
            elif message.author.bot:
                return
            else:
                locale.setlocale(locale.LC_ALL, "ru_RU.utf8")
                time = datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime("%A, %d %b. %Y г., %H:%M:%S")
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
