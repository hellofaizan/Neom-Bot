import discord
from discord.ext import commands
from config import fetch_member, check_role

def vc_cmds(bot):
 # Move Command
    @bot.command(name="drag")
    @commands.check(check_role)
    async def move(ctx, member_identifier: str, target_channel_id: int):
        member = await fetch_member(ctx, member_identifier)
        if not member:
            await ctx.send(f"**Member '{member_identifier}' not found.  ||({ctx.author.name})||**")
            return

        target_channel = ctx.guild.get_channel(target_channel_id)
        if not target_channel or not isinstance(target_channel, discord.VoiceChannel):
            await ctx.send(f"**Invalid channel ID or the channel is not a voice channel.  ||({ctx.author.name})||**")
            return

        try:
            await member.move_to(target_channel)
            await ctx.send(f"**{member.display_name} has been moved to {target_channel.name}.  ||({ctx.author.name})||**")
        except discord.Forbidden:
            await ctx.send(f"**I do not have permission to move {member.display_name}.  ||({ctx.author.name})||**")
        except Exception as e:
            await ctx.send(f"**Failed to move {member.display_name}: {e}.  ||({ctx.author.name})||**")   


             # Move All Members from One VC to Another
    @bot.command(name="moveall", aliases=["mvall"])
    @commands.check(check_role)
    async def moveall(ctx, source_channel_id: int, target_channel_id: int):
        source_channel = ctx.guild.get_channel(source_channel_id)
        target_channel = ctx.guild.get_channel(target_channel_id)

        if not source_channel or not isinstance(source_channel, discord.VoiceChannel):
            await ctx.send(f"**Invalid source channel ID.  ||({ctx.author.name})||**")
            return
        if not target_channel or not isinstance(target_channel, discord.VoiceChannel):
            await ctx.send(f"**Invalid target channel ID.  ||({ctx.author.name})||**")
            return

        members = source_channel.members
        if not members:
            await ctx.send(f"**No members found in {source_channel.name}.  ||({ctx.author.name})||**")
            return

        for member in members:
            try:
                await member.move_to(target_channel)
            except Exception as e:
                await ctx.send(f"**Failed to move {member.display_name}: {e}.  ||({ctx.author.name})||**")

        await ctx.send(f"**All members have been moved from {source_channel.name} to {target_channel.name}.  ||({ctx.author.name})||**")



# Mute All Command
    @bot.command(name="muteall")
    @commands.check(check_role)
    async def muteall(ctx, voice_channel_id: int):
        voice_channel = ctx.guild.get_channel(voice_channel_id)
        if not voice_channel or not isinstance(voice_channel, discord.VoiceChannel):
            await ctx.send(f"**Invalid channel ID or the channel is not a voice channel.  ||({ctx.author.name})||**")
            return

        members = voice_channel.members
        if not members:
            await ctx.send(f"**No members are in {voice_channel.name}.  ||({ctx.author.name})||**")
            return

        for member in members:
            try:
                await member.edit(mute=True)
            except Exception as e:
                await ctx.send(f"**Failed to mute {member.display_name}: {e}.  ||({ctx.author.name})||**")

        await ctx.send(f"**All members in {voice_channel.name} have been muted.  ||({ctx.author.name})||**")

    # Disconnect All Command
    @bot.command(name="disconnectall", aliases=["dcall"])
    @commands.check(check_role)
    async def disconnectall(ctx, voice_channel_id: int):
        voice_channel = ctx.guild.get_channel(voice_channel_id)
        if not voice_channel or not isinstance(voice_channel, discord.VoiceChannel):
            await ctx.send(f"**Invalid channel ID or the channel is not a voice channel.  ||({ctx.author.name})||**")
            return

        members = voice_channel.members
        if not members:
            await ctx.send(f"**No members are in {voice_channel.name}.  ||({ctx.author.name})||**")
            return

        for member in members:
            try:
                await member.move_to(None)
            except Exception as e:
                await ctx.send(f"**Failed to disconnect {member.display_name}: {e}.  ||({ctx.author.name})||**")

        await ctx.send(f"**All members have been disconnected from {voice_channel.name}.  ||({ctx.author.name})||**")

# Unmute All Command
    @bot.command(name="unmuteall")
    @commands.check(check_role)
    async def unmuteall(ctx, voice_channel_id: int):
        voice_channel = ctx.guild.get_channel(voice_channel_id)
        if not voice_channel or not isinstance(voice_channel, discord.VoiceChannel):
            await ctx.send(f"**Invalid channel ID or the channel is not a voice channel.  ||({ctx.author.name})||**")
            return

        members = voice_channel.members
        if not members:
            await ctx.send(f"**No members are in {voice_channel.name}.  ||({ctx.author.name})||**")
            return

        for member in members:
            try:
                await member.edit(mute=False)
            except Exception as e:
                await ctx.send(f"**Failed to unmute {member.display_name}: {e}.  ||({ctx.author.name})||**")

        await ctx.send(f"**All members in {voice_channel.name} have been unmuted.  ||({ctx.author.name})||**")
