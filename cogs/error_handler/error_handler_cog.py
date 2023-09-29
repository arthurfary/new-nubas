import discord
from discord.ext import commands

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.author.send(f":x: Argumento obrigatório faltando. ({error.param.name})")

        elif isinstance(error, commands.CommandNotFound):
            await ctx.message.author.send(f":x: Este comando não existe.")

        elif isinstance(error, commands.MissingPermissions):
            await ctx.message.author.send(f":x: Você não tem permissão para usar este comando. ({error.missng_perms[0]})") 

        if isinstance(error, commands.CommandInvokeError):
            original = error.original  
            if isinstance(original, Exception):
                await ctx.message.author.send(f":x: Um erro ocorreu: {original.args[0]}")

        else:
            error_message = str(error.args[0]) if error.args else str(error)
            await ctx.message.author.send(f"Um erro ocorreu: {error_message}.")