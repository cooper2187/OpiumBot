import disnake
from disnake.ext import commands
import os
import asyncio
import pymongo
from pymongo import MongoClient
from main import sets
from file1 import triada_num
from random import sample

stats_options = [
    disnake.SelectOption(label = 'Change Username', value = "username", description = "Сменить имя пользоваетля", emoji = "🖊️"),
    disnake.SelectOption(label = 'Set balance', value = "balance", description = "Установить баланс пользователю", emoji = "💵"),
    disnake.SelectOption(label = 'Set lvl', value = "lvl", description = "Установить уровень пользователю", emoji = "🏅"),
    disnake.SelectOption(label = 'Set xp', value = "xp", description = "Установить xp пользователю", emoji = "💎"),
    disnake.SelectOption(label = 'Set spin(max. win)', value = "sbonus", description = "Установить макс. выигрыш в рулетке", emoji = "💰"),
    disnake.SelectOption(label = 'Set daily spin(max. win)', value = "dsbonus", description = "Установить макс. выигрыш в ежедневной рулетке", emoji = "💰"),
    disnake.SelectOption(label = 'Set jackpot(drop chance)', value = "spot", description = "Установить шанс выпаления джекпота", emoji = "🔋"),
    disnake.SelectOption(label = 'Set jackpot(win)', value = "jpwin", description = "Установить сумму джекпота", emoji = "🎁"),
    disnake.SelectOption(label = 'Set spin up(price)', value = "sprice", description = "Установить цену на повышение навыка 'макс. выигрыш в рулетке'", emoji = "💸"),
    disnake.SelectOption(label = 'Set daily spin up(price)', value = "dsprice", description = "Установить цену на повышение навыка 'макс. выигрыш в ежедневной рулетке'", emoji = "💸"),
    disnake.SelectOption(label = 'Set daily(status)', value = "daily", description = "Установить статус для ежедневной рулетки", emoji = "♻️"),
    disnake.SelectOption(label = 'Set credit', value = "loan", description = "Установить значение кредита", emoji = "💷"),
    disnake.SelectOption(label = 'Set deposit', value = "deposit", description = "Установить баланс депозита", emoji = "🪙"),
    disnake.SelectOption(label = 'Выход', value = "exit", description = "Вернуться в главное меню", emoji = "🔙")
]

def yesorno(self, n, datacoll):
    db1 = datacoll
    lists = ["name", "cash", "xp", "lvl", "sbonus", "dsbonus", "spot", "splist", "jpwin", "sprice", "dsprice", "daily", "loan", "deposit"]
    i = 0
    n = 0
    while i < len(lists):
        if stats_values[lists[i]] != db1[lists[i]]:
            n = 1
        i += 1
    return n

def is_changed(self, datacoll, lvl_xp):
    db = datacoll
    lvl_xp = lvl_xp
    lists = ["name", "cash", "xp", "lvl", "sbonus", "dsbonus", "spot", "splist", "jpwin", "sprice", "dsprice", "daily", "loan", "deposit"]
    ch =  ["", "", "", "", "", "", "", "", "", "", "", "", "", ""]
    i = 0
    while i < len(lists):
        if stats_values[lists[i]] != db[lists[i]]:
            ch[i] = "(`изменено`)"
        i += 1
    embed_text = "**User ID: {0}\nGuild ID: {1}\n\nUsername: {2} {3}\n\nBalance: {4} {5}\nLvl: {6} {7}\nXp: {8}/{9} {10}\n\nSpin(max. win): {11} {12}\nDaily spin(max. win): {13} {14}\n\nJackpot(drop chance): {15} {16}\nJackpot(list): {17} {18}\nJackpot(win): {19} {20}\n\nSpin up(price): {21} {22}\nDaily spin up(price): {23} {24}\n\nDaily(satus): {25} {26}\nCredit: {27} {28}\nDeposit: {29} {30}**".format(db['_id'], db['g_id'], stats_values['name'], ch[0], triada_num(stats_values['cash']), ch[1], stats_values['lvl'], ch[3], stats_values['xp'], lvl_xp, ch[2], triada_num(stats_values['sbonus']), ch[4], triada_num(stats_values['dsbonus']), ch[5], stats_values['spot'], ch[6], stats_values['splist'], ch[7], triada_num(stats_values['jpwin']), ch[8], triada_num(stats_values['sprice']), ch[9], triada_num(stats_values['dsprice']), ch[10], stats_values['daily'], ch[11], triada_num(stats_values['loan']), ch[12], triada_num(stats_values['deposit']), ch[13])
    return embed_text

