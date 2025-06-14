# Discord Bot

A feature-rich Discord bot with moderation, fun, music, and chatbot capabilities.

## Features

### Chatbot Features
- Bot will respond when mentioned (@bot)
- Smart responses based on message content
- Customizable personality and responses
- Commands:
  - `!setpersonality <text>` - Set bot's personality (Owner only)
  - `!setname <name>` - Set bot's display name (Owner only)
  - `!setresponse <response>` - Add a custom response (Owner only)
  - `!sethelp <response>` - Add a custom help response (Owner only)
  - `!removeresponse <index>` - Remove a response by index (Owner only)
  - `!removehelp <index>` - Remove a help response by index (Owner only)
  - `!listresponses` - List all responses and settings (Owner only)
  - `!resetprompts` - Reset all prompts to default (Owner only)

### Moderation Commands
- `!kick <user> [reason]` - Kick a user from the server
- `!ban <user> [reason]` - Ban a user from the server
- `!clear <amount>` - Clear a specified number of messages
- `!mute <user> <duration> [reason]` - Mute a user for a specified duration (in minutes)

### Fun Commands
- `!8ball <question>` - Ask the magic 8-ball a question
- `!meme` - Get a random meme from Reddit
- `!roll <NdN>` - Roll dice (e.g., !roll 2d6)
- `!choose <option1> <option2> ...` - Choose between multiple options

### Music Commands
- `!join` - Join the voice channel
- `!play <url>` - Play music from a URL
- `!stop` - Stop playing and disconnect
- `!skip` - Skip the current song
- `!queue` - Show the current queue
- `!pause` - Pause the current song
- `!resume` - Resume the current song

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your Discord bot token:
   ```
   DISCORD_TOKEN=your_bot_token_here
   ```
4. Run the bot:
   ```bash
   python main.py
   ```

## GitHub Actions Deployment

The bot can be run automatically using GitHub Actions. To set this up:

1. Go to your repository settings
2. Navigate to Secrets
3. Add a new secret named `DISCORD_TOKEN` with your bot token
4. The bot will automatically run when you push to the main branch

## Requirements

- Python 3.9 or higher
- FFmpeg (for music commands)
- Dependencies listed in requirements.txt

## License

MIT License #   N e w N o t i f S O C  
 