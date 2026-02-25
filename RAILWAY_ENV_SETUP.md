# Railway Environment Variables Setup

> 🇷🇺 **Русская версия инструкции:** См. [RAILWAY_QUICK_FIX_RU.md](RAILWAY_QUICK_FIX_RU.md) для подробной инструкции на русском языке.

## Problem
Bot doesn't start with error: `RuntimeError: Environment variables are required: TELEGRAM_BOT_TOKEN`

This means environment variables are not added in Railway.

## Solution: Adding Environment Variables

### Step 1: Open Project in Railway

1. Go to [railway.app](https://railway.app)
2. Sign in to your account
3. Open project `telegram-ai-bot`

### Step 2: Add Environment Variables

1. In the project panel, click on your service
2. Go to the **"Variables"** tab
3. Click **"New Variable"**

### Step 3: Add Each Variable One by One

Add the following variables (click "Add" after each):

#### Required Variables:

```
TELEGRAM_BOT_TOKEN
```
Value: `your_telegram_bot_token`

```
OPENROUTER_API_KEY
```
Value: `your_openrouter_api_key`

#### Additional OpenRouter Keys (for rotation):

```
OPENROUTER_API_KEY_1
```
Value: `your_additional_key_1`

```
OPENROUTER_API_KEY_2
```
Value: `your_additional_key_2`

```
OPENROUTER_API_KEY_3
```
Value: `your_additional_key_3`

```
OPENROUTER_API_KEY_4
```
Value: `your_additional_key_4`

#### Optional Variables:

```
APP_PUBLIC_URL
```
Value: `https://your-project.up.railway.app` (replace with your actual URL from Railway)

```
APP_NAME
```
Value: `AI Assistant Bot`

### Step 4: Restart Service

After adding all variables:

1. Railway will automatically restart the service
2. Or click the three dots (⋮) next to the service → **"Restart"**

### Step 5: Check Logs

1. Go to the **"Deployments"** or **"Logs"** tab
2. You should see: `Starting bot polling` and `Run polling for bot...`
3. If you see these messages - the bot is running! ✅

## Quick Method (via Railway CLI)

If you have Railway CLI installed:

```bash
railway variables set TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
railway variables set OPENROUTER_API_KEY="your_openrouter_api_key"
railway variables set OPENROUTER_API_KEY_1="your_additional_key_1"
railway variables set OPENROUTER_API_KEY_2="your_additional_key_2"
railway variables set OPENROUTER_API_KEY_3="your_additional_key_3"
railway variables set OPENROUTER_API_KEY_4="your_additional_key_4"
railway variables set APP_NAME="AI Assistant Bot"
```

## Verification

After adding variables and restarting:

1. Open Telegram
2. Find your bot
3. Send `/start`
4. The bot should respond! 🎉

## Important

⚠️ **Security**: Do not publish tokens publicly. Railway stores them securely in encrypted form.

## If Error Persists

1. Make sure all variables are added correctly (no extra spaces)
2. Check that values are copied completely
3. Restart the service manually
4. Check logs for other errors