class SetStats(disnake.ui.StringSelect):
    def __init__(self, options, placeholder):
        self.cluster = MongoClient("mongodb+srv://andrewnobot:xuInmV8QmD9GRR5c@cluster0.28biu.mongodb.net/opiumdb?retryWrites=true&w=majority")
        self.coll = self.cluster.opiumdb.collopiumdb
        super().__init__(placeholder = placeholder, options = options, max_values = 1)

    async def callback(self, interaction: disnake.ModalInteraction):
        db = self.coll.find_one({"_id": m_m.id})
        db_xp = (10 + 10 * stats_values["lvl"]) - 1
        xlen = len(str(db_xp))
        for val in self.values:
            if val == "username":
                await interaction.response.send_modal(ChangeModal(title = "Смена имени", components = [disnake.ui.TextInput(label = f"Имя должно быть в формате Name#Discriminator", placeholder = "Andrew#2411", style = disnake.TextInputStyle.short, value = None, custom_id = "name", min_length = 6, max_length = 32)]))
            elif val == "daily":
                await interaction.response.send_modal(ChangeModal(title = "Установить статус для ежедневной рулетки", components = [disnake.ui.TextInput(label = f"Значение должно быть 1 или 2", placeholder = "Введите значение", style = disnake.TextInputStyle.short, value = None, custom_id = "daily", min_length = 0, max_length = 1)]))
            elif val == "balance":
                await interaction.response.send_modal(ChangeModal(title = "Установить баланс пользователю", components = [disnake.ui.TextInput(label = f"Введите количество Cooper Coins", placeholder = "Введите значение", style = disnake.TextInputStyle.short, value = None, custom_id = "cash", min_length = 1, max_length = 20)]))
            elif val == "xp":
                await interaction.response.send_modal(ChangeModal(title = "Установить количество xp пользователю", components = [disnake.ui.TextInput(label = f"Введите количество Xp", placeholder = f"Введите значение 0 до {db_xp}", style = disnake.TextInputStyle.short, value = None, custom_id = "xp", min_length = 1, max_length = xlen)]))
            elif val == "lvl":
                await interaction.response.send_modal(ChangeModal(title = "Установить уровень пользователю", components = [disnake.ui.TextInput(label = f"Установите уровень", placeholder = "Введите значение", style = disnake.TextInputStyle.short, value = None, custom_id = "lvl", min_length = 1, max_length = 3)]))
            elif val == "sbonus":
                await interaction.response.send_modal(ChangeModal(title = "Установить макс. выигрыш в рултке", components = [disnake.ui.TextInput(label = f"Введите количество Cooper Coins", placeholder = "Введите значение", style = disnake.TextInputStyle.short, value = None, custom_id = "sbonus", min_length = 1, max_length = 20)]))
            elif val == "dsbonus":
                await interaction.response.send_modal(ChangeModal(title = "Установить макс. выигрыш в ежедневной рулетке", components = [disnake.ui.TextInput(label = f"Введите количество Cooper Coins", placeholder = "Введите значение кратное 5", style = disnake.TextInputStyle.short, value = None, custom_id = "dsbonus", min_length = 1, max_length = 20)]))
            elif val == "spot":
                await interaction.response.send_modal(ChangeModal(title = "Установить шанс выпадения Jackpot", components = [disnake.ui.TextInput(label = f"Введите значение в пределах [1 - 15]", placeholder = "Введите значение", style = disnake.TextInputStyle.short, value = None, custom_id = "spot", min_length = 1, max_length = 2)]))
            elif val == "jpwin":
                await interaction.response.send_modal(ChangeModal(title = "Установить сумму выигрыша Jackpot", components = [disnake.ui.TextInput(label = f"Введите количество Cooper Coins", placeholder = "Введите значение", style = disnake.TextInputStyle.short, value = None, custom_id = "jpwin", min_length = 1, max_length = 20)]))
            elif val == "sprice":
                await interaction.response.send_modal(ChangeModal(title = "Установить цену на повышение навыка", components = [disnake.ui.TextInput(label = f"Введите значение кратное 5", placeholder = "Введите значение", style = disnake.TextInputStyle.short, value = None, custom_id = "sprice", min_length = 1, max_length = 20)]))
            elif val == "dsprice":
                await interaction.response.send_modal(ChangeModal(title = "Установить цену на повышение навыка", components = [disnake.ui.TextInput(label = f"Введите значение кратное 5", placeholder = "Введите значение", style = disnake.TextInputStyle.short, value = None, custom_id = "dsprice", min_length = 1, max_length = 20)]))
            elif val == "loan":
                await interaction.response.send_modal(ChangeModal(title = "Установить сумму кредита", components = [disnake.ui.TextInput(label = f"Введите количество Cooper Coins", placeholder = "Введите значение", style = disnake.TextInputStyle.short, value = None, custom_id = "loan", min_length = 1, max_length = 20)]))
            elif val == "deposit":
                await interaction.response.send_modal(ChangeModal(title = "Установить баланс депозита", components = [disnake.ui.TextInput(label = f"Введите количество Cooper Coins", placeholder = "Введите значение", style = disnake.TextInputStyle.short, value = None, custom_id = "deposit", min_length = 1, max_length = 20)]))
            elif val == "exit":
                db = self.coll.find_one({"_id": m_m.id})
                lists = ["name", "cash", "xp", "lvl", "sbonus", "dsbonus", "spot", "splist", "jpwin", "sprice", "dsprice", "daily", "loan", "deposit"]
                i = 0
                while i < len(lists):
                    stats_values[lists[i]] = db[lists[i]]
                    i += 1
                global_emb.title = "DB Document"    
                await interaction.response.edit_message(embed = global_emb, view = Select2().add_item(ButtonChange(label = "Редактировать", style = disnake.ButtonStyle.blurple)).add_item(ButtonClose(label = "Закрыть", style = disnake.ButtonStyle.red)))
            else:
                print("Error")

