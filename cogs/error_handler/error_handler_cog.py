import discord
from discord.ext import commands

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.author.send(f"Argumento obrigatório faltando. ({error.param.name})")
        elif isinstance(error, commands.CommandNotFound):
            await ctx.message.author.send(f"Este comando não existe.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.message.author.send(f"Você não tem permissão para usar este comando. ({error.missng_perms[0]})") 
        else:
            await ctx.message.author.send(f"Um erro ocorreu: {error}.")