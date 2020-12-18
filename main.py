import discord
from discord.ext import commands
import os
import pymongo
from pymongo import MongoClient
from discord import Activity, ActivityType

cluster = MongoClient("mongodb+srv://andrewnobot:xuInmV8QmD9GRR5c@cluster0.28biu.mongodb.net/opiumdb?retryWrites=true&w=majority")
prx = cluster.opiumdb.prefixcoll

def get_prefix(client, message):
    return prx.find_one({"_id": message.guild.id})["prefix"]


client = commands.Bot(command_prefix = get_prefix, intents = discord.Intents.all())
client.remove_command('help')

@client.event
async def on_guild_join(guild):
    prefix = {
        "_id": guild.id,
        "name": guild.name,
        "prefix": "+"
    }
    if prx.count_documents({"_id": guild.id}) == 0:
        prx.insert_one(prefix)

@client.event
async def on_guild_remove(guild):
    prx.find_one({"_id": guild.id}, {"$set": {"prefix": "+"}})

@client.command()
@commands.has_permissions(administrator = True)
async def changeprefix(ctx, pref):
    prx.update_one({"_id": ctx.guild.id}, {"$set": {"prefix": f"{pref}"}})
    await ctx.send(f'**Префикс изменён на `{pref}`**')

def dev(ctx):
    return ctx.author.id == 382522784841990144

@client.event
async def on_ready():
    print('Online')
    await client.change_presence(activity=discord.Game(name="Выращивание марихуаны"))

@client.command()
@commands.check(dev)
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")
    await ctx.send(embed = discord.Embed(description = f'**Cog `{extension}.py` is load!**', color = 0x2eb300))

@client.command()
@commands.check(dev)
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    await ctx.send(embed = discord.Embed(description = f'**Cog `{extension}.py` is unload!**', color = 0xff1c00))

@client.command()
@commands.check(dev)
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")
    await ctx.send(embed = discord.Embed(description = f'**Cog `{extension}.py` is reload!**', color = 0xffdf00))

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

#toke = open('token.txt', 'r').readline()
#client.run(toke)
client.run(os.environ['BOT_TOKEN'])