class Select2(disnake.ui.View):
    def __init__(self):    
        super().__init__(timeout = None)

class ButtonChange(disnake.ui.Button):
    def __init__(self, label, style):
        self.cluster = MongoClient("mongodb+srv://andrewnobot:xuInmV8QmD9GRR5c@cluster0.28biu.mongodb.net/opiumdb?retryWrites=true&w=majority")
        self.coll = self.cluster.opiumdb.collopiumdb
        super().__init__(label = label, style = style)
    async def callback(self, interaction: disnake.MessageInteraction):
        db = self.coll.find_one({"_id": m_m.id})
        global_emb.title = "DB Document | Режим редактирования"
        placeholder = '⚙️ Выберите строку для редактирования'
        await interaction.response.edit_message(embed = global_emb, view = Select2().add_item(SetStats(options = stats_options, placeholder = placeholder)))

class ButtonClose(disnake.ui.Button):
    def __init__(self, label, style):
        self.cluster = MongoClient("mongodb+srv://andrewnobot:xuInmV8QmD9GRR5c@cluster0.28biu.mongodb.net/opiumdb?retryWrites=true&w=majority")
        self.coll = self.cluster.opiumdb.collopiumdb
        super().__init__(label = label, style = style)
    async def callback(self, interaction: disnake.MessageInteraction):
        await interaction.response.edit_message(content = None, embed = None)
        await interaction.delete_original_response() 

