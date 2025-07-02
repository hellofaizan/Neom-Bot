import discord
from discord.ext import commands
from config import check_role


def text_cmds(bot):

# Lock Command
    @bot.command(name="lock")
    @commands.check(check_role)
    async def lock(ctx):
        try:
            overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
            overwrite.send_messages = False
            await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            await ctx.send(f"**{ctx.channel.name} has been locked.  ||({ctx.author.name})||**")
        except discord.Forbidden:
            await ctx.send(f"**I do not have permission to lock this channel.  ||({ctx.author.name})||**")
        except Exception as e:
            await ctx.send(f"**Failed to lock the channel: {e}.  ||({ctx.author.name})||**")

    # Unlock Command
    @bot.command(name="unlock")
    @commands.check(check_role)
    async def unlock(ctx):
        try:
            overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
            overwrite.send_messages = True
            await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            await ctx.send(f"**{ctx.channel.name} has been unlocked.  ||({ctx.author.name})||**")
        except discord.Forbidden:
            await ctx.send(f"**I do not have permission to unlock this channel.  ||({ctx.author.name})||**")
        except Exception as e:
            await ctx.send(f"**Failed to unlock the channel: {e}.  ||({ctx.author.name})||**")

    # Slowmode Command
    @bot.command(name="sm")
    @commands.check(check_role)
    async def sm(ctx, seconds: int):
        # Check if the input is within a valid range (0 to 21600 seconds)
        if seconds < 0 or seconds > 21600:
            await ctx.send("Please provide a valid number of seconds (0-21600).")
            return

        # Get the current channel where the command was issued
        channel = ctx.channel

        # Set the slowmode delay for the channel
        await channel.edit(slowmode_delay=seconds)
        
        if seconds == 0:
            await ctx.send(f"Slowmode has been **disabled** in {channel.mention}.")
        else:
            await ctx.send(f"Slowmode has been set to **{seconds}** seconds in {channel.mention}.")