import discord
from discord.ext import commands, tasks
import sqlite3

from cogs.currency.interest import InterestHandler
from cogs.currency.currency_db_handler import Database as db

class Currency(commands.Cog):
    '''
    cog que lida com comandos relacionado com dinheiro
    '''
    def __init__(self, bot):
        self.db_path = 'cogs/currency/currency.db'
        self.bot = bot
        self.db = db(self.db_path)

        self.interest_task_loop.start()

    @tasks.loop(hours=12)
    async def interest_task_loop(self):
        print('Checando interesse...')
        interest = InterestHandler(self.db_path)
        interest.add_intrest_if_one_day_is_passed()
    
    @staticmethod
    def is_me(ctx):
        return ctx.message.author.id == 226524214411132928

    def is_account_number_valid(self, account_number):
        if len(str(account_number)) == 2 and account_number > 0:
            return True
        else:
            return False

    def is_user_in_db(self, ctx):
        uid = self.get_uid(ctx)
        cursor = self.db.fetch_one_by_uid(uid)

        if cursor is not None:
            return True
        else:
            return False

    def is_account_number_in_db(self, account_number):
        cursor = self.db.fetch_one_by_account_num(account_number)
        if cursor is not None:
            return True
        else:
            return False

    def is_join_valid(self, ctx, account_number):

        if self.is_user_in_db(ctx):
            raise Exception("Usuário já registrado.")

        elif self.is_account_number_in_db(account_number):
            raise Exception("Número da conta já registrado.")
        
        elif not self.is_account_number_valid(account_number):
            raise Exception("Número da conta inválido, deve ser um número inteiro entre 10 e 99.")
        
        else: 
            return True
        
    def is_transfer_valid(self, ctx, account_number, amount):
        if not self.is_user_in_db(ctx):
            raise Exception("É preciso ter uma conta para fazer um trasnferência")

        elif not self.is_account_number_in_db(account_number):
            raise Exception("Conta de transferência não registrada.")

        elif self.db.fetch_money_by_uid(self.get_uid(ctx)) < amount:
            raise Exception("Quantidade de dinheiro insuficiente.")
        
        elif amount <= 0:
            raise Exception("Quantidade de dinheiro inválida.")
        
        else:
            return True

    def get_uid(self, ctx) -> int:
        return int(ctx.message.author.id)

    def get_author_name(self, ctx) -> str:
        return str(ctx.message.author.name)


    def is_message_public(self, ctx):
        if ctx.message.guild is not None:
            return True
        else:
            return False
        
    @commands.command()
    async def join(self, ctx, account_number: int):
        if self.is_join_valid(ctx, account_number):
            uid = self.get_uid(ctx)
            name = self.get_author_name(ctx)

            self.db.create_and_commit_db_entry(uid, account_number, name)
            await ctx.send(f'Conta criada com o número {account_number}! Bem vindo ao Nubas!')

    @commands.command()
    async def saldo(self, ctx):
        if self.is_user_in_db(ctx):
            await ctx.send(f'Você tem {self.db.fetch_money_by_uid(self.get_uid(ctx)):.2f} na sua conta :moneybag:')

        else:
            raise Exception("Conta não registrada.")

    @commands.command()
    @commands.check(is_me)
    async def showdb(self, ctx):
        cursor = self.db.fetch_whole_database()
        for row in cursor:
            await ctx.message.author.send(row)

    @commands.command()
    async def dix(self, ctx, account_number: int, amount: float):
        if self.is_transfer_valid(ctx, account_number, amount):
            self.db.transfer_money(self.get_uid(ctx), account_number, amount)
            await ctx.send(f'{amount} Transferidos para a conta {account_number}')

    @commands.command()
    async def lst(self, ctx):
        account_and_names = zip(self.db.fetch_all_accounts(), self.db.fetch_all_names())

        names_in_code = ''
        for account, name in account_and_names:
            names_in_code += '```' + f'{account} >>> {name}' + '```'

        await ctx.message.author.send('Pessoas que tem contas: ' + names_in_code)


    @commands.command()
    @commands.check(is_me)
    async def add(self, ctx, account_number: int, amount: float):
        if self.is_account_number_in_db(account_number):
            self.db.add_money_in_account(amount, account_number)
            await ctx.send(f"{amount} adicionado a conta {account_number}.")
        
        else:
            raise Exception('Conta não existe.')
        