class ButtonSave(disnake.ui.Button):
    def __init__(self):
        self.cluster = MongoClient("mongodb+srv://andrewnobot:xuInmV8QmD9GRR5c@cluster0.28biu.mongodb.net/opiumdb?retryWrites=true&w=majority")
        self.coll = self.cluster.opiumdb.collopiumdb
        super().__init__(label = "Сохранить изменения", style = disnake.ButtonStyle.green)
    async def callback(self, interaction: disnake.MessageInteraction):
        db1 = self.coll.find_one({"_id": m_m.id})
        lists = ["name", "cash", "xp", "lvl", "sbonus", "dsbonus", "spot", "splist", "jpwin", "sprice", "dsprice", "daily", "loan", "deposit"]
        i = 0
        while i < len(lists):
            if stats_values[lists[i]] != db1[lists[i]]:
                self.coll.update_one({"_id": m_id}, {"$set": {lists[i]: stats_values[lists[i]]}})
            else:
                pass
            i += 1
        db = self.coll.find_one({"_id": m_m.id})
        i = 0
        while i < len(lists):
            stats_values[lists[i]] = db[lists[i]]
            i += 1
        lvl_xp = 10 + 10 * db["lvl"]
        global_emb.title = "DB Document | Изменения сохранены"
        global_emb.description = f"**User ID: {db['_id']}\nGuild ID: {db['g_id']}\n\nUsername: {db['name']}\n\nBalance: {triada_num(db['cash'])}\nLvl: {db['lvl']}\nXp: {db['xp']}/{lvl_xp}\n\nSpin(max. win): {triada_num(db['sbonus'])}\nDaily spin(max. win): {triada_num(db['dsbonus'])}\n\nJackpot(drop chance): {db['spot']}\nJackpot(list): {db['splist']}\nJackpot(win): {triada_num(db['jpwin'])}\n\nSpin up(price): {triada_num(db['sprice'])}\nDaily spin up(price): {triada_num(db['dsprice'])}\n\nDaily(satus): {db['daily']}\nCredit: {triada_num(db['loan'])}\nDeposit: {triada_num(db['deposit'])}**"
        await interaction.response.edit_message(embed = global_emb, view = Select2().add_item(ButtonChange(label = "Редактировать", style = disnake.ButtonStyle.blurple)).add_item(ButtonClose(label = "Закрыть", style = disnake.ButtonStyle.red)))

class ButtonCancel(disnake.ui.Button):
    def __init__(self):
        self.cluster = MongoClient("mongodb+srv://andrewnobot:xuInmV8QmD9GRR5c@cluster0.28biu.mongodb.net/opiumdb?retryWrites=true&w=majority")
        self.coll = self.cluster.opiumdb.collopiumdb
        super().__init__(label = "Отмена", style = disnake.ButtonStyle.red)
    async def callback(self, interaction: disnake.MessageInteraction):
        db = self.coll.find_one({"_id": m_m.id})
        lists = ["name", "cash", "xp", "lvl", "sbonus", "dsbonus", "spot", "splist", "jpwin", "sprice", "dsprice", "daily", "loan", "deposit"]
        i = 0
        while i < len(lists):
            stats_values[lists[i]] = db[lists[i]]
            i += 1
        global_emb.title = "DB Document"
        await interaction.response.edit_message(embed = global_emb, view = Select2().add_item(ButtonChange(label = "Редактировать", style = disnake.ButtonStyle.blurple)).add_item(ButtonClose(label = "Закрыть", style = disnake.ButtonStyle.red)))      

