import discord
from discord.ext import commands
import asyncio

categories = {
    "moderation": (
        "`&kick <user> <reason>` - Kick a user.\n"
        "`&ban <user> <reason>` - Ban a user.\n"
        "`&unban <user_id>` - Unban a user.\n"
        "`&timeout or to <user> <duration>` - Timeout a user.\n"
        "`&removetimeout or rmto <user>` - Remove timeout.\n"
        "`&spam <times> <message>` – Send a message multiple times\n"
        "`&purge <amount>` - Delete messages.\n"
        "`&warn <user> <reason>` - Issue a warning.\n"
        "`&warnings <user>` - View warnings.\n"
        "`&nick <user> <new_nickname>` - Change nickname.\n"
        "`&addrole or adrl<user> <role>` - Add a role.\n"
        "`&removerole or rmrl <user> <role>` - Remove a role.\n"
        "`&dm <user> <message>` - Send a DM.\n"
        "`&dmwarn <user> <message>` - Send a warning DM.\n"
        "`&snipe [index]` - Retrieve the most recently deleted message.\n"
        "`&snipe_list` - View a list of deleted messages in this channel.\n "
        
    ),
    "text": (
        "`&lock` - Lock the current channel.\n"
        "`&unlock` - Unlock the current channel.\n"
        "`&sm <seconds>` - Set slowmode.\n"
    ),
    "voice": (
        "`&moveall or mvall <source_vc_id> <target_vc_id>` - Move all users to a VC.\n"
        "`&drag <user> <vc_id>` - Moves a user to specific vc.\n"
        "`&muteall <vc_id>` - Mute everyone in a VC.\n"
        "`&unmuteall <vc_id>` - Unmute everyone in a VC.\n"
        "`&disconnectall or dcall <vc_id>` - Disconnect all users in a VC."

    ),
    "user": (
        "`&afk <reason>` – Set yourself as AFK.\n"
        "`&checktokens|&ct` - checks token (in dm)\n"
        "`&avatar <user>` - Display user avatar.\n"
        "`&invite` – Get a server invite link.\n"
        "`&ping` – Check bot latency.\n"
        "`&remind <time> <message>` – Set a reminder for a specified time\n"
        "`&serverinfo or &si` – Show server details\n"
        "`&userinfo or &ui <user>` – View user info.\n"

    )
}

reactions = {
    "⚔️": "moderation",
    "📝": "text",
    "🎤": "voice",
    "🎲": "user"
}


def help_cmds(bot):
    @bot.command()
    async def cmds(ctx):
        """Displays the reaction-based help menu."""
        embed = discord.Embed(
            title="🔧 Bot Help Menu",
            description="Choose a category for more details:\n\n"
                        "⚔️ - `Moderation commands` \n"
                        "📝 - `Text channel commands`\n"
                        "🎤 - `Voice Channel`\n"
                        "🎲 - `User commands`\n\n"
                        "Use these commands with the `&` prefix.",
            color=discord.Color.blue()
        )
        message = await ctx.send(embed=embed)

        for emoji in reactions.keys():
            await message.add_reaction(emoji)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in reactions

        while True:
            try:
                reaction, user = await bot.wait_for("reaction_add", timeout=60.0, check=check)
                category = reactions[str(reaction.emoji)]

                embed = discord.Embed(
                    title=f"🔧 Help: {category.title()} Commands",
                    description=categories[category],
                    color=discord.Color.green()
                )
                await message.edit(embed=embed)
                await message.remove_reaction(reaction.emoji, user)
            except discord.errors.NotFound:
                break
            except discord.errors.Forbidden:
                break
            except discord.ext.commands.CommandError:
                break
            except Exception as e:
                print(e)
                break

    @bot.command()
    async def help(ctx):
        """Displays the reaction-based help menu (same as &cmds)."""
        await cmds(ctx)