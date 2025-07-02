import discord
from discord.ext import commands
from datetime import timedelta
from config import fetch_member, check_role
from collections import defaultdict
sniped_messages = defaultdict(list)

def moderation_cmds(bot):

    @bot.event
    async def on_message_delete(message):
        if message.author.bot:
            return

        record = {
            "content": message.content,
            "author": str(message.author),
            "timestamp": message.created_at,
            "attachments": [attachment.url for attachment in message.attachments],
        }

        # Add the record to the channel's sniped history
        channel_snipes = sniped_messages[message.channel.id]
        channel_snipes.append(record)

        # Keep only the last 10 snipes
        if len(channel_snipes) > 10:
            channel_snipes.pop(0)

    @bot.command(name="snipe")
    @commands.check(check_role)
    async def snipe(ctx, index: int = 1):
        channel_snipes = sniped_messages.get(ctx.channel.id, [])
        if not channel_snipes:
            await ctx.send("There's nothing to snipe in this channel!")
            return

        # Ensure the index is valid
        if index < 1 or index > len(channel_snipes):
            await ctx.send(f"Invalid index! Choose a number between 1 and {len(channel_snipes)}.")
            return

        # Retrieve the desired message from history
        sniped_message = channel_snipes[-index]

        # Create an embed to display the message
        embed = discord.Embed(
            description=sniped_message["content"] or "[No content]",
            color=discord.Color.red(),
            timestamp=sniped_message["timestamp"],
        )
        embed.set_author(name=sniped_message["author"])
        embed.set_footer(text=f"Sniped by {ctx.author.name} | Message #{index}")

        # Add attachments to the embed, if any
        if sniped_message["attachments"]:
            embed.add_field(
                name="Attachments",
                value="\n".join(sniped_message["attachments"]),
                inline=False,
            )

        await ctx.send(embed=embed)

    @bot.command(name="snipe_list")
    @commands.check(check_role)
    async def snipe_list(ctx):
        channel_snipes = sniped_messages.get(ctx.channel.id, [])
        if not channel_snipes:
            await ctx.send("There's nothing to snipe in this channel!")
            return

        # Create a summary of the sniped messages
        snipe_summary = "\n".join(
            [
                f"**#{len(channel_snipes) - i}:** {sniped['author']} - {sniped['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}"
                for i, sniped in enumerate(reversed(channel_snipes))
            ]
        )
        await ctx.send(f"Sniped message history:\n{snipe_summary}")
            
    # Kick Command
    @bot.command(name="kick")
    @commands.check(check_role)
    async def kick(ctx, member_identifier: str, *, reason: str = "No reason provided"):

        member = await fetch_member(ctx, member_identifier)
        if not member:
            await ctx.send(f"**Member '{member_identifier}' not found.  ||({ctx.author.name})||**")
            return
        try:
            await member.kick(reason=reason)
            await ctx.send(f"**{member.display_name} has been kicked. Reason: {reason}  ||({ctx.author.name})||**")
        except discord.Forbidden:
            await ctx.send(f"**I do not have permission to kick {member.display_name}.  ||({ctx.author.name})||**")
        except Exception as e:
            await ctx.send(f"**Failed to kick the member: {e}  ||({ctx.author.name})||**")

            # Ban Command
    @bot.command(name="ban")
    @commands.check(check_role)
    async def ban(ctx, member_identifier: str, *, reason: str = "No reason provided"):
        member = await fetch_member(ctx, member_identifier)
        if not member:
            await ctx.send(f"**Member '{member_identifier}' not found.  ||({ctx.author.name})||**")
            return
        try:
            await member.ban(reason=reason)
            await ctx.send(f"**{member.display_name} has been banned. Reason: {reason}  ||({ctx.author.name})||**")
        except discord.Forbidden:
            await ctx.send(f"**I do not have permission to ban {member.display_name}.  ||({ctx.author.name})||**")
        except Exception as e:
            await ctx.send(f"**Failed to ban the member: {e}  ||({ctx.author.name})||**")


    # Unban Command
    @bot.command(name="unban")
    @commands.check(check_role)
    async def unban(ctx, user_id: int):
        try:
            user = await bot.fetch_user(user_id)
            await ctx.guild.unban(user)
            await ctx.send(f"**{user.name}#{user.discriminator} has been unbanned.  ||({ctx.author.name})||**")
        except discord.NotFound:
            await ctx.send(f"**User with ID {user_id} not found in the ban list.  ||({ctx.author.name})||**")
        except discord.Forbidden:
            await ctx.send(f"**I do not have permission to unban this user.  ||({ctx.author.name})||**")
        except Exception as e:
            await ctx.send(f"**Failed to unban the user: {e}  ||({ctx.author.name})||**")