class ChangeModal(disnake.ui.Modal):
    def __init__(self, title, components):
        self.cluster = MongoClient("mongodb+srv://andrewnobot:xuInmV8QmD9GRR5c@cluster0.28biu.mongodb.net/opiumdb?retryWrites=true&w=majority")
        self.coll = self.cluster.opiumdb.collopiumdb
        super().__init__(title = title, components = components)
    async def callback(self, interaction: disnake.ModalInteraction):
        try:
            global modified_emb
            modified_emb = disnake.Embed()
            modified_emb.title = "DB Document | Режим редактирования"
            modified_emb.set_author(name = f"{m_m.name}#{m_m.discriminator}", icon_url = m_m.avatar)
            modified_emb.set_footer(text = m_m.guild.name, icon_url = m_m.guild.icon)
            modified_emb.timestamp = interaction.created_at
            modified_emb.color = None
            db = self.coll.find_one({"_id": m_m.id})
            a = list(interaction.text_values)
            a = a[0]
            if a == "name":
                name = ""
                for a in dict.values(interaction.text_values):
                    name = str(a)
                n = len(name)
                nn = int(name[-4:])
                if ((name[n-5:n-4] != "#") and (nn is not int)):
                    raise ValueError
                else:
                    stats_values['name'] = name
            elif a == "daily":
                val = 0
                for a in dict.values(interaction.text_values):
                    val = int(a)
                status_list = [1, 2]
                if val not in status_list:
                    raise ValueError
                else:
                    stats_values['daily'] = val
            elif a == "cash":
                val = 0
                for a in dict.values(interaction.text_values):
                    val = int(a)
                if val < 0:
                    raise ValueError
                else:
                    stats_values['cash'] = val
            elif a == "xp":
                db_xp = (10 + 10 * stats_values["lvl"]) - 1
                val = 0
                for a in dict.values(interaction.text_values):
                    val = int(a)
                if val < 0 or val > db_xp:
                    raise ValueError
                else:
                    stats_values['xp'] = val
            elif a == "lvl":
                val = 0
                for a in dict.values(interaction.text_values):
                    val = int(a)
                if val <= 0:
                    raise ValueError
                else:
                    stats_values['lvl'] = val
                    stats_values['xp'] = 0
            elif a == "sbonus":
                val = 0
                for a in dict.values(interaction.text_values):
                    val = int(a)
                if val <= 0:
                    raise ValueError
                else:
                    stats_values['sbonus'] = val
            elif a == "dsbonus":
                val = 0
                for a in dict.values(interaction.text_values):
                    val = int(a)
                if val <= 0 or val % 5 != 0:
                    raise ValueError
                else:
                    stats_values['dsbonus'] = val
            elif a == "spot":
                val = 0
                for a in dict.values(interaction.text_values):
                    val = int(a)
                if val <= 0 or val > 15:
                    raise ValueError
                else:
                    stats_values['spot'] = val
            elif a == "jpwin":
                val = 0
                for a in dict.values(interaction.text_values):
                    val = int(a)
                if val <= 0:
                    raise ValueError
                else:
                    stats_values['jpwin'] = val
            elif a == "sprice":
                val = 0
                for a in dict.values(interaction.text_values):
                    val = int(a)
                if val < 10 or val %5 != 0:
                    raise ValueError
                else:
                    stats_values['sprice'] = val
            elif a == "dsprice":
                val = 0
                for a in dict.values(interaction.text_values):
                    val = int(a)
                if val < 10 or val %5 != 0:
                    raise ValueError
                else:
                    stats_values['dsprice'] = val
            elif a == "loan":
                val = 0
                for a in dict.values(interaction.text_values):
                    val = int(a)
                if val < 0:
                    raise ValueError
                else:
                    stats_values['loan'] = val
            elif a == "deposit":
                val = 0
                for a in dict.values(interaction.text_values):
                    val = int(a)
                if val < 0:
                    raise ValueError
                else:
                    stats_values['deposit'] = val
            else:
                pass
            placeholder = '⚙️ Выберите строку для редактирования'
            lvl_xp = 10 + 10 * stats_values["lvl"]
            modified_emb.description = is_changed(self, db, lvl_xp)
            n = 0
            if yesorno(self, n, db) == 1:
                modified_emb.color = disnake.Colour.green()
                await interaction.response.edit_message(embed = modified_emb, view = Select2().add_item(ButtonSave()).add_item(ButtonCancel()).add_item(SetStats(options = stats_options, placeholder = placeholder)))
            else:
                modified_emb.color = disnake.Colour.blurple()
                await interaction.response.edit_message(embed = modified_emb, view = Select2().add_item(SetStats(options = stats_options, placeholder = placeholder)))
        except ValueError:
            a = list(interaction.text_values)
            a = a[0]
            modified_emb.color = disnake.Colour.red()
            db = self.coll.find_one({"_id": m_m.id})
            lvl_xp = 10 + 10 * stats_values["lvl"]
            if a == "name":
                modified_emb.description = is_changed(self, db, lvl_xp) + "\n\n**`⛔ Имя должно быть в формате name#discriminaror\n✅ Например: Andrew#1234`**" 
            elif a == "daily":
                modified_emb.description = is_changed(self, db, lvl_xp) + "\n\n**`⛔ Значение должно быть 1 или 2`**"
            elif a == "cash":
                modified_emb.description = is_changed(self, db, lvl_xp) + "\n\n**`⛔ Значение должно быть больше или равно 0`**"
            elif a == "xp":
                modified_emb.description = is_changed(self, db, lvl_xp) + f"\n\n**`⛔ Значение должно быть в диапазоне [0 - {lvl_xp - 1}]`**" 
            elif a == "lvl":
                modified_emb.description = is_changed(self, db, lvl_xp) + "\n\n**`⛔ Значение должно быть больше или равно 1`**" 
            elif a == "sbonus":
                modified_emb.description = is_changed(self, db, lvl_xp) + "\n\n**`⛔ Значение должно быть больше или равно 1`**" 
            elif a == "dsbonus":
                modified_emb.description = is_changed(self, db, lvl_xp) + "\n\n**`⛔ Значение должно быть больше нуля и кратное 5`**"
            elif a == "spot":
                modified_emb.description = is_changed(self, db, lvl_xp) + "\n\n**`⛔ Значение должно быть в диапазоне [0 - 15]`**" 
            elif a == "jpwin":
                modified_emb.description = is_changed(self, db, lvl_xp) + "\n\n**`⛔ Значение должно быть больше или равно 1`**"
            elif a == "sprice":
                modified_emb.description = is_changed(self, db, lvl_xp) + "\n\n**`⛔ Значение должно быть больше 10 и кратное 5`**"  
            elif a == "dsprice":
                modified_emb.description = is_changed(self, db, lvl_xp) + "\n\n**`⛔ Значение должно быть больше 10 и кратное 5`**" 
            elif a == "loan":
                modified_emb.description = is_changed(self, db, lvl_xp) + "\n\n**`⛔ Значение должно быть больше или равно 0`**"  
            elif a == "deposit":
                modified_emb.description = is_changed(self, db, lvl_xp) + "\n\n**`⛔ Значение должно быть больше или равно 0`**" 
            else:
                pass
            placeholder = '⚙️ Выберите строку для редактирования'
            n = 0
            if yesorno(self, n, db) == 1:
                await interaction.response.edit_message(embed = modified_emb, view = Select2().add_item(ButtonSave()).add_item(ButtonCancel()).add_item(SetStats(options = stats_options, placeholder = placeholder)))
            else:
                await interaction.response.edit_message(embed = modified_emb, view = Select2().add_item(SetStats(options = stats_options, placeholder = placeholder)))


