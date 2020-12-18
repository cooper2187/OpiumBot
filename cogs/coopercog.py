import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient
import os
from random import randint
import asyncio
import time
import datetime
from datetime import timezone, tzinfo, timedelta
from random import sample
import array
import math

class Cooperka(commands.Cog):

    def __init__(self, client):
        self.client = client    
        self.cluster = MongoClient("mongodb+srv://andrewnobot:xuInmV8QmD9GRR5c@cluster0.28biu.mongodb.net/opiumdb?retryWrites=true&w=majority")
        self.coll = self.cluster.opiumdb.collopiumdb
        self.prx = self.cluster.opiumdb.prefixcoll

    

def setup(client):
    client.add_cog(Cooperka(client))

#\n\nУровень: `{a_lvl}`\n\nXp: `{a_xp}/{lvl_xp}`\n\nБаланс: `{a_cash}` Cooper Coins**'