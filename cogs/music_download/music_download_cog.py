
from discord.ext import commands
from sys import platform
import discord
from dotenv import load_dotenv
import asyncio
import os
import shutil
from moviepy.editor import AudioFileClip



class Md(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        load_dotenv()
        self.SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
        self.SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')

    async def download_songs(self, ctx, link):
        await ctx.send(f"Baixando {link}, pode demorar. POR FAVOR SÓ USE O COMANDO $DOWN QUANDO TODOS SEUS DOWNLOADS ESTIVEREM FINALIZADOS")

        directory = "cogs/music_download/downloads"
    
        process = await asyncio.create_subprocess_shell(f"spotify_dl -l {link} -o {directory}")
        await process.communicate()

        await ctx.send("Baixado! Convertendo para mp3...")

        for root, dirs, files in os.walk(directory):
                for dir in dirs:
                    albumdir = os.path.join(root, dir)

                    for song in os.listdir(albumdir):
                        song_path = os.path.join(albumdir, song)

                        song_name = os.path.splitext(song)[0]

                        clip = AudioFileClip(song_path)
                        clip.write_audiofile(os.path.join(albumdir, f"{song_name}.mp3"))

                        await ctx.send(f"*{song_name} Convertido para mp3...*")

                        os.remove(song_path)

        await ctx.send("Convertido! Enviando arquivos...")

        await self.down(ctx)

        await ctx.send("Arquivos enviados! Apagando do banco...")

        await self.err(ctx)

        await ctx.send("Arquivos apagados!")


    @commands.command()
    async def spotifyd(self, ctx, link):
        if ctx.author.id == 226524214411132928 or ctx.author.id == 647555342510719000 or ctx.author.id == 166953039008104448:
            try:
                if platform == "win32":
                    os.system(f"set SPOTIPY_CLIENT_ID={self.SPOTIPY_CLIENT_ID}")
                    os.system(f"set SPOTIPY_CLIENT_SECRET={self.SPOTIPY_CLIENT_SECRET}")
                
                elif platform == "linux":
                    os.system(f"export SPOTIPY_CLIENT_ID='{self.SPOTIPY_CLIENT_ID}'")
                    os.system(f"export SPOTIPY_CLIENT_SECRET='{self.SPOTIPY_CLIENT_SECRET}'")

            except Exception as e:
                await ctx.send(f'Deu erro setando as env: {e}')
            
            try:
                asyncio.create_task(self.download_songs(ctx, link))

            except Exception as e:
                await ctx.send(f'Deu erro ao baixar: {e}')

    async def down(self, ctx):
        directory = "cogs/music_download/downloads"
        
        ctx.send('Enviando arquivos...')

        for root, dirs, files in os.walk(directory):
            for dir in dirs:
                albumdir = os.path.join(root, dir)

                for song in os.listdir(albumdir):
                    song_path = os.path.join(albumdir, song)
                    await ctx.send(file=discord.File(rf'{song_path}'))
        
    async def err(self, ctx):
        directory = "cogs/music_download/downloads"
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isdir(file_path):
                    await ctx.send(f"Removendo {file_path}...")
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

            

