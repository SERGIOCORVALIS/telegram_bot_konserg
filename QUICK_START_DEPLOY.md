# 🚀 Quick Start: Railway Deployment (5 minutes)

## Step 1: Prepare GitHub Repository

1. Create an account on [GitHub.com](https://github.com) (if you don't have one)
2. Create a new repository (New Repository)
3. Name it, for example: `telegram-ai-bot`
4. Upload the code:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/telegram-ai-bot.git
git push -u origin main
```

## Step 2: Register on Railway

1. Go to [railway.app](https://railway.app)
2. Click "Start a New Project"
3. Sign in with GitHub (authorize Railway)

## Step 3: Create Project

1. Select "Deploy from GitHub repo"
2. Find your repository `telegram-ai-bot`
3. Click "Deploy Now"

## Step 4: Configure Environment Variables

1. In Railway, open your project
2. Go to the "Variables" tab
3. Click "New Variable" and add each variable:

```
TELEGRAM_BOT_TOKEN = your_telegram_bot_token
```

```
OPENROUTER_API_KEY = your_openrouter_api_key
```

```
OPENROUTER_API_KEY_1 = your_additional_key_1
```

```
OPENROUTER_API_KEY_2 = your_additional_key_2
```

```
OPENROUTER_API_KEY_3 = your_additional_key_3
```

```
OPENROUTER_API_KEY_4 = your_additional_key_4
```

```
APP_PUBLIC_URL = https://your-project.up.railway.app
```

```
APP_NAME = AI Assistant Bot
```

> **Important:** After adding variables, Railway will automatically restart the bot!

## Step 5: Verify Operation

1. Open the "Logs" tab in Railway
2. You should see: `Starting bot polling`
3. Open Telegram and send `/start` to your bot
4. The bot should respond! 🎉

## Done! ✅

Your bot is now running 24/7 on Railway!

### What's Next:

- **Update bot**: Just do `git push` - Railway will automatically update the bot
- **View logs**: "Logs" tab in Railway
- **Stop**: Settings → Delete Project (if needed)

### Problems?

- Check logs in Railway
- Make sure all environment variables are added
- Verify that tokens are correct

---

📖 **Detailed guide** with other deployment options: [DEPLOYMENT.md](DEPLOYMENT.md)