# Timeout Command
    @bot.command(name="timeout", aliases=["to"])
    @commands.check(check_role)
    async def timeout(ctx, member_identifier: str, duration: str):
        member = await fetch_member(ctx, member_identifier)
        if not member:
            await ctx.send(f"**Member '{member_identifier}' not found.  ||({ctx.author.name})||**")
            return

        # Parse duration (e.g., "1m", "1h", "1d")
        time_units = {
            "s": "second",
            "m": "minute",
            "h": "hour",
            "d": "day"
        }
        try:
            time_value = int(duration[:-1])
            unit = duration[-1]
            if unit not in time_units:
                raise ValueError
            seconds = time_value * {"s": 1, "m": 60, "h": 3600, "d": 86400}[unit]
            unit_full = time_units[unit]
            unit_full = unit_full + "s" if time_value > 1 else unit_full
        except ValueError:
            await ctx.send(f"**Invalid duration format: {duration}. Use 1s, 1m, 1h, or 1d.  ||({ctx.author.name})||**")
            return

        try:
            timeout_until = discord.utils.utcnow() + timedelta(seconds=seconds)
            await member.timeout(timeout_until, reason=f"Timed out by {ctx.author.name}")
            await ctx.send(f"**{member.display_name} has been timed out for {time_value} {unit_full}.  ||({ctx.author.name})||**")
        except discord.Forbidden:
            await ctx.send(f"**I do not have permission to timeout {member.display_name}.  ||({ctx.author.name})||**")
        except Exception as e:
            await ctx.send(f"**Failed to timeout {member.display_name}: {e}.  ||({ctx.author.name})||**")


