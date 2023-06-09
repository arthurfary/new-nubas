import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

from cogs.currency.currency_cog import Currency
from cogs.sever.server_cog import Server
from cogs.error_handler.error_handler_cog import ErrorHandler


# Get the Discord token from the environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Create a bot instance with a command prefix
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# Add the Greetings cog to the bot within an async function
@bot.event
async def on_ready():
    print('> Loading cogs...')

    # bot cogs
    await bot.add_cog(Currency(bot))
    await bot.add_cog(Server(bot))
   
    await bot.add_cog(ErrorHandler(bot))
    
    print('> Cogs loaded!')
    print('> Bot ready!')

    

# Run the bot with your bot token from the .env file
if __name__ == '__main__':
    
    bot.run(TOKEN)
    