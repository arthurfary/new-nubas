import discord
from discord.ext import commands, tasks
from discord.ext.commands.converter import MemberConverter
import sqlite3

class Currency(commands.Cog):
    '''
    cog que lida com comandos relacionado com dinheiro
    '''
    def __init__(self, bot):
        self.bot = bot

        # NEE TO ADD CONN TO ALL FUNTIOPNS
        conn = sqlite3.connect('currency.db')

        
        '''
        conn.execute('DROP TABLE users')
        conn.commit()
        exit()

        '''
        # create in first execution
        conn.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY,
             account INTAGER NOT NULL,
             name TEXT NOT NULL,
             money INTEGER NOT NULL);''')

        conn.close()
        
    def get_uid(self, ctx) -> int:
        '''
        Retorna User Id em string
        '''
        return int(ctx.message.author.id)

    def is_message_public(self, ctx):
        if ctx.message.guild is not None:
            return True
        else:
            return False
        
    @commands.command()
    async def join(self, ctx, account_number: int):
        if self.is_message_public(ctx):
            await ctx.send('Join o que meu se é besta? ta acontecendo nd n!')

        if len(str(account_number)) != 2 or account_number < 0:
            await ctx.message.author.send(f'Conta invalida: {account_number}')
            return

        # # # # #
        uid = self.get_uid(ctx)
        conn = sqlite3.connect('currency.db')

        cursor = conn.execute("SELECT * from users WHERE id=?", (uid,))

        if cursor.fetchone() is not None:
            await ctx.message.author.send('Se ja tem conta caraio')
            return 

        else:
            conn.execute("INSERT INTO users (id, account, name, money) VALUES (?, ?, ?, ?)", (uid, account_number, ctx.message.author.name, 0))
            conn.commit()

            await ctx.message.author.send('Te adicionei ao esquema, mas deixa baixo :shushing_face:')

        cursor.close()
        conn.close()

    @commands.command()
    async def saldo(self, ctx):
        if self.is_message_public(ctx):
            await ctx.send('SALDO DO QUE MANO SALDO DO QUE????')
            await ctx.message.author.send('NÃO MANDA ESSAS COISA EM LUGAR PUBLICO MEU, TA PIXURUCO?????')

        # # # # #
        uid = self.get_uid(ctx)
        conn = sqlite3.connect('currency.db')

        cursor = conn.execute("SELECT * from users WHERE id=?", (uid,))

        row = cursor.fetchone()

        if row is None:
            await ctx.message.author.send('Se n tem conta nao besta')
            return 
        else:
            money = row[3]
            await ctx.message.author.send(f'Você tem {money} na sua conta :moneybag:')

        cursor.close()
        conn.close()
    
    @commands.command()
    async def showdb(self, ctx):
        if ctx.author.id == 226524214411132928:
            conn = sqlite3.connect('currency.db')
            cursor = conn.execute("SELECT * from users")

            for row in cursor:
                await ctx.message.author.send(row)

        
    @commands.command()
    async def dix(self, ctx, account_number: int, amount: int):
        if self.is_message_public(ctx):
            await ctx.send('Eu LITERALMENTE não tenho ideia o que é um dix??')
            await ctx.message.author.send('CARAMBOLAS MEU CARAMBOLAS O CARA QUER MANDAR PIX NO PUBLICO\nFICA ESPERTO MANO FICA')
        
        ## checks 
        uid = self.get_uid(ctx)
        conn = sqlite3.connect('currency.db')


        cursor = conn.execute("SELECT * from users WHERE id=?", (uid,))
        sender_row = cursor.fetchone()
        cursor.close()

        cursor = conn.execute("SELECT * from users WHERE account=?", (account_number,))
        reciever_row = cursor.fetchone()
        cursor.close()

        reciever_money = reciever_row[3]
        sender_money = sender_row[3]

        # check if sender account exists

        if sender_row is None:
            await ctx.message.author.send('Voce não tem conta')
            cursor.close()
            return

        # check if recipient account exists

        if reciever_row is None:
            await ctx.message.author.send('Conta não encontrada na db')
            cursor.close()
            return

        #

        if amount < 0:
            await ctx.message.author.send('Dinheiro inválido!')
            cursor.close()
            return

        if sender_money < amount:
            await ctx.message.author.send('Não tem dinheiro suficiente!')
            cursor.close()
            return

        ## END OF CHECKS
        # sends the money

        conn.execute('UPDATE users SET money = ? WHERE id = ?', (sender_money - amount, uid))
        conn.execute('UPDATE users SET money = ? WHERE account = ?', (reciever_money + amount, account_number))

        await ctx.message.author.send('Transferido.')

        conn.commit()
        conn.close()

    @commands.command()
    async def lst(self, ctx):

        if self.is_message_public(ctx):
            await ctx.send('lista ? de que ?')
            await ctx.message.author.send('tu quer que peguem a gente memo ne?')

        # # # # #
        uid = self.get_uid(ctx)
        conn = sqlite3.connect('currency.db')


        cursor = conn.execute("SELECT account, name from users")
        rows = cursor.fetchall()

        names_in_code = ''
        for row in rows:
            names_in_code += '```' + f'{row[0]} >>> {row[1]}' + '```'


        #
        await ctx.message.author.send('Pessoas que tem contas: ' + names_in_code)

        cursor.close()
        conn.close()

    @commands.command()
    async def add(self, ctx, account_number: int, amount: int):
        # my id
        if ctx.author.id == 226524214411132928:
            conn = sqlite3.connect('currency.db')

            cursor = conn.execute("SELECT money from users WHERE account=?", (account_number,))
            money_str = cursor.fetchone()[0]

            conn.execute('UPDATE users SET money = ? WHERE account = ?', (money_str + amount, account_number))
            conn.commit()
            conn.close()

            await ctx.send("Atualizado.")
        else:
            return