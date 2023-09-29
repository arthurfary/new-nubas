import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

from cogs.music_download.music_download_cog import Md
from cogs.currency.currency_cog import Currency
from cogs.error_handler.error_handler_cog import ErrorHandler


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('> Loading cogs...')

    await bot.add_cog(Md(bot))

    await bot.add_cog(Currency(bot))
   
    await bot.add_cog(ErrorHandler(bot))
    
    print('> Cogs loaded!')
    print('> Bot ready!')

    

# Run the bot with your bot token from the .env file
if __name__ == '__main__':
    
    bot.run(TOKEN)
    
