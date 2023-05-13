import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from python_aternos import Client, ServerStartError

load_dotenv()
LOGIN = os.getenv('ATERNOS_LOGIN')
SENHA = os.getenv('ATERNOS_PASSWORD')

class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def serveron(self, ctx):
        aternos = Client.from_hashed(f'{LOGIN}', f'{SENHA}')
        lista_de_servers = aternos.list_servers()

        liga_server = None
        for serv in lista_de_servers:
            if serv.address == 'UDAS2.aternos.me:19015':
                liga_server = serv
        
        if liga_server is not None:
    
            # Lingar o server
            try:
                liga_server.start()
                await ctx.send('Ligando servidor...')
            
            except ServerStartError:
                await ctx.send('Servidor ja ligado.')


    @commands.has_permissions(administrator=True)
    @commands.command()
    async def serveroff(self, ctx):
        aternos = Client.from_hashed(f'{LOGIN}', f'{SENHA}')
        lista_de_servers = aternos.list_servers()

        liga_server = None
        for serv in lista_de_servers:
            if serv.address == 'UDAS2.aternos.me:19015':
                liga_server = serv

        if liga_server is not None:
            # Lingar o server
            try:
                liga_server.stop()
                await ctx.send('Desligando servidor...')
            
            except ServerStartError:
                await ctx.send('Servidor ja desligado.')

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def serverrestart(self, ctx):
        aternos = Client.from_hashed(f'{LOGIN}', f'{SENHA}')
        lista_de_servers = aternos.list_servers()

        liga_server = None
        for serv in lista_de_servers:
            if serv.address == 'UDAS2.aternos.me:19015':
                liga_server = serv

        if liga_server is not None:
        
            # Lingar o server
            try:
                liga_server.restart()
                await ctx.send('Restartando servidor...')
            
            except ServerStartError:
                await ctx.send('Servidor já sendo restartado...')

        