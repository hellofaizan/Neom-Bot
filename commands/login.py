import json
import discord
from discord.ext import commands
from config import check_role

# Load data from data.json
DATA_FILE = "data.json"



try:
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
except FileNotFoundError:
    data = {"whitelisted_servers": []}

whitelisted_servers = data["whitelisted_servers"]

# Function to save changes to data.json
def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def ready1(bot):

    @bot.command()
    @commands.check(check_role)
    async def whitelist(ctx, action: str, server_id: int = None):
        """
        Add or remove servers from the whitelist or display the current whitelist.

        Usage:
        - `&whitelist add <server_id>`: Adds a server to the whitelist.
        - `&whitelist remove <server_id>`: Removes a server from the whitelist.
        - `&whitelist list`: Lists all whitelisted servers.
        """
        if action.lower() == "add":
            if server_id in whitelisted_servers:
                await ctx.send("This server is already whitelisted.")
            else:
                whitelisted_servers.append(server_id)
                save_data()
                await ctx.send(f"Server with ID {server_id} has been added to the whitelist.")

        elif action.lower() == "remove":
            if server_id in whitelisted_servers:
                whitelisted_servers.remove(server_id)
                save_data()
                await ctx.send(f"Server with ID {server_id} has been removed from the whitelist.")
            else:
                await ctx.send("This server is not in the whitelist.")

        elif action.lower() == "list":
            if whitelisted_servers:
                server_list = "\n".join(str(sid) for sid in whitelisted_servers)
                embed = discord.Embed(
                    title="Whitelisted Servers",
                    description=server_list,
                    color=discord.Color.blue()
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send("No servers are currently whitelisted.")
        else:
            await ctx.send("Invalid action. Use `add`, `remove`, or `list`.")

    @bot.command()
    @commands.check(check_role)
    async def leave_server(ctx, server_id: int):
        """
        Makes the bot leave a specified server.

        Usage:
        - `&leave_server <server_id>`: Makes the bot leave the specified server.
        """
        server = bot.get_guild(server_id)
        if server:
            if server.id not in whitelisted_servers:
                await server.leave()
                await ctx.send(f"Successfully left the server: {server.name} (ID: {server_id})")
            else:
                await ctx.send("This server is whitelisted. Remove it from the whitelist before leaving.")
        else:
            await ctx.send("The bot is not in a server with this ID.")


    # Event: Bot has joined a server
    @bot.event
    async def on_guild_join(guild):
        print(f"Joined a new server: {guild.name}")  # Debugging line to ensure the event is triggered
        if guild.id not in whitelisted_servers:
            print(f"Bot joined a non-whitelisted server: {guild.name}. Leaving...")
            await guild.leave()
        

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

    

