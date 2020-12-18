import discord
from discord.ext import commands
import os

class Reaction(commands.Cog):

    def __init__(self, client):
        self.client = client

    #ON RAW REACTION ADD
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == 751432906542546974:
            if payload.emoji.name == '⚪':
                await payload.member.add_roles(payload.member.guild.get_role(751397706605264976))
        if payload.message_id == 751432906542546974:
            if payload.emoji.name == '⚫':
                    await payload.member.add_roles(payload.member.guild.get_role(751396602144358504))
        if payload.message_id == 751432906542546974:
            if payload.emoji.name == '🔴':
                    await payload.member.add_roles(payload.member.guild.get_role(751396595660095528))
        if payload.message_id == 751432906542546974:
            if payload.emoji.name == '🔵':
                    await payload.member.add_roles(payload.member.guild.get_role(751396594016059442))
        if payload.message_id == 751432906542546974:
            if payload.emoji.name == '🟢':
                    await payload.member.add_roles(payload.member.guild.get_role(751396599002824795))
        if payload.message_id == 751432906542546974:
            if payload.emoji.name == '🟡':
                    await payload.member.add_roles(payload.member.guild.get_role(751396596884963390))
        if payload.message_id == 751432906542546974:
            if payload.emoji.name == '🟣':
                    await payload.member.add_roles(payload.member.guild.get_role(751427599242362960))
        if payload.message_id == 751432906542546974:
            if payload.emoji.name == '🟤':
                    await payload.member.add_roles(payload.member.guild.get_role(751428586765942824))
        if payload.message_id == 751432906542546974:
            if payload.emoji.name == '🟠':
                    await payload.member.add_roles(payload.member.guild.get_role(751397751253630996))
        if payload.message_id == 751432906542546974:
            if payload.emoji.name == '🔘':
                    await payload.member.add_roles(payload.member.guild.get_role(751428880299982879))

    #ON RAW REACTION REMOVE
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id == 751432906542546974:
            if payload.emoji.name == '⚪':
                role = self.client.get_guild(payload.guild_id).get_role(751397706605264976)
                member = self.client.get_guild(payload.guild_id).get_member(payload.user_id)
                await member.remove_roles(role)
        if payload.message_id == 751432906542546974:
            if payload.emoji.name == '⚫':
                role = self.client.get_guild(payload.guild_id).get_role(751396602144358504)
                member = self.client.get_guild(payload.guild_id).get_member(payload.user_id)
                await member.remove_roles(role)
        if payload.message_id == 751432906542546974:
            if payload.emoji.name == '🔴':
                role = self.client.get_guild(payload.guild_id).get_role(751396595660095528)
                member = self.client.get_guild(payload.guild_id).get_member(payload.user_id)
                await member.remove_roles(role)
        if payload.message_id == 751432906542546974:
            if payload.emoji.name == '🔵':
                role = self.client.get_guild(payload.guild_id).get_role(751396594016059442)
                member = self.client.get_guild(payload.guild_id).get_member(payload.user_id)
                await member.remove_roles(role)
        if payload.message_id == 751432906542546974:
            if payload.emoji.name == '🟢':
                role = self.client.get_guild(payload.guild_id).get_role(751396599002824795)
                member = self.client.get_guild(payload.guild_id).get_member(payload.user_id)
                await member.remove_roles(role)
        if payload.message_id == 751432906542546974:
            if payload.emoji.name == '🟡':
                role = self.client.get_guild(payload.guild_id).get_role(751396596884963390)
                member = self.client.get_guild(payload.guild_id).get_member(payload.user_id)
                await member.remove_roles(role)
        if payload.message_id == 751432906542546974:
            if payload.emoji.name == '🟣':
                role = self.client.get_guild(payload.guild_id).get_role(751427599242362960)
                member = self.client.get_guild(payload.guild_id).get_member(payload.user_id)
                await member.remove_roles(role)
        if payload.message_id == 751432906542546974:
            if payload.emoji.name == '🟤':
                role = self.client.get_guild(payload.guild_id).get_role(751428586765942824)
                member = self.client.get_guild(payload.guild_id).get_member(payload.user_id)
                await member.remove_roles(role)
        if payload.message_id == 751432906542546974:
            if payload.emoji.name == '🟠':
                role = self.client.get_guild(payload.guild_id).get_role(751397751253630996)
                member = self.client.get_guild(payload.guild_id).get_member(payload.user_id)
                await member.remove_roles(role)
        if payload.message_id == 751432906542546974:
            if payload.emoji.name == '🔘':
                role = self.client.get_guild(payload.guild_id).get_role(751428880299982879)
                member = self.client.get_guild(payload.guild_id).get_member(payload.user_id)
                await member.remove_roles(role)


def setup(client):
    client.add_cog(Reaction(client))