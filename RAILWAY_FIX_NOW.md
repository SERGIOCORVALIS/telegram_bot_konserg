# 🚨 URGENT: Fix Railway Deployment - Missing Environment Variables

## Problem
```
RuntimeError: Environment variables are required: TELEGRAM_BOT_TOKEN
```

**This means:** Railway cannot find the required environment variables.

## ✅ Solution: Add Environment Variables in Railway

### Step-by-Step Instructions:

#### 1. Open Railway Dashboard
- Go to [railway.app](https://railway.app)
- Sign in to your account
- Open your project (should be named something like `telegram-ai-bot`)

#### 2. Open Your Service
- Click on your **service** (the box that says "worker" or your service name)
- You should see tabs: **Deployments**, **Metrics**, **Logs**, **Variables**, **Settings**

#### 3. Go to Variables Tab
- Click on the **"Variables"** tab
- You should see a list of variables (probably empty or with some defaults)

#### 4. Add Required Variables
Click **"New Variable"** button and add each variable one by one:

**Variable 1:**
- **Key**: `TELEGRAM_BOT_TOKEN`
- **Value**: `YOUR_SECRET_HERE`
- Click **"Add"**

**Variable 2:**
- **Key**: `OPENROUTER_API_KEY`
- **Value**: `YOUR_SECRET_HERE`
- Click **"Add"**

**Variable 3:**
- **Key**: `OPENROUTER_API_KEY_1`
- **Value**: `YOUR_SECRET_HERE`
- Click **"Add"**

**Variable 4:**
- **Key**: `OPENROUTER_API_KEY_2`
- **Value**: `YOUR_SECRET_HERE`
- Click **"Add"**

**Variable 5:**
- **Key**: `OPENROUTER_API_KEY_3`
- **Value**: `YOUR_SECRET_HERE`
- Click **"Add"**

**Variable 6:**
- **Key**: `OPENROUTER_API_KEY_4`
- **Value**: `YOUR_SECRET_HERE`
- Click **"Add"**

**Variable 7 (Optional but recommended):**
- **Key**: `APP_PUBLIC_URL`
- **Value**: `https://your-project-name.up.railway.app` (replace with your actual Railway URL)
- Click **"Add"**

**Variable 8 (Optional):**
- **Key**: `APP_NAME`
- **Value**: `AI Assistant Bot`
- Click **"Add"**

#### 5. Verify Variables Are Added
After adding all variables, you should see them listed in the Variables tab:
- ✅ TELEGRAM_BOT_TOKEN
- ✅ OPENROUTER_API_KEY
- ✅ OPENROUTER_API_KEY_1
- ✅ OPENROUTER_API_KEY_2
- ✅ OPENROUTER_API_KEY_3
- ✅ OPENROUTER_API_KEY_4
- ✅ APP_PUBLIC_URL (optional)
- ✅ APP_NAME (optional)

#### 6. Railway Will Auto-Restart
- Railway automatically restarts the service when you add/modify variables
- Wait 10-30 seconds for the restart

#### 7. Check Logs
- Go to **"Logs"** tab
- You should see:
  ```
  Starting bot polling
  Run polling for bot @AIpomoshnikalissabot id=...
  Loaded X API keys and Y models
  ```
- ✅ **If you see these messages - SUCCESS! Bot is running!**

#### 8. Test Bot
- Open Telegram
- Find your bot
- Send `/start`
- Bot should respond! 🎉

## 🔍 Troubleshooting

### If you still see the error:

1. **Check variable names** - Make sure they are EXACTLY:
   - `TELEGRAM_BOT_TOKEN` (not `TELEGRAM_TOKEN` or `BOT_TOKEN`)
   - `OPENROUTER_API_KEY` (not `OPENROUTER_KEY`)

2. **Check for extra spaces** - Make sure there are no spaces before/after the variable name or value

3. **Check you're in the right service** - Make sure you added variables to the service that's running the bot (not a database or other service)

4. **Manual restart** - Click the three dots (⋮) next to your service → **"Restart"**

5. **Check service type** - Go to **Settings** → Make sure **Service Type** is `Worker` (not Web Service)

## 📸 Visual Guide

```
Railway Dashboard
├── Your Project
    └── Your Service (click here)
        ├── Deployments
        ├── Metrics
        ├── Logs
        ├── Variables ← CLICK HERE
        └── Settings

Variables Tab:
┌─────────────────────────────────┐
│ + New Variable                  │
├─────────────────────────────────┤
│ TELEGRAM_BOT_TOKEN = 8399...   │
│ OPENROUTER_API_KEY = sk-or...   │
│ OPENROUTER_API_KEY_1 = sk-or... │
│ ...                             │
└─────────────────────────────────┘
```

## ⚠️ Important Notes

- **Never commit tokens to GitHub** - They are stored securely in Railway
- **Variables are case-sensitive** - `TELEGRAM_BOT_TOKEN` ≠ `telegram_bot_token`
- **Railway restarts automatically** - No need to manually restart after adding variables

## ✅ Success Checklist

- [ ] Opened Railway dashboard
- [ ] Opened your service
- [ ] Went to Variables tab
- [ ] Added `TELEGRAM_BOT_TOKEN`
- [ ] Added `OPENROUTER_API_KEY`
- [ ] Added `OPENROUTER_API_KEY_1` through `OPENROUTER_API_KEY_4`
- [ ] Checked Logs tab - see "Starting bot polling"
- [ ] Tested bot in Telegram - bot responds!

## 🆘 Still Having Issues?

If after following all steps you still see the error:

1. **Delete and recreate the service:**
   - Delete the current service
   - Create a new service
   - Connect GitHub repository
   - Add all variables again

2. **Check Railway status:**
   - Go to [status.railway.app](https://status.railway.app)
   - Make sure Railway is operational

3. **Contact support:**
   - Railway Discord: [discord.gg/railway](https://discord.gg/railway)
   - Or check Railway documentation

