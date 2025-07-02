import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "PASTE_BOT_TOKEN_HERE")
PREFIX = "&"
REQUIRED_ROLE = "OWNER"

import discord
from discord.ext import commands

# Utility function to fetch a member by mention, username, display name, or ID
async def fetch_member(ctx, member_identifier: str):
    if member_identifier.isdigit():
        return await ctx.guild.fetch_member(int(member_identifier))
    if member_identifier.startswith('<@') and member_identifier.endswith('>'):
        user_id = int(member_identifier[2:-1].replace('!', ''))  # Handle optional exclamation mark for nickname mentions
        return await ctx.guild.fetch_member(user_id)
    else:
        member = discord.utils.find(
            lambda m: m.name.lower() == member_identifier.lower() or m.display_name.lower() == member_identifier.lower(),
            ctx.guild.members
        )
        if member is None:
            members = await ctx.guild.fetch_members(limit=None).flatten()
            member = discord.utils.find(
                lambda m: m.name.lower() == member_identifier.lower() or m.display_name.lower() == member_identifier.lower(),
                members
            )
        return member


# Check Role Function to Restrict Commands
def check_role(ctx):
    perms = ctx.author.guild_permissions
    return (
        perms.administrator or
        perms.manage_guild or
        perms.manage_channels or
        any(role.name == REQUIRED_ROLE for role in ctx.author.roles)
    )