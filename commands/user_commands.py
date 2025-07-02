# user_commands.py

import discord
from discord.ext import commands
import asyncio
import random
from config import fetch_member

def user_cmds(bot):


    # Ping Command
    @bot.command(name="ping")
    async def ping(ctx):
        await ctx.send(f"**Pong!** Latency: {round(bot.latency * 1000)}ms")



# Server Info Command
    @bot.command(name="serverinfo", aliases=["si"])
    async def server_info(ctx):
        guild = ctx.guild
        embed = discord.Embed(title=f"Server Information - {guild.name}", color=discord.Color.green())
        embed.add_field(name="Server Owner", value=f"SIOTUS", inline=True)
        embed.add_field(name="Member Count", value=f"{guild.member_count} members", inline=True)
        #embed.add_field(name="Server Region", value=str(guild.region), inline=True)
        embed.add_field(name="Creation Date", value=guild.created_at.strftime("%B %d, %Y"), inline=True)
        embed.add_field(name="Boosts", value=f"{guild.premium_subscription_count} boosts", inline=True)
        await ctx.send(embed=embed)

    # User Info Command
    @bot.command(name="userinfo", aliases=["ui"])
    async def user_info(ctx, member_identifier: str):
        member = await fetch_member(ctx, member_identifier)
        if not member:
            await ctx.send(f"**Member '{member_identifier}' not found, **")
            return

        embed = discord.Embed(title=f"User Information - {member.name}", color=discord.Color.blue())
        embed.add_field(name="Username", value=member.name, inline=True)
        embed.add_field(name="Discriminator", value=f"#{member.discriminator}", inline=True)
        embed.add_field(name="Joined At", value=member.joined_at.strftime("%B %d, %Y"), inline=True)
        embed.add_field(name="Roles", value=", ".join([role.name for role in member.roles[1:]]), inline=False)
        embed.add_field(name="Account Created At", value=member.created_at.strftime("%B %d, %Y"), inline=True)
        await ctx.send(embed=embed)

    # Avatar Command
    @bot.command(name="avatar", aliases=["av"])
    async def avatar(ctx, member_identifier: str = None):
        member = await fetch_member(ctx, member_identifier) if member_identifier else ctx.author
        if member:
            await ctx.send(f"**{member.name}'s Avatar:** {member.avatar.url}")
        else:
            await ctx.send(f"**Could not find user: {member_identifier}.**")

    # Dice Roll Command
    @bot.command(name="roll")
    async def roll(ctx):
        roll_result = random.randint(1, 6)
        await ctx.send(f"**You rolled a {roll_result}!**")

    # Invite Command
    @bot.command(name="invite")
    async def invite(ctx):
        invite = await ctx.channel.create_invite(max_uses=1, unique=True)
        await ctx.send(f"**Here is your server invite link:** {invite.url}")


    # Dictionary to store AFK users
    afk_users = {}

    # AFK Command
    @bot.command(name="afk")
    async def afk(ctx, *, reason: str = "AFK"):
        afk_users[ctx.author.id] = reason
        await ctx.send(f"**{ctx.author.name} is now AFK: {reason}**")

    # Event to handle AFK status
    @bot.event
    async def on_message(message):
        if message.author.id in afk_users:
            del afk_users[message.author.id]
            await message.channel.send(f"**Welcome back, {message.author.name}! You are no longer AFK.**")

        if message.mentions:
            for user in message.mentions:
                if user.id in afk_users:
                    await message.channel.send(f"**{user.name} is currently AFK: {afk_users[user.id]}**")
        await bot.process_commands(message)




    @bot.command(name="remind")
    async def remind(ctx, time: str, *, message: str):
        """
        Sends a reminder message after a specified amount of time.
        :param ctx: Context of the command.
        :param time: The time to wait (e.g., 1s, 1m, 1h, 1d).
        :param message: The reminder message to send.
        """
        # Convert time string to seconds
        time_units = {"s": 1, "m": 60, "h": 3600, "d": 86400}
        try:
            duration = int(time[:-1]) * time_units[time[-1].lower()]
        except (ValueError, KeyError):
            await ctx.send("**Invalid time format. Use formats like 1s, 1m, 1h, 1d.**")
            return

        if duration <= 0:
            await ctx.send("**Time must be greater than 0.**")
            return

        try:
            await ctx.send(f"**Reminder set for {time}. I'll remind you soon!**")
            await asyncio.sleep(duration)
            await ctx.send(f"**Reminder: {message} **")
        except Exception as e:
            await ctx.send(f"**Failed to set the reminder: {e}.**")


        