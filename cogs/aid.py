import disnake
from disnake.ext import commands
import os
import asyncio
import pymongo
from pymongo import MongoClient
from main import autocomp_adm_command
from main import autocomp_command

set_options1 = [
    disnake.SelectOption(label = '/set lang', value = "LANG", description = "Установить языы для Big-dick game", emoji = "👨🏼"),
    disnake.SelectOption(label = '/set channel', value = "CHANNEL", description = "Установить канал для Big-dick game", emoji = "👨🏼"),
    disnake.SelectOption(label = '/set nick', value = "NICK", description = "Сменить ник пользователю", emoji = "🖊️"),
    disnake.SelectOption(label = '/set balance', value = "BALANCE", description = "Economy: Установить баланс пользователю", emoji = "💰"),
    disnake.SelectOption(label = '/set lvl', value = "LVL", description = "Economy: Установить уровень пользователю", emoji = "💰"),
    disnake.SelectOption(label = '/set log-channel', value = "LOG-CHANNEL", description = "Установить канал для логов", emoji = "📕"),
    disnake.SelectOption(label = '/set welcome-channel', value = "WELCOME-CHANNEL", description = "Установить приветственный канал", emoji = "🖐️")
]

set_options = [
    disnake.SelectOption(label = '/set lang', value = "LANG", description = "Установить языы для Big-dick game", emoji = "👨🏼"),
    disnake.SelectOption(label = '/set channel', value = "CHANNEL", description = "Установить канал для Big-dick game", emoji = "👨🏼"),
    disnake.SelectOption(label = '/set nick', value = "NICK", description = "Сменить ник пользователю", emoji = "🖊️"),
    disnake.SelectOption(label = '/set balance', value = "BALANCE", description = "Economy: Установить баланс пользователю", emoji = "💰"),
    disnake.SelectOption(label = '/set lvl', value = "LVL", description = "Economy: Установить уровень пользователю", emoji = "💰"),
    disnake.SelectOption(label = '/set log-channel', value = "LOG-CHANNEL", description = "Установить канал для логов", emoji = "📕"),
    disnake.SelectOption(label = '/set welcome-channel', value = "WELCOME-CHANNEL", description = "Установить приветственный канал", emoji = "🖐️"),
    disnake.SelectOption(label = 'Выход', value = "EXIT", description = "Вернуться на главную страницу", emoji = "🔙")
]

