import disnake
from disnake.ext import commands
import os
import pymongo
from pymongo import MongoClient
from file1 import triada_num
import asyncio
from random import randint

money_options = [
    disnake.SelectOption(label = 'Ввести сумму', value = "cc", description = "Количество монет на которые хотите сыграть", emoji = "💲"),
    disnake.SelectOption(label = '100 Cooper Coins', value = "cc1", description = "Количество монет на которые хотите сыграть", emoji = "💶"),
    disnake.SelectOption(label = '200 Cooper Coins', value = "cc2", description = "Количество монет на которые хотите сыграть", emoji = "💵"),
    disnake.SelectOption(label = '500 Cooper Coins', value = "cc3", description = "Количество монет на которые хотите сыграть", emoji = "💷"),
    disnake.SelectOption(label = '1 000 Cooper Coins', value = "cc4", description = "Количество монет на которые хотите сыграть", emoji = "💴"),
    disnake.SelectOption(label = 'Назад', value = "exit", description = "Вернуться к выбору стороны", emoji = "🔙")
]

class Viev(disnake.ui.View):
    def __init__(self):
        super().__init__()

class Select(disnake.ui.Select):
    def __init__(self, options, placeholder):
        self.cluster = MongoClient("mongodb+srv://andrewnobot:xuInmV8QmD9GRR5c@cluster0.28biu.mongodb.net/opiumdb?retryWrites=true&w=majority")
        self.coll = self.cluster.opiumdb.collopiumdb
        self.colors = self.cluster.opium.prefixcoll
        super().__init__(placeholder = placeholder, options = options, max_values = 1)
    async def callback(self, interaction: disnake.ModalInteraction):
        for val in self.values:
            global CooperCoins
            if val == "cc":
                await interaction.response.send_modal(Modal(title = "Введите сумму", components = [disnake.ui.TextInput(label = f"Введите сумму на которую хотите сыграть", placeholder = "Введите значение", style = disnake.TextInputStyle.short, value = None, custom_id = "hz", min_length = 1, max_length = 20)]))
            elif val == "exit":
                emb = disnake.Embed(description = "**Выберите сторону Орел или Решка - <:unverified:1062370904941793417>\nВведите сумму на которую хотите сыграть - <:unverified:1062370904941793417>\n**", color = 0x3498db)
                emb.set_author(name = f'{interaction.guild.name} | Орёл - Решка', icon_url = interaction.guild.icon)
                emb.set_footer(text = f'(X) {interaction.author.name} x {m_m.name} (X)')
                await interaction.response.edit_message(embed = emb, view = Button())
            else:
                CooperCoins = 0
                if val == "cc1":
                    CooperCoins = 100
                elif val == "cc2":
                    CooperCoins = 200
                elif val == "cc3":
                    CooperCoins = 500
                elif val == "cc4":
                    CooperCoins = 1000
                else:
                    pass
                money = self.coll.find_one({"_id": interaction.author.id})['cash']
                m_money = self.coll.find_one({"_id": m_m.id})['cash']
                summ = 0
                if money < m_money:
                    summ = money
                elif m_money < money:
                    summ = m_money
                else:
                    summ = money
                if CooperCoins > summ:
                    emb = disnake.Embed(description = f"**Выберите сторону Орел или Решка - <:verified:1062370903524118638>\nВведите сумму на которую хотите сыграть - <:unverified:1062370904941793417>\n\n⛔ У вас или у {m_m.mention} недостаточно Cooper Coins.\nВведите сумму не более {triada_num(summ)} cc**", color = 0x3498db)
                    emb.set_author(name = f'{interaction.guild.name} | Орёл - Решка', icon_url = interaction.guild.icon)
                    emb.set_footer(text = f'({a_ch}) {interaction.author.name} x {m_m.name} ({m_ch})')
                    await interaction.response.edit_message(embed = emb, view = Viev().add_item(Select(options = money_options, placeholder = "💵 Ввести сумму")))
                else:
                    emb = disnake.Embed(description = f"**Выберите сторону Орел или Решка - <:verified:1062370903524118638>\nВведите сумму на которую хотите сыграть - `{triada_num(CooperCoins)}` cc\n**", color = 0x3498db)
                    emb.set_author(name = f'{interaction.guild.name} | Орёл - Решка', icon_url = interaction.guild.icon)
                    emb.set_footer(text = f'({a_ch}) {interaction.author.name} x {m_m.name} ({m_ch})')
                    await interaction.response.edit_message(embed = emb, view = Button2())

