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

        self.conn = sqlite3.connect('example.db')
        
        '''
        self.conn.execute('DROP TABLE users')
        self.conn.commit()
        exit()

        '''
        # create in first execution
        self.conn.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY,
             account INTAGER NOT NULL,
             name TEXT NOT NULL,
             money INTEGER NOT NULL);''')
        
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

        cursor = self.conn.execute("SELECT * from users WHERE id=?", (uid,))

        if cursor.fetchone() is not None:
            await ctx.message.author.send('Se ja tem conta caraio')
            return 

        else:
            self.conn.execute("INSERT INTO users (id, account, name, money) VALUES (?, ?, ?, ?)", (uid, account_number, ctx.message.author.name, 0))
            self.conn.commit()

            await ctx.message.author.send('Te adicionei ao esquema, mas deixa baixo :shushing_face:')

        cursor.close()

    @commands.command()
    async def saldo(self, ctx):
        if self.is_message_public(ctx):
            await ctx.send('SALDO DO QUE MANO SALDO DO QUE????')
            await ctx.message.author.send('NÃO MANDA ESSAS COISA EM LUGAR PUBLICO MEU, TA PIXURUCO?????')

        # # # # #
        uid = self.get_uid(ctx)

        cursor = self.conn.execute("SELECT * from users WHERE id=?", (uid,))

        row = cursor.fetchone()

        if row is None:
            await ctx.message.author.send('Se n tem conta nao besta')
            return 
        else:
            money = row[2]
            await ctx.message.author.send(f'Você tem {money} na sua conta :moneybag:')

        cursor.close()
    
    @commands.command()
    async def showdb(self, ctx):
        cursor = self.conn.execute("SELECT * from users")

        for row in cursor:
            await ctx.message.author.send(row)

    @commands.command()
    async def dix(self, ctx, account_number):
        if self.is_message_public(ctx):
            await ctx.send('Eu LITERALMENTE não tenho ideia o que é um dix??')
            await ctx.message.author.send('CARAMBOLAS MEU CARAMBOLAS O CARA QUER MANDAR PIX NO PUBLICO\nFICA ESPERTO MANO FICA')
        
        ## checks

        uid = self.get_uid(ctx)

        cursor = self.conn.execute("SELECT * from users WHERE id=?", (uid,))

        row = cursor.fetchone()

        if float(accounts[account_number]['cash']) < float(arg1):
            embed = discord.Embed(title=":x: Algo deu errado", description="Dinheiro insuficiente.", color=discord.Color.purple())
            return embed

        if float(arg1) <= 0:
            embed = discord.Embed(title=":x: Algo deu errado", description="Quantidade Inválida", color=discord.Color.purple())
            return embed
        
        if str(arg2) not in accounts and str(arg2) not in stores:
            embed = discord.Embed(title=":x: Algo deu errado", description="Conta {conta} não existe.".format(conta=arg2), color=discord.Color.purple())
            return embed
        ##
        
        if str(arg2) in accounts:
            accounts[account_number]['cash'] = float(f"{(float(accounts[account_number]['cash']) - float(arg1)):.2f}")
            accounts[str(arg2)]['cash'] = float(f"{(float(accounts[str(arg2)]['cash']) + float(arg1)):.2f}")

            
        elif str(arg2) in stores:
            
            accounts[account_number]['cash'] = float(f"{(float(accounts[account_number]['cash']) - float(arg1)):.2f}")
            
        for i, owner in enumerate(stores[str(arg2)]['owners']):

            perc = float(stores[str(arg2)]['percentages'][i])
            print(accounts[owner]['cash'])
            accounts[owner]['cash'] = float(f"{(float(accounts[owner]['cash']) + (float(arg1) * perc/100)):.2f}")
            print(accounts[owner]['cash'])

    @commands.command()
    async def lst(self, ctx):
        if self.is_message_public(ctx):
            await ctx.send('lista ? de que ?')
            await ctx.message.author.send('tu quer que peguem a gente memo ne?')

        # # # # #
        uid = self.get_uid(ctx)

        cursor = self.conn.execute("SELECT account, name from users")
        rows = cursor.fetchall()

        names_in_code = ''
        for row in rows:
            names_in_code += '```' + f'{row[0]} >>> {row[1]}' + '```'


        #

        await ctx.message.author.send('Pessoas que tem contas: ' + names_in_code)

        cursor.close()

            