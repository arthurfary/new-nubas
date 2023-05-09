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

        # Iniciando por ip
        liga_server = None
        for serv in lista_de_servers:
            print(serv.address)
            if serv.address == 'UDAS2.aternos.me:19015':
                liga_server = serv

        if liga_server is not None:
            # Especificações do server
            print(liga_server.software, liga_server.version)
            # Lingar o server
            try:
                liga_server.start()
                await ctx.send('Ligando servidor...')
            
            except ServerStartError:
                await ctx.send('Servidor ja ligado.')
    