# Remove Timeout Command
    @bot.command(name="removetimeout", aliases=["rmto"])
    @commands.check(check_role)
    async def remove_timeout(ctx, member_identifier: str):
        member = await fetch_member(ctx, member_identifier)
        if not member:
            await ctx.send(f"**Member '{member_identifier}' not found.  ||({ctx.author.name})||**")
            return

        try:
            await member.timeout(None, reason=f"Timeout removed by {ctx.author.name}")
            await ctx.send(f"**Timeout removed for {member.display_name}.  ||({ctx.author.name})||**")
        except discord.Forbidden:
            await ctx.send(f"**I do not have permission to remove timeout for {member.display_name}.  ||({ctx.author.name})||**")
        except Exception as e:
            await ctx.send(f"**Failed to remove timeout for {member.display_name}: {e}.  ||({ctx.author.name})||**")

 # Purge Command (Clearing messages)
    @bot.command(name="purge")
    @commands.check(check_role)
    async def purge(ctx, amount: int):
        try:
            await ctx.channel.purge(limit=amount)
            await ctx.send(f"**{amount} messages have been deleted.  ||({ctx.author.name})||**", delete_after=5)
        except discord.Forbidden:
            await ctx.send(f"**I do not have permission to delete messages.  ||({ctx.author.name})||**")
        except Exception as e:
            await ctx.send(f"**Failed to delete messages: {e}.  ||({ctx.author.name})||**")


    # Dictionary to store warnings
    warnings = {}

    # Warn Command
    @bot.command(name="warn")
    @commands.check(check_role)
    async def warn(ctx, member_identifier: str, *, reason: str = "No reason provided"):
        member = await fetch_member(ctx, member_identifier)
        if not member:
            await ctx.send(f"**Member '{member_identifier}' not found.  ||({ctx.author.name})||**")
            return

        # Log the warning
        if member.id not in warnings:
            warnings[member.id] = []
        warnings[member.id].append((ctx.author.name, reason))

        await ctx.send(f"**{member.display_name} has been warned. Reason: {reason}.  ||({ctx.author.name})||**")

    # Command to check warnings
    @bot.command(name="warnings")
    @commands.check(check_role)
    async def view_warnings(ctx, member_identifier: str):
        member = await fetch_member(ctx, member_identifier)
        if not member:
            await ctx.send(f"**Member '{member_identifier}' not found.  ||({ctx.author.name})||**")
            return

        member_warnings = warnings.get(member.id, [])
        if not member_warnings:
            await ctx.send(f"**{member.display_name} has no warnings.**")
        else:
            embed = discord.Embed(title=f"Warnings for {member.display_name}", color=discord.Color.orange())
            for idx, (issuer, reason) in enumerate(member_warnings, start=1):
                embed.add_field(name=f"Warning {idx}", value=f"Issued by: {issuer}\nReason: {reason}", inline=False)
            await ctx.send(embed=embed)

    # Change Nickname Command
    @bot.command(name="changenick", aliases=["nick"])
    @commands.check(check_role)
    async def change_nickname(ctx, member_identifier: str, *, new_nickname: str):
        member = await fetch_member(ctx, member_identifier)
        if not member:
            await ctx.send(f"**Member '{member_identifier}' not found.  ||({ctx.author.name})||**")
            return

        try:
            await member.edit(nick=new_nickname)
            await ctx.send(f"**{member.display_name}'s nickname has been changed to '{new_nickname}'.  ||({ctx.author.name})||**")
        except discord.Forbidden:
            await ctx.send(f"**I do not have permission to change {member.display_name}'s nickname.  ||({ctx.author.name})||**")
        except Exception as e:
            await ctx.send(f"**Failed to change nickname: {e}.  ||({ctx.author.name})||**")

    # Add Role Command
    @bot.command(name="addrole", aliases=["adrl"])
    @commands.check(check_role)
    async def add_role(ctx, member_identifier: str, role_name_or_id: str):
        """
        Command to add a role to a member.
        The role can be specified by either name or ID.
        :param ctx: The context of the command.
        :param member_identifier: The member to whom the role should be assigned.
        :param role_name_or_id: The name or ID of the role to assign.
        """
        # Fetch the member
        member = await fetch_member(ctx, member_identifier)
        if not member:
            await ctx.send(f"**Member '{member_identifier}' not found.  ||({ctx.author.name})||**")
            return

        # Try to get the role by ID or name
        role = None
        if role_name_or_id.isdigit():  # Check if it's a digit (role ID)
            role = ctx.guild.get_role(int(role_name_or_id))  # Fetch role by ID
        else:
           role = discord.utils.find(lambda r: r.name.lower() == role_name_or_id.lower(), ctx.guild.roles)  # Fetch role by name

        # Check if role was found
        if not role:
            await ctx.send(f"**Role '{role_name_or_id}' not found.  ||({ctx.author.name})||**")
            return

        try:
            # Add the role to the member
            await member.add_roles(role)
            await ctx.send(f"**Role '{role.name}' has been added to {member.display_name}.  ||({ctx.author.name})||**")

        except discord.Forbidden:
            await ctx.send(f"**I do not have permission to manage roles for {member.display_name}.  ||({ctx.author.name})||**")
        except Exception as e:
            await ctx.send(f"**Failed to add role: {e}.  ||({ctx.author.name})||**")

            
    # Remove Role Command
    @bot.command(name="removerole", aliases=["rmrl"])
    @commands.check(check_role)
    async def remove_role(ctx, member_identifier: str, role_name_or_id: str):
        """
        Command to remove a role from a member.
        The role can be specified by either name or ID.
        :param ctx: The context of the command.
        :param member_identifier: The member from whom the role should be removed.
        :param role_name_or_id: The name or ID of the role to remove.
        """
        # Fetch the member
        member = await fetch_member(ctx, member_identifier)
        if not member:
            await ctx.send(f"**Member '{member_identifier}' not found.  ||({ctx.author.name})||**")
            return

        # Try to get the role by ID or name
        role = None
        if role_name_or_id.isdigit():  # Check if it's a digit (role ID)
            role = ctx.guild.get_role(int(role_name_or_id))  # Fetch role by ID
        else:
            role = discord.utils.find(lambda r: r.name.lower() == role_name_or_id.lower(), ctx.guild.roles)  # Fetch role by name

        # Check if role was found
        if not role:
            await ctx.send(f"**Role '{role_name_or_id}' not found.  ||({ctx.author.name})||**")
            return

        try:
            # Remove the role from the member
            await member.remove_roles(role)
            await ctx.send(f"**Role '{role.name}' has been removed from {member.display_name}.  ||({ctx.author.name})||**")

        except discord.Forbidden:
            await ctx.send(f"**I do not have permission to manage roles for {member.display_name}.  ||({ctx.author.name})||**")
        except Exception as e:
            await ctx.send(f"**Failed to remove role: {e}.  ||({ctx.author.name})||**")


  # DM Command
    @bot.command(name="dm")
    @commands.check(check_role)
    async def dm(ctx, member_identifier: str, *, message: str):
        member = await fetch_member(ctx, member_identifier)
        if not member:
            await ctx.send(f"**Member '{member_identifier}' not found.  ||({ctx.author.name})||**")
            return

        try:
            await member.send(f"**Message from {ctx.author.name} ({ctx.guild.name}):**\n{message}")
            await ctx.send(f"**Message sent to {member.display_name}.  ||({ctx.author.name})||**")
        except discord.Forbidden:
            await ctx.send(f"**I could not DM {member.display_name}. They might have DMs disabled.  ||({ctx.author.name})||**")
        except Exception as e:
            await ctx.send(f"**Failed to send the message: {e}.  ||({ctx.author.name})||**")

    # DM Warn Command
    @bot.command(name="dmwarn")
    @commands.check(check_role)
    async def dmwarn(ctx, member_identifier: str, *, message: str):
        member = await fetch_member(ctx, member_identifier)
        if not member:
            await ctx.send(f"**Member '{member_identifier}' not found.  ||({ctx.author.name})||**")
            return

        try:
            await member.send(f"**You have received a warning from {ctx.guild.name}:**\n{message}")
            await ctx.send(f"**Warning sent to {member.display_name}.  ||({ctx.author.name})||**")
        except discord.Forbidden:
            await ctx.send(f"**I could not DM {member.display_name}. They might have DMs disabled.  ||({ctx.author.name})||**")
        except Exception as e:
            await ctx.send(f"**Failed to send the warning: {e}.  ||({ctx.author.name})||**")


    @bot.command(name="spam")
    @commands.check(check_role)
    async def spam(ctx, times: int, *, message: str):
        """
        Sends a message multiple times in the channel.
        :param ctx: Context of the command.
        :param times: Number of times to repeat the message.
        :param message: The message to send.
        """
        if times <= 0:
            await ctx.send("**Number of times must be greater than 0.**")
            return
        
        try:
               for _ in range(times):
                   await ctx.send(message)
        except Exception as e:
               await ctx.send(f"**Failed to send spam messages: {e}.**")