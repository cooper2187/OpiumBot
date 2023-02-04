import disnake
from disnake.ext import commands
import os

class Reaction(commands.Cog):

    def __init__(self, client):
        self.client = client

    #ON RAW REACTION ADD
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        color_roles_id = [751397706605264976, 751396602144358504, 751396595660095528, 751396594016059442, 751396599002824795, 751396596884963390, 751427599242362960, 751428586765942824, 751397751253630996, 751428880299982879]
        ch = self.client.get_channel(payload.channel_id)
        msg = await ch.fetch_message(payload.message_id)
        if payload.message_id == 751432906542546974:
            if payload.emoji.name == '⚪':
                await payload.member.add_roles(payload.member.guild.get_role(751397706605264976))
                await msg.remove_reaction('⚪', payload.member)
        if payload.message_id == 751432906542546974:
            if payload.emoji.name == '⚫':
                    await payload.member.add_roles(payload.member.guild.get_role(751396602144358504))
                    await msg.remove_reaction('⚫', payload.member)
        if payload.message_id == 751432906542546974:
            if payload.emoji.name == '🔴':
                    await payload.member.add_roles(payload.member.guild.get_role(751396595660095528))
                    await msg.remove_reaction('🔴', payload.member)
        if payload.message_id == 751432906542546974:
            if payload.emoji.name == '🔵':
                    await payload.member.add_roles(payload.member.guild.get_role(751396594016059442))
                    await msg.remove_reaction('🔵', payload.member)
        if payload.message_id == 751432906542546974:
            if payload.emoji.name == '🟢':
                    await payload.member.add_roles(payload.member.guild.get_role(751396599002824795))
                    await msg.remove_reaction('🟢', payload.member)
        if payload.message_id == 751432906542546974:
            if payload.emoji.name == '🟡':
                    await payload.member.add_roles(payload.member.guild.get_role(751396596884963390))
                    await msg.remove_reaction('🟡', payload.member)
        if payload.message_id == 751432906542546974:
            if payload.emoji.name == '🟣':
                    await payload.member.add_roles(payload.member.guild.get_role(751427599242362960))
                    await msg.remove_reaction('🟣', payload.member)
        if payload.message_id == 751432906542546974:
            if payload.emoji.name == '🟤':
                    await payload.member.add_roles(payload.member.guild.get_role(751428586765942824))
                    await msg.remove_reaction('🟤', payload.member)
        if payload.message_id == 751432906542546974:
            if payload.emoji.name == '🟠':
                    await payload.member.add_roles(payload.member.guild.get_role(751397751253630996))
                    await msg.remove_reaction('🟠', payload.member)
        if payload.message_id == 751432906542546974:
            if payload.emoji.name == '🔘':
                    await payload.member.add_roles(payload.member.guild.get_role(751428880299982879))
                    await msg.remove_reaction('🔘', payload.member)
        if payload.message_id == 751432906542546974:
            a = 0
            while a < len(color_roles_id):
                if payload.member.guild.get_role(color_roles_id[a]) in payload.member.roles:
                    await payload.member.remove_roles(payload.member.guild.get_role(color_roles_id[a]))
                a += 1

def setup(client):
    client.add_cog(Reaction(client))