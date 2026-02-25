# 🚀 Quick Start: Run Bot Locally

## ✅ Bot is Now Running!

The bot has been started with:
- **Telegram Token:** `REDACTED`
- **OpenRouter API Keys:** 5 keys configured
- **Status:** Running in background

## 📱 Test Your Bot

1. **Open Telegram**
2. **Find your bot** (search by username or use the token to find it)
3. **Send `/start`**
4. **Bot should respond!** 🎉

## 🔍 Check Bot Status

Look at the PowerShell window that opened - you should see:
```
Starting bot polling
Run polling for bot @... id=8544635888
Loaded 5 API keys and 4 models
```

## 🛑 Stop Bot

To stop the bot:
1. Go to the PowerShell window where bot is running
2. Press `Ctrl+C`
3. Bot will stop gracefully

## 🔄 Restart Bot

### Easy Way:
```powershell
.\start_bot.ps1
```

### Manual Way:
```powershell
# Set variables
$env:TELEGRAM_BOT_TOKEN="REDACTED"
$env:OPENROUTER_API_KEY="REDACTED"
# ... (other keys)

# Run
.\.venv\Scripts\python.exe -m src.bot
```

## 📝 Available Commands

Once bot is running, you can use:
- `/start` - Start conversation (clears history)
- `/help` - Show available commands
- `/reset` - Clear dialog history
- `/about` - Bot information
- `/feedback` - Send feedback

## ⚠️ Important Notes

1. **Bot runs only while PowerShell window is open** - Close it = Bot stops
2. **For 24/7 operation** - Deploy to Railway (see DEPLOYMENT.md)
3. **API Keys** - Current keys may be invalid (401 error). Get new ones from OpenRouter if bot doesn't respond to questions.

## 🆘 Troubleshooting

### Bot doesn't respond to messages:
- Check PowerShell window for errors
- Verify API keys are valid: `python test_api_keys.py`
- Check internet connection

### Bot shows errors:
- **401 Unauthorized** → API keys invalid, get new ones from OpenRouter
- **429 Rate Limit** → Wait a few seconds, bot will retry automatically
- **Token invalid** → Check Telegram token is correct

### Bot won't start:
- Make sure virtual environment is activated
- Check dependencies: `pip install -r requirements.txt`
- Verify environment variables are set

## 📚 More Information

- **Full setup guide:** [LOCAL_RUN.md](LOCAL_RUN.md)
- **Deploy to Railway:** [DEPLOYMENT.md](DEPLOYMENT.md)
- **Test API keys:** `python test_api_keys.py`

