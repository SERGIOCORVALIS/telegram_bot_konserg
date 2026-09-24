# 🎯 STEP-BY-STEP: Add Variables to Railway (5 minutes)

## ⚠️ Current Problem
```
RuntimeError: Environment variables are required: TELEGRAM_BOT_TOKEN
```

**This means:** Railway cannot find `TELEGRAM_BOT_TOKEN` variable.

## ✅ Solution: Add Variables (Follow Exactly)

### Step 1: Open Railway
1. Go to: https://railway.app
2. Sign in
3. Click on your project (the one with the bot)

### Step 2: Find Your Service
- You should see a box/card that says "worker" or your service name
- **Click on that box** (not the project name, but the service inside)

### Step 3: Open Variables Tab
- At the top, you'll see tabs: `Deployments`, `Metrics`, `Logs`, **`Variables`**, `Settings`
- **Click on "Variables"** tab

### Step 4: Add First Variable (TELEGRAM_BOT_TOKEN)
1. Click the button **"New Variable"** or **"+ New"**
2. In the **"Key"** field, type exactly: `TELEGRAM_BOT_TOKEN`
3. In the **"Value"** field, paste: `YOUR_SECRET_HERE`
4. Click **"Add"** or **"Save"**

### Step 5: Add Second Variable (OPENROUTER_API_KEY)
1. Click **"New Variable"** again
2. **Key**: `OPENROUTER_API_KEY`
3. **Value**: `YOUR_SECRET_HERE`
4. Click **"Add"**

### Step 6: Add Additional Keys (Optional but Recommended)
Repeat for each:

**Variable 3:**
- Key: `OPENROUTER_API_KEY_1`
- Value: `YOUR_SECRET_HERE`

**Variable 4:**
- Key: `OPENROUTER_API_KEY_2`
- Value: `YOUR_SECRET_HERE`

**Variable 5:**
- Key: `OPENROUTER_API_KEY_3`
- Value: `YOUR_SECRET_HERE`

**Variable 6:**
- Key: `OPENROUTER_API_KEY_4`
- Value: `YOUR_SECRET_HERE`

### Step 7: Verify Variables Are Added
After adding, you should see a list like this:
```
✅ TELEGRAM_BOT_TOKEN
✅ OPENROUTER_API_KEY
✅ OPENROUTER_API_KEY_1
✅ OPENROUTER_API_KEY_2
✅ OPENROUTER_API_KEY_3
✅ OPENROUTER_API_KEY_4
```

### Step 8: Wait for Auto-Restart
- Railway automatically restarts when you add variables
- Wait 20-30 seconds
- You'll see a new deployment starting

### Step 9: Check Logs
1. Go to **"Logs"** tab
2. Scroll to the bottom (newest logs)
3. Look for:
   ```
   Starting bot polling
   Run polling for bot @AIpomoshnikalissabot id=...
   Loaded X API keys and Y models
   ```
4. ✅ **If you see "Starting bot polling" - SUCCESS!**

### Step 10: Test Bot
1. Open Telegram
2. Find your bot
3. Send `/start`
4. Bot should respond! 🎉

## 🔍 Common Mistakes to Avoid

❌ **Wrong:** Adding variables to the PROJECT (not the service)
✅ **Right:** Add variables to the SERVICE (the "worker" box)

❌ **Wrong:** Variable name with spaces: `TELEGRAM_BOT_TOKEN ` (space at end)
✅ **Right:** Exact name: `TELEGRAM_BOT_TOKEN` (no spaces)

❌ **Wrong:** Adding variables but not clicking "Add" button
✅ **Right:** Click "Add" after each variable

❌ **Wrong:** Adding to wrong service (database, redis, etc.)
✅ **Right:** Add to the service that runs `python -m src.bot`

## 🆘 Still Not Working?

### Check 1: Are variables actually added?
- Go to Variables tab
- Do you see `TELEGRAM_BOT_TOKEN` in the list?
- If NO → You didn't add it correctly, try again
- If YES → Continue to Check 2

### Check 2: Is Railway reading them?
- In Variables tab, click on `TELEGRAM_BOT_TOKEN`
- Does it show the value? (it might be hidden with dots)
- If you can see/edit it → Variable is saved

### Check 3: Did Railway restart?
- Go to "Deployments" tab
- Do you see a new deployment after adding variables?
- If NO → Click three dots (⋮) → "Redeploy"

### Check 4: Check service type
- Go to "Settings" tab
- Is "Service Type" set to `Worker`?
- If NO → Change it to `Worker`

### Check 5: Check start command
- In Settings, is "Start Command" set to `python -m src.bot`?
- If NO → Set it to `python -m src.bot`

## 📞 Need More Help?

If you've followed all steps and still see the error:

1. **Take a screenshot** of your Variables tab
2. **Take a screenshot** of your Settings tab
3. Check Railway status: https://status.railway.app
4. Try deleting and recreating the service

## ✅ Success Indicators

You'll know it's working when you see in Logs:
```
2025-11-11 XX:XX:XX | INFO | root | Starting bot polling
2025-11-11 XX:XX:XX | INFO | aiogram.dispatcher | Run polling for bot @AIpomoshnikalissabot id=8399609153 - 'AIalisa'
2025-11-11 XX:XX:XX | INFO | root | Loaded 5 API keys and 4 models
```

**No more errors!** 🎉