class Modal(disnake.ui.Modal):
    def __init__(self, title, components):
        self.cluster = MongoClient("mongodb+srv://andrewnobot:xuInmV8QmD9GRR5c@cluster0.28biu.mongodb.net/opiumdb?retryWrites=true&w=majority")
        self.coll = self.cluster.opiumdb.collopiumdb
        super().__init__(title = title, components = components)
    async def callback(self, interaction: disnake.ModalInteraction):
        try:
            global CooperCoins
            CooperCoins = 0
            for a in dict.values(interaction.text_values):
                CooperCoins = int(a)
            money = self.coll.find_one({"_id": interaction.author.id})['cash']
            m_money = self.coll.find_one({"_id": m_m.id})['cash']
            summ = 0
            if money < m_money:
                summ = money
            elif m_money < money:
                summ = m_money
            else:
                summ = money
            if CooperCoins <= 0:
                emb = disnake.Embed(description = "**Выберите сторону Орел или Решка - <:verified:1062370903524118638>\nВведите сумму на которую хотите сыграть - <:unverified:1062370904941793417>\n\n⛔ Введена неверная сумма. Попробуйте снова**", color = 0x3498db)
                emb.set_author(name = f'{interaction.guild.name} | Орёл - Решка', icon_url = interaction.guild.icon)
                emb.set_footer(text = f'({a_ch}) {interaction.author.name} x {m_m.name} ({m_ch})')
                await interaction.response.edit_message(embed = emb, view = Viev().add_item(Select(options = money_options, placeholder = "💵 Ввести сумму")))
            elif CooperCoins > summ:
                emb = disnake.Embed(description = f"**Выберите сторону Орел или Решка - <:verified:1062370903524118638>\nВведите сумму на которую хотите сыграть - <:unverified:1062370904941793417>\n\n⛔ У вас или у {m_m.mention} недостаточно Cooper Coins.\nВведите сумму не более {triada_num(summ)} cc**", color = 0x3498db)
                emb.set_author(name = f'{interaction.guild.name} | Орёл - Решка', icon_url = interaction.guild.icon)
                emb.set_footer(text = f'({a_ch}) {interaction.author.name} x {m_m.name} ({m_ch})')
                await interaction.response.edit_message(embed = emb, view = Viev().add_item(Select(options = money_options, placeholder = "💵 Ввести сумму")))
            else:                         
                emb = disnake.Embed(description = f"**Выберите сторону Орел или Решка - <:verified:1062370903524118638>\nВведите сумму на которую хотите сыграть - `{triada_num(CooperCoins)}` cc\n**", color = 0x3498db)
                emb.set_author(name = f'{interaction.guild.name} | Орёл - Решка', icon_url = interaction.guild.icon)
                emb.set_footer(text = f'({a_ch}) {interaction.author.name} x {m_m.name} ({m_ch})')
                await interaction.response.edit_message(embed = emb, view = Button2())
        except ValueError:
            emb = disnake.Embed(description = "**Выберите сторону Орел или Решка - <:verified:1062370903524118638>\nВведите сумму на которую хотите сыграть - <:unverified:1062370904941793417>\n\n⛔ Введена неверная сумма. Попробуйте снова**", color = 0x3498db)
            emb.set_author(name = f'{interaction.guild.name} | Орёл - Решка', icon_url = interaction.guild.icon)
            emb.set_footer(text = f'({a_ch}) {interaction.author.name} x {m_m.name} ({m_ch})')
            await interaction.response.edit_message(embed = emb, view = Viev().add_item(Select(options = money_options, placeholder = "💵 Ввести сумму")))

class Button2(disnake.ui.View):
    def __init__(self):
        self.cluster = MongoClient("mongodb+srv://andrewnobot:xuInmV8QmD9GRR5c@cluster0.28biu.mongodb.net/opiumdb?retryWrites=true&w=majority")
        self.coll = self.cluster.opiumdb.collopiumdb
        self.colors = self.cluster.opium.prefixcoll
        super().__init__(timeout = None)
    @disnake.ui.button(label = "Предложить игру", style = disnake.ButtonStyle.green, emoji = "✅")
    async def callback(self, button: disnake.Button, ctx: disnake.Interaction):
        emb = disnake.Embed(description = f'**{ctx.author.mention} предложил {m_m.mention} игру на {CooperCoins} cc\n\n{ctx.author.display_name} - <:verified:1062370903524118638>\n{m_m.display_name} - <:unverified:1062370904941793417>**', color = 0x425be0)
        emb.set_author(name = f'{ctx.guild.name} | Орёл - Решка', icon_url = ctx.guild.icon)
        emb.set_footer(text = f'({a_ch}) {ctx.author.name} x {m_m.name} ({m_ch})')
        global a_m
        a_m = ctx.author
        await ctx.response.edit_message(view = None)
        await ctx.send(embed = emb, view = Button3())
        await ctx.delete_original_response()
    @disnake.ui.button(label = "Назад", style = disnake.ButtonStyle.red, emoji = "🔙")
    async def callback1(self, button: disnake.Button, ctx: disnake.Interaction):
        emb = disnake.Embed(description = "**Выберите сторону Орел или Решка - <:verified:1062370903524118638>\nВведите сумму на которую хотите сыграть - <:unverified:1062370904941793417>\n**", color = 0x3498db)
        emb.set_author(name = f'{ctx.guild.name} | Орёл - Решка', icon_url = ctx.guild.icon)
        emb.set_footer(text = f'({a_ch}) {ctx.author.name} x {m_m.name} ({m_ch})')
        await ctx.response.edit_message(embed = emb, view = Viev().add_item(Select(options = money_options, placeholder = "💵 Ввести сумму")))
        