class SelectMenu(disnake.ui.Select):
    def __init__(self, options, placeholder):
        super().__init__(placeholder = placeholder, options = options, max_values = 1)
    async def callback(self, interaction: disnake.Interaction):
        for val in self.values:
            if val == "LANG":
                emb = disnake.Embed(title = "Command: /set lang", description = "**Описание**: Установить язык для Big-gick game\n**Cooldown**: None\n**Использование:**\n/set lang [Українська/Русский]\n**Пример:**\n/set lang Українська\n/set lang Русский", color = 0x40d406)
                await interaction.response.edit_message(embed = emb, view = Select().add_item(SelectMenu(options = set_options, placeholder = "👨🏼 /set lang")))
            elif val == 'CHANNEL':
                emb = disnake.Embed(title = "Command: /set channel", description = "**Описание**: Установить канал для Big-gick game\n**Cooldown**: None\n**Использование:**\n/set channel [TextChannel]\n**Пример:**\n/set channel #big-dick-game", color = 0x40d406)
                await interaction.response.edit_message(embed = emb, view = Select().add_item(SelectMenu(options = set_options, placeholder = "👨🏼 /set channel")))
            elif val == 'NICK':
                emb = disnake.Embed(title = "Command: /set nick", description = "**Описание**: Сменить ник нейм пользователю\n**Cooldown**: None\n**Использование:**\n/set nick [member] [NickName]\n**Примечание:** Никнейм должен быть длиной от 1 до 32 символов\n**Пример:**\n/set nick @cooper#0001 anthony cooper", color = 0x40d406)
                await interaction.response.edit_message(embed = emb, view = Select().add_item(SelectMenu(options = set_options, placeholder = "🖊️ /set nick")))
            elif val == 'BALANCE':
                emb = disnake.Embed(title = "Command: /set balance", description = "**Категория:** Economy\n**Описание**: Установить баланс пользователю\n**Cooldown**: None\n**Использование:**\n/set balance [member] [amount]\n**Пример:**\n/set balance @cooper#0001 500", color = 0x40d406)
                await interaction.response.edit_message(embed = emb, view = Select().add_item(SelectMenu(options = set_options, placeholder = "💰 /set balance")))
            elif val == 'LVL':
                emb = disnake.Embed(title = "Command: /set lvl", description = "**Категория:** Economy\n**Описание**: Установить уровень пользователю\n**Cooldown**: None\n**Использование:**\n/set lvl [member] [lvl]\n**Пример:**\n/set lvl @cooper#0001 12", color = 0x40d406)
                await interaction.response.edit_message(embed = emb, view = Select().add_item(SelectMenu(options = set_options, placeholder = "💰 /set lvl")))
            elif val == 'LOG-CHANNEL':
                emb = disnake.Embed(title = "Command: /set log-channel", description = "**Описание**: Установить канал для логов\n**Cooldown**: None\n**Использование:**\n/set log-channel [TextChannel]\n**Пример:**\n/set log-channel #log-channel", color = 0x40d406)
                await interaction.response.edit_message(embed = emb, view = Select().add_item(SelectMenu(options = set_options, placeholder = "📕 /set log-channel")))
            elif val == 'WELCOME-CHANNEL':
                emb = disnake.Embed(title = "Command: /set welcome-channel", description = "**Описание**: Установить приветственный канал\n**Cooldown**: None\n**Использование:**\n/set welcome-channel [TextChannel]\n**Пример:**\n/set welcome-channel #welcome", color = 0x40d406)
                await interaction.response.edit_message(embed = emb, view = Select().add_item(SelectMenu(options = set_options, placeholder = "🖐️ /set welcome-channel")))
            elif val == 'EXIT':
                emb = disnake.Embed(title = "Command: /set", description = f'**⬇️ Выберите нужную команду ⬇️**', color = 0x40d406)
                await interaction.response.edit_message(embed = emb, view = Select().add_item(SelectMenu(options = set_options1, placeholder = "🔎 View subcommands")))
            else:
                pass

class Select(disnake.ui.View):
    def __init__(self):
        super().__init__()

class Aid(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cluster = MongoClient("mongodb+srv://andrewnobot:xuInmV8QmD9GRR5c@cluster0.28biu.mongodb.net/opiumdb?retryWrites=true&w=majority", connect = False)
        self.prx = self.cluster.opiumdb.prefixcoll

    #ON MESSAGE
    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            prefix = self.prx.find_one({"_id": message.guild.id})["prefix"]
            if message.author == self.client.user:
                return
            if message.content.startswith('$help$'):
                await message.delete()
                emb = disnake.Embed(description = '**Help: [Support Server](https://discord.gg/sWHrXQT)\nAdd Opium: [Invite Opium to your Server](https://discord.com/api/oauth2/authorize?client_id=722921602026700861&permissions=8&scope=bot)**\n**Помощь по команде: {}help [имя_команды]**'.format(prefix))
                emb.set_author(name = f"Префикс на {message.guild.name} =  ' {prefix} '", icon_url = message.guild.icon)
                await message.author.send(embed = emb)
            if message.content.startswith('prefix'):
                await message.channel.send(f'**Prefix on {message.guild.name}: `{prefix}`**')
        except AttributeError:
            pass

    #HELP
    @commands.slash_command(name = "help", description = 'Помощь по команде')
    async def help_command(self, ctx: disnake.ApplicationCommandInteraction, command_name: str = commands.Param(autocomplete = autocomp_command)):
        if command_name == "set":
            pass

    #MODERATORS HELP
    @commands.slash_command(name = "help_admin", description = "Помощь по командам для администраторов")
    @commands.default_member_permissions(administrator = True)
    async def help_admin_command(self, ctx: disnake.ApplicationCommandInteraction, command_name: str = commands.Param(autocomplete = autocomp_adm_command)):
        if command_name == "set":
            emb = disnake.Embed(title = "Command: /set", description = f'**⬇️ Выберите нужную команду ⬇️**', color = 0x40d406)
            placeholder = "🔎 View subcommands"
            await ctx.response.send_message(embed = emb, view = Select().add_item(SelectMenu(options = set_options1, placeholder = placeholder)), ephemeral = True)           

def setup(client):
    client.add_cog(Aid(client))