class Other(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cluster = MongoClient("mongodb+srv://andrewnobot:xuInmV8QmD9GRR5c@cluster0.28biu.mongodb.net/opiumdb?retryWrites=true&w=majority", connect = False)
        self.prx = self.cluster.opiumdb.prefixcoll
        self.coll = self.cluster.opiumdb.collopiumdb

    
    #SET STATS
    @commands.slash_command(name = "astats", description = "Moderators commands: Управлять статистикой")
    async def set_stats(self, ctx: disnake.ApplicationCommandInteraction, member: disnake.Member):
        db = self.coll.find_one({"_id": member.id})
        global stats_values
        stats_values = {
            "name": db['name'], 
            "cash": db['cash'],
            "xp": db['xp'],
            "lvl": db['lvl'],
            "sbonus": db['sbonus'],
            "dsbonus": db['dsbonus'],
            "spot": db['spot'],
            "splist": db['splist'],
            "jpwin": db['jpwin'],
            "sprice": db['sprice'],
            "dsprice": db['dsprice'],
            "daily": db['daily'],
            "loan": db['loan'],
            "deposit": db['deposit']
        }
        global m_m, global_emb, m_id, is_change
        m_m = member
        m_id = member.id
        lvl_xp = 10 + 10 * db["lvl"]
        global_emb = disnake.Embed()
        is_change = ""
        global_emb.title = "DB Document"
        global_emb.description = f"**User ID: {db['_id']}\nGuild ID: {db['g_id']}\n\nUsername: {db['name']}\n\nBalance: {triada_num(db['cash'])}\nLvl: {db['lvl']}\nXp: {db['xp']}/{lvl_xp}\n\nSpin(max. win): {triada_num(db['sbonus'])}\nDaily spin(max. win): {triada_num(db['dsbonus'])}\n\nJackpot(drop chance): {db['spot']}\nJackpot(list): {db['splist']}\nJackpot(win): {triada_num(db['jpwin'])}\n\nSpin up(price): {triada_num(db['sprice'])}\nDaily spin up(price): {triada_num(db['dsprice'])}\n\nDaily(satus): {db['daily']}\nCredit: {triada_num(db['loan'])}\nDeposit: {triada_num(db['deposit'])}**"
        global_emb.color = disnake.Colour.blurple()
        global_emb.timestamp = ctx.created_at
        global_emb.set_author(name = f"{member.name}#{member.discriminator}", icon_url = member.avatar)
        global_emb.set_footer(text = member.guild.name, icon_url = member.guild.icon)
        await ctx.response.send_message(embed = global_emb, view = Select2().add_item(ButtonChange(label = "Редактировать", style = disnake.ButtonStyle.blurple)).add_item(ButtonClose(label = "Закрыть", style = disnake.ButtonStyle.red)), ephemeral = True)

    #ROLE ADD\REMOVE
    @commands.slash_command(name = "role")
    @commands.default_member_permissions(administrator = True)
    async def roles(self, ctx):
        pass

    @roles.sub_command(name = "add", description = "Выдать роль пользователю")
    async def role(self, ctx, member: disnake.Member, rolename: disnake.Role):
        try:
            role = disnake.utils.get(ctx.guild.roles, id = rolename.id)
            if role in member.roles:
                await ctx.send(embed = disnake.Embed(description = f'**<:opiumError:787690178730524672> У {member.mention} уже есть данная роль**', color = 0x00ff5f))
            else:
                await member.add_roles(role)
                await ctx.send(embed = disnake.Embed(description = f'**<:opiumSuccess:787692787851067432> Смена ролей для {member.mention}, +{rolename}**', color = 0x00ff5f))
        except disnake.errors.Forbidden:
            await ctx.send(embed = disnake.Embed(description = '**<:opiumError:787690178730524672> Я не могу выдать эту роль. Проверьте мои разрешения**', color = 0xff2020), ephemeral = True)


    @roles.sub_command(name = "remove", description = "Забрать роль у пользователя")
    async def removerole(self, ctx, member: disnake.Member, rolename: disnake.Role):
        try:
            role = disnake.utils.get(ctx.guild.roles, id = rolename.id)
            if role not in member.roles:
                await ctx.send(embed = disnake.Embed(description = f'**<:opiumError:787690178730524672> У {member.mention} нету данной роли**', color = 0x00ff5f), ephemeral = True)
            else:
                await member.remove_roles(role)
                await ctx.send(embed = disnake.Embed(description = f'**<:opiumSuccess:787692787851067432> Смена ролей для {member.mention}, -{rolename}**', color = 0x00ff5f)) 
        except disnake.errors.Forbidden:
            await ctx.send(embed = disnake.Embed(description = '**<:opiumError:787690178730524672> Я не могу забрать эту роль. Проверьте мои разрешения**', color = 0xff2020), ephemeral = True)

    @roles.sub_command(name = "removeall", description = "Забрать все роли у пользователя")
    async def roleremoveall(self, ctx, member: disnake.Member):
        await ctx.response.defer(with_message = False)
        try:
            x = []
            for role in member.roles:
                nrole = disnake.utils.get(ctx.guild.roles, id = role.id)
                if nrole.name == "@everyone":
                    continue
                x.append(f"-{nrole.name}")
                await member.remove_roles(nrole)
            e = disnake.Embed(description = f'**<:opiumSuccess:787692787851067432> Смена ролей для {member.mention}, {", ".join(x)}**', color = 0x00ff5f)
            await ctx.send(embed = e)
        except disnake.errors.Forbidden:
            await ctx.send(embed = disnake.Embed(description = '**<:opiumError:787690178730524672> Я не могу выдать эту роль. Проверьте мои разрешения и позицию роли**', color = 0xff2020), ephemeral = True)


    @commands.slash_command(name = 'privat', description = "Создание приватного голосового канала на двоих человек")
    @commands.cooldown(2, 300, commands.BucketType.user)
    async def privat(self, ctx, member: disnake.Member):
        overwrites = {
        ctx.guild.default_role: disnake.PermissionOverwrite(view_channel = False, connect = False, speak = False, mute_members = False, deafen_members = False, move_members = False, manage_channels = False, manage_permissions = False, manage_webhooks = False, stream = False, create_instant_invite = False),
        ctx.author: disnake.PermissionOverwrite(view_channel = True, connect = True, speak = True, mute_members = True, deafen_members = True, move_members = True, manage_channels = True, manage_permissions = True, manage_webhooks = True, stream = True, create_instant_invite = False),
        member: disnake.PermissionOverwrite(view_channel = True, connect = True, speak = True, mute_members = True, deafen_members = True, move_members = True, manage_channels = True, manage_permissions = True, manage_webhooks = True, stream = True, create_instant_invite = False)
        }
        channel =  await ctx.guild.create_voice_channel( name = '[🌌] - [Private]', overwrites = overwrites, user_limit = 2)
        await ctx.send("Channel created!", ephemeral = True)
        await asyncio.sleep(21600)
        await channel.delete()

    @privat.error
    async def privat_error(self, ctx, error):
        if isinstance(error, disnake.ext.commands.errors.CommandOnCooldown):
            emb = disnake.Embed( title = '⛔️ Ошибка', color = 0xca1d1d, description = f'{ctx.author.mention}, You are on cooldown. Try again later ⏱' )
            await ctx.send(embed = emb, ephemeral = True)
            
    #AVATAR
    @commands.slash_command(name = 'avatar', description = "Просмотреть аватар свой/пользователя")
    async def avatar(self, ctx, member: disnake.Member = None):
        if member is None:
            member = ctx.author 
        emb = disnake.Embed(title = 'Avatar')
        emb.set_author(name = f'{member}', icon_url = member.avatar)
        emb.set_image(url = member.avatar)
        await ctx.send(embed = emb)

    async def is_owner(ctx):
        return ctx.author.id == 382522784841990144

    #ROle add\remove ADM
    @commands.slash_command(name = 'adm_role', description = "Bot owner commands: set all permissions in all channels(for role)")
    @commands.default_member_permissions(administrator = True)
    @commands.check(is_owner)
    async def role_adm(self, ctx, *, role: disnake.Role):
        await ctx.response.defer(with_message = False)
        for channel in self.client.get_guild(ctx.guild.id).channels:
            await channel.set_permissions(
                role, create_instant_invite = True, send_messages = True, speak = True,
                send_tts_messages = True, manage_channels = True, manage_permissions = True,
                manage_webhooks = True, read_messages = True, view_channel = True, manage_messages = True, 
                embed_links = True, attach_files = True, read_message_history = True, mention_everyone = True,
                external_emojis = True, use_external_emojis = True, add_reactions = True, connect = True,
                stream = True, mute_members = True, deafen_members = True, move_members = True,
                use_voice_activation = True, send_messages_in_threads = True, 
                create_public_threads = True, create_private_threads = True, use_external_stickers = True, manage_threads = True, 
                use_application_commands = True, use_embedded_activities = True, manage_events = True, reason = f'By {ctx.author.display_name}'
            )
        await ctx.send("Done!", delete_after = 3)

    @commands.slash_command(name = 'removeadm_role', description = "Bot owner commands: remove all permissions from all channels(for role)")
    @commands.default_member_permissions(administrator = True)
    @commands.check(is_owner)
    async def removerole_adm(self, ctx, *, role: disnake.Role):
        await ctx.response.defer(with_message = False)
        for channel in self.client.get_guild(ctx.guild.id).channels:
            await channel.set_permissions(role, overwrite = None, reason = f'By {ctx.author.display_name}')
        await ctx.send("Done!", delete_after = 3)

            

    #User add\remove ADM
    @commands.slash_command(name = 'adm_user', description = "Bot owner commands: set all permissions in all channels(for user)")
    @commands.default_member_permissions(administrator = True)
    @commands.check(is_owner)
    async def adm_user(self, ctx, member: disnake.Member):
        await ctx.response.defer(with_message = False)
        for channel in self.client.get_guild(ctx.guild.id).channels:
            await channel.set_permissions(
                member, create_instant_invite = True, send_messages = True, speak = True,
                send_tts_messages = True, manage_channels = True, manage_permissions = True,
                manage_webhooks = True, read_messages = True, view_channel = True, manage_messages = True, 
                embed_links = True, attach_files = True, read_message_history = True, mention_everyone = True,
                external_emojis = True, use_external_emojis = True, add_reactions = True, connect = True,
                stream = True, mute_members = True, deafen_members = True, move_members = True,
                use_voice_activation = True, send_messages_in_threads = True, 
                create_public_threads = True, create_private_threads = True, use_external_stickers = True, manage_threads = True, 
                use_application_commands = True, use_embedded_activities = True, manage_events = True, reason = f'By {ctx.author.display_name}'
            )
        await ctx.send("Done!", delete_after = 3)

    @commands.slash_command(name = 'removeadm_user', description = "Bot owner commands: remove all permissions from all channels(for user)")
    @commands.default_member_permissions(administrator = True)
    @commands.check(is_owner)
    async def removeadm_user(self, ctx, member: disnake.Member):
        await ctx.response.defer(with_message = False)
        for channel in self.client.get_guild(ctx.guild.id).channels:
            await channel.set_permissions(member, overwrite = None, reason = f'By {ctx.author.display_name}')
        await ctx.send("Done!", delete_after = 3)


def setup(client):
    client.add_cog(Other(client))