class Button3(disnake.ui.View):
    def __init__(self):
        self.cluster = MongoClient("mongodb+srv://andrewnobot:xuInmV8QmD9GRR5c@cluster0.28biu.mongodb.net/opiumdb?retryWrites=true&w=majority")
        self.coll = self.cluster.opiumdb.collopiumdb
        super().__init__(timeout = None)
    @disnake.ui.button(label = "Согласиться", style = disnake.ButtonStyle.green, emoji = "✔️")
    async def callback(self, button: disnake.Button, ctx: disnake.Interaction):
        if ctx.author.id == m_m.id:
            emb = disnake.Embed(description = f'**{a_m.mention} предложил {m_m.mention} игру на {CooperCoins} cc\n\n{a_m.display_name} - <:verified:1062370903524118638>\n{m_m.display_name} - <:verified:1062370903524118638>**', color = 0x425be0)
            emb.set_author(name = f'{m_m.guild.name} | Орёл - Решка', icon_url = m_m.guild.icon)
            emb.set_footer(text = f'({a_ch}) {a_m.name} x {m_m.name} ({m_ch})')
            await ctx.response.edit_message(embed = emb)
            n = randint(0, 1)
            if n == 0:
                if a_ch == "Орёл":
                    winner = a_m
                    loser = m_m
                else:
                    winner = m_m
                    loser = a_m
                self.coll.update_one({"_id": winner.id}, {"$inc": {"cash": CooperCoins}})
                self.coll.update_one({"_id": loser.id}, {"$inc": {"cash": -CooperCoins}})
                self.coll.update_one({"_id": 1}, {"$inc": {"cash": CooperCoins}})
                e1 = disnake.Embed(description = f'**Выпало: Орёл\nПобеда {winner.mention}, + {CooperCoins} Cooper Coins**', color = 0x1b7fdf)
                e1.set_author(name = f'{winner.guild.name} | Орёл - Решка', icon_url = winner.guild.icon)
                e1.set_footer(text = f'({a_ch}) {a_m.name} x {m_m.name} ({m_ch})')
                await ctx.edit_original_response(embed = e1, view = None)
                await ctx.edit_original_message(view = Button4())
            elif n == 1:
                if a_ch == "Решка":
                    winner = a_m
                    loser = m_m
                else:
                    winner = m_m
                    loser = a_m
                self.coll.update_one({"_id": winner.id}, {"$inc": {"cash": CooperCoins}})
                self.coll.update_one({"_id": loser.id}, {"$inc": {"cash": -CooperCoins}})
                self.coll.update_one({"_id": 1}, {"$inc": {"cash": CooperCoins}})
                e1 = disnake.Embed(description = f'**Выпало: Решка\nПобеда {winner.mention}, + {CooperCoins} Cooper Coins**', color = 0x1b7fdf)
                e1.set_author(name = f'{winner.guild.name} | Орёл - Решка', icon_url = winner.guild.icon)
                e1.set_footer(text = f'({a_ch}) {a_m.name} x {m_m.name} ({m_ch})')
                await ctx.edit_original_response(embed = e1, view = None)
                await ctx.edit_original_message(view = Button4())
            else:
                pass
    @disnake.ui.button(label = "Отказаться", style = disnake.ButtonStyle.red, emoji = "❌")
    async def callback1(self, button: disnake.Button, ctx: disnake.Interaction):
        if (ctx.author.id == m_m.id or ctx.author.id == a_m.id):
            emb = disnake.Embed(description = f"**⛔ {ctx.author.mention} откзался от игры**", color = 0x3498db)
            emb.set_author(name = f'{ctx.guild.name} | Орёл - Решка', icon_url = ctx.guild.icon)
            emb.set_footer(text = f'({a_ch}) {ctx.author.name} x {m_m.name} ({m_ch})')
            await ctx.response.edit_message(embed = emb, view = None)
            await ctx.delete_original_response(delay = 3)
            await asyncio.sleep(3)
        else:
            pass

