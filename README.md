# Neom Bot

A feature-rich Discord bot for moderation, utility, voting, and more.

---

## Features
- Moderation (kick, ban, timeout, warn, purge, etc.)
- Text channel management (lock, unlock, slowmode)
- Voice channel management (move, mute, disconnect, etc.)
- User utilities (AFK, avatar, server info, reminders, etc.)
- Voting and token management for Karuta
- Reaction-based help menu

---

## Required Discord Bot Permissions
To function properly, the bot needs the following permissions. You can check these boxes when creating the bot invite link in the Discord Developer Portal:

### General Permissions
- [x] Administrator *(recommended for all features, otherwise select all below)*
- [x] View Audit Log
- [x] Manage Server
- [x] Manage Roles
- [x] Manage Channels
- [x] Kick Members
- [x] Ban Members
- [x] Create Instant Invite
- [x] Change Nickname
- [x] Manage Nicknames
- [x] View Channels
- [x] Moderate Members

### Text Permissions
- [x] Send Messages
- [x] Manage Messages
- [x] Embed Links
- [x] Attach Files
- [x] Read Message History
- [x] Mention Everyone
- [x] Use External Emojis
- [x] Add Reactions

### Voice Permissions
- [x] Connect
- [x] Speak
- [x] Mute Members
- [x] Deafen Members
- [x] Move Members

> **Note:** If you do not want to use Administrator, make sure to grant all the above individually.

---

## Getting the Bot Token
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Create a new application or select your bot application.
3. Go to the **Bot** tab and click **Reset Token** or **Copy** to get your bot token.
4. Open the `config.py` file in this project and set the value of `BOT_TOKEN`:
   ```python
   BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
   ```

---

## Installation & Setup

### 1. Clone the Repository
```sh
git clone <repo-url>
cd Neom\ Bot
```

### 2. Install Python Dependencies
Make sure you have Python 3.8+ installed.

```sh
pip install -r requirements.txt
```

### 3. Configure the Bot
- Edit `config.py`:
  - Set your `BOT_TOKEN`.
  - Optionally, change `PREFIX` and `REQUIRED_ROLE` as needed.

### 4. Run the Bot
```sh
python main.py
```

---

## Usage
- Use `&help` or `&cmds` in your server to see the help menu.
- Most commands require you to have a specific role (default: `OWNER`).
- Some commands (like token checking) require you to DM the bot.

---

## Example Commands
- `&kick <user> <reason>` — Kick a user
- `&ban <user> <reason>` — Ban a user
- `&timeout <user> <duration>` — Timeout a user (e.g., 1h, 30m)
- `&lock` / `&unlock` — Lock or unlock a channel
- `&moveall <source_vc_id> <target_vc_id>` — Move all users between voice channels
- `&remind 10m Take a break!` — Set a reminder
- `&token add <token>` — Add a Karuta token

---

## Notes
- The bot stores some data in `data.json` and `tokens.txt`.
- For advanced voting features, see the Karuta commands in the help menu.
- If you encounter permission errors, double-check the bot's role and permissions in your server settings.

---

## License
MIT 