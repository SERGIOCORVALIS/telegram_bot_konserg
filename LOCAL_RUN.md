# Local Bot Setup and Run Guide

## Quick Start

### Option 1: Using PowerShell Script (Easiest)

1. Open PowerShell in project directory
2. Run:
   ```powershell
   .\start_bot.ps1
   ```

### Option 2: Manual Setup

1. **Activate virtual environment:**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

2. **Set environment variables:**
   ```powershell
   $env:TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
   $env:OPENROUTER_API_KEY="YOUR_OPENROUTER_API_KEY"
   $env:OPENROUTER_API_KEY_1="YOUR_OPENROUTER_API_KEY"
   $env:OPENROUTER_API_KEY_2="YOUR_OPENROUTER_API_KEY"
   $env:OPENROUTER_API_KEY_3="YOUR_OPENROUTER_API_KEY"
   $env:OPENROUTER_API_KEY_4="YOUR_OPENROUTER_API_KEY"
   $env:OPENROUTER_API_KEY_5="YOUR_OPENROUTER_API_KEY"
   $env:OPENROUTER_API_KEY_6="YOUR_OPENROUTER_API_KEY"
   ```

3. **Run bot:**
   ```powershell
   python -m src.bot
   ```

### Option 3: Create .env File

Create `.env` file in project root:
```
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
OPENROUTER_API_KEY=YOUR_OPENROUTER_API_KEY
OPENROUTER_API_KEY_1=YOUR_OPENROUTER_API_KEY
OPENROUTER_API_KEY_2=YOUR_OPENROUTER_API_KEY
OPENROUTER_API_KEY_3=YOUR_OPENROUTER_API_KEY
OPENROUTER_API_KEY_4=YOUR_OPENROUTER_API_KEY
OPENROUTER_API_KEY_5=YOUR_OPENROUTER_API_KEY
OPENROUTER_API_KEY_6=YOUR_OPENROUTER_API_KEY
APP_PUBLIC_URL=https://example.com
APP_NAME=AI Assistant Bot
```

Then run:
```powershell
python -m src.bot
```

## Verify Bot is Running

You should see in console:
```
2025-11-11 XX:XX:XX | INFO | root | Starting bot polling
2025-11-11 XX:XX:XX | INFO | aiogram.dispatcher | Run polling for bot @...
2025-11-11 XX:XX:XX | INFO | root | Loaded X API keys and Y models
```

## Test Bot

1. Open Telegram
2. Find your bot (search by token or bot username)
3. Send `/start`
4. Bot should respond!

## Stop Bot

Press `Ctrl+C` in the terminal where bot is running.

## Troubleshooting

### Bot doesn't start
- Check that virtual environment is activated
- Verify environment variables are set
- Check that dependencies are installed: `pip install -r requirements.txt`

### Bot starts but doesn't respond
- Check console for errors
- Verify Telegram token is correct
- Check OpenRouter API keys are valid (run `python test_api_keys.py`)

### Import errors
- Make sure you're in project root directory
- Activate virtual environment: `.\.venv\Scripts\Activate.ps1`
- Install dependencies: `pip install -r requirements.txt`