class Button4(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout = 10)
    @disnake.ui.button(label = "Play again", style = disnake.ButtonStyle.blurple, emoji = "🔃")
    async def callback(self, button: disnake.Button, ctx: disnake.Interaction):
        if ctx.author.id == a_m.id:
            emb = disnake.Embed(description = "**Выберите сторону Орел или Решка - <:unverified:1062370904941793417>\nВведите сумму на которую хотите сыграть - <:unverified:1062370904941793417>\n**", color = 0x3498db)
            emb.set_author(name = f'{ctx.guild.name} | Орёл - Решка', icon_url = ctx.guild.icon)
            emb.set_footer(text = f'(X) {ctx.author.name} x {m_m.name} (X)')
            await ctx.response.edit_message(view = None)
            await ctx.send(embed = emb, view = Button(), ephemeral = True)
            self.stop()
        else:
            await ctx.send(embed = disnake.Embed(description = "**⛔ Предложить игру заново может только инициатор предыдущей игры.\nСоздать новую игру можно через /orel-reshka**"), ephemeral = True)

class Button(disnake.ui.View):
    def __init__(self):
        self.cluster = MongoClient("mongodb+srv://andrewnobot:xuInmV8QmD9GRR5c@cluster0.28biu.mongodb.net/opiumdb?retryWrites=true&w=majority")
        self.coll = self.cluster.opiumdb.collopiumdb
        self.colors = self.cluster.opium.prefixcoll
        super().__init__(timeout = None)
    @disnake.ui.button(label = "Орёл", style = disnake.ButtonStyle.green, emoji = "🔱")
    async def callback(self, button: disnake.Button, ctx: disnake.Interaction):
        global a_ch
        global m_ch
        a_ch = "Орёл"
        m_ch = "Решка"
        emb = disnake.Embed(description = "**Выберите сторону Орел или Решка - <:verified:1062370903524118638>\nВведите сумму на которую хотите сыграть - <:unverified:1062370904941793417>\n**", color = 0x3498db)
        emb.set_author(name = f'{ctx.guild.name} | Орёл - Решка', icon_url = ctx.guild.icon)
        emb.set_footer(text = f'(Орёл) {ctx.author.name} x {m_m.name} (Решка)')
        await ctx.response.edit_message(embed = emb, view = Viev().add_item(Select(options = money_options, placeholder = "💵 Ввести сумму")))
    @disnake.ui.button(label = "Решка", style = disnake.ButtonStyle.green, emoji = "🔆")
    async def callback2(self, button: disnake.Button, ctx: disnake.Interaction):
        global a_ch
        global m_ch
        a_ch = "Решка"
        m_ch = "Орёл"
        emb = disnake.Embed(description = "**Выберите сторону Орел или Решка - <:verified:1062370903524118638>\nВведите сумму на которую хотите сыграть - <:unverified:1062370904941793417>\n**", color = 0x3498db)
        emb.set_author(name = f'{ctx.guild.name} | Орёл - Решка', icon_url = ctx.guild.icon)
        emb.set_footer(text = f'(Решка) {ctx.author.name} x {m_m.name} (Орёл)')
        await ctx.response.edit_message(embed = emb, view = Viev().add_item(Select(options = money_options, placeholder = "💵 Ввести сумму")))


class OrelReshka(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cluster = MongoClient("mongodb+srv://andrewnobot:xuInmV8QmD9GRR5c@cluster0.28biu.mongodb.net/opium?retryWrites=true&w=majority", connect = False)
        self.collection = self.cluster.opium.collopium
        self.colors = self.cluster.opium.prefixcoll

    @commands.slash_command(name = 'orel-reshka', description = "Сыграть в с другим пользователем в Орел или Решка")
    async def orel_reshka_game(self, ctx: disnake.ApplicationCommandInteraction, member: disnake.Member):
        global m_m
        m_m = member
        emb = disnake.Embed(description = "**Выберите сторону Орел или Решка - <:unverified:1062370904941793417>\nВведите сумму на которую хотите сыграть - <:unverified:1062370904941793417>\n**", color = 0x3498db)
        emb.set_author(name = f'{ctx.guild.name} | Орёл - Решка', icon_url = ctx.guild.icon)
        emb.set_footer(text = f'(X) {ctx.author.name} x {member.name} (X)')
        await ctx.send(embed = emb, view = Button(), ephemeral = True)

def setup(client):
    client.add_cog(OrelReshka(client))