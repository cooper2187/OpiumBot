import discord
from discord.ext import commands
import os
import pymongo
from pymongo import MongoClient

class Colors(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cluster = MongoClient("mongodb+srv://andrewnobot:xuInmV8QmD9GRR5c@cluster0.28biu.mongodb.net/opium?retryWrites=true&w=majority", connect = False)
        self.collection = self.cluster.opium.collopium

    #ON MESSAGE
    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.author.bot:
                return
            elif not message.channel.id == 751072089347457076:
                return
            else:
                await message.delete(delay = 1)
                if self.collection.find_one({"_id": message.author.id})["role"] == 0:
                    role = await message.guild.create_role(name = 'custom', mentionable = True)
                    await message.author.add_roles(role)
                    self.collection.update_one({"_id": message.author.id}, {"$set": {"role": role.id}})
                    msg = message.content.replace('#', '')
                    msg1 = '0x' + msg
                    self.collection.update_one({"_id": message.author.id}, {"$set": {"color": msg1}})
                    role1 = discord.utils.get(message.guild.roles, id = role.id)
                    perm = discord.Permissions(change_nickname = True, read_messages = True, view_channel = True, send_messages = True, send_tts_messages = True, embed_links = True, attach_files = True, read_message_history = True, mention_everyone = True, external_emojis = True, connect = True, speak = True, stream = True, use_voice_activation = True)
                    await role1.edit(position = 38, permissions = perm, colour = discord.Colour(value = int(msg1, base = 16)))
                    emb = discord.Embed(description = '**Цвет успешно изменён! 👍**', color = discord.Colour(value = int(msg1, base = 16)))
                    emb.set_author(name = message.author, icon_url = message.author.avatar_url)
                    emb.set_footer(text = f'Color • #{msg}')
                    await message.channel.send(embed = emb)
                else:
                    data = self.collection.find_one({"_id": message.author.id})
                    arole = data['role']
                    arole1 = discord.utils.get(message.guild.roles, id = arole)
                    amsg = message.content.replace('#', '')
                    amsg1 = '0x' + amsg
                    self.collection.update_one({"_id": message.author.id}, {"$set": {"color": amsg1}})
                    await arole1.edit(color = discord.Colour(value = int(amsg1, base = 16)))
                    emb = discord.Embed(description = '**Цвет успешно изменён! 👍**', color = discord.Colour(value = int(amsg1, base = 16)))
                    emb.set_author(name = message.author, icon_url = message.author.avatar_url)
                    emb.set_footer(text = f'Color • #{amsg}')
                    await message.channel.send(embed = emb)
        except ValueError:
            e = discord.Embed(title = '⛔ Ошибка', description = '**Такого цвета не существует**', color = 0xff1c00) 
            await message.channel.send(embed = e, delete_after = 3)
        except discord.errors.HTTPException:
            e = discord.Embed(title = '⛔ Ошибка', description = '**Такого цвета не существует**', color = 0xff1c00) 
            await message.channel.send(embed = e, delete_after = 3)

    #ON MEMBER JOIN
    @commands.Cog.listener()
    async def on_member_join(self, member):
        colors = {
            "_id": member.id,
            "name": f"{member.name}#{member.discriminator}",
            "role": 0,
            "color": None
        }
        if self.collection.count_documents({"_id": member.id}) == 0:
            self.collection.insert_one(colors)

def setup(client):
    client.add_cog(Colors(client))