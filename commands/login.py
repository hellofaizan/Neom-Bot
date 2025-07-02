import discord
from discord.ext import commands
from config import check_role

def ready1(bot):
    @bot.event
    async def on_command_error(ctx, error):
        """
        Global error handler for all commands.
        """
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("❌ Command not found. Use `&cmds` to see the list of available commands.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"❌ Missing arguments. Usage: `{ctx.prefix}{ctx.command} {ctx.command.signature}`")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("❌ Invalid argument provided. Please check the command usage.")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("❌ You don't have the required permissions or roles to use this command.")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"⏳ This command is on cooldown. Try again in {error.retry_after:.2f} seconds.")
        elif isinstance(error, commands.MissingPermissions):
            missing_perms = ', '.join(error.missing_permissions)
            await ctx.send(f"❌ You need the following permissions to run this command: {missing_perms}.")
        elif isinstance(error, commands.BotMissingPermissions):
            missing_perms = ', '.join(error.missing_permissions)
            await ctx.send(f"❌ I need the following permissions to run this command: {missing_perms}.")
        else:
            # Log unexpected errors for debugging
            await ctx.send("⚠️ An unexpected error occurred. Please try again later.")
            raise error  # Optional: Raises the error for logging or debugging purposes