# ⚠️ API Keys Invalid - Solution Guide

## Test Results
```
[FAIL] All 5 API keys returned: 401 UNAUTHORIZED
Status: Invalid API key or key expired
```

**This means:** All your OpenRouter API keys are invalid, expired, or revoked.

## ✅ Solution: Get New API Keys

### Step 1: Check OpenRouter Account
1. Go to [openrouter.ai](https://openrouter.ai)
2. Sign in to your account
3. Go to **"Keys"** or **"API Keys"** section

### Step 2: Check Key Status
- Look at your API keys list
- Check if keys are **Active** or **Revoked**
- If revoked → Delete them and create new ones

### Step 3: Create New API Keys
1. In OpenRouter, click **"Create API Key"** or **"New Key"**
2. Give it a name (e.g., "Telegram Bot")
3. Copy the new key (starts with `sk-or-v1-`)
4. **Important:** Copy it immediately - you won't see it again!

### Step 4: Update Keys in Railway
1. Go to Railway → Your Project → Your Service → **Variables**
2. For each key:
   - Find the variable (e.g., `OPENROUTER_API_KEY`)
   - Click to edit
   - Replace the old key with the new one
   - **No quotes, no spaces**
   - Click **Save**

### Step 5: Verify Keys Work
Run the test script locally:
```bash
python test_api_keys.py
```

Or check Railway logs - should see:
```
Starting bot polling
Loaded X API keys and Y models
```

## 🔍 Why Keys Might Be Invalid

1. **Keys were revoked** - You or OpenRouter revoked them
2. **Keys expired** - Some keys have expiration dates
3. **Account issue** - Your OpenRouter account might have issues
4. **Wrong keys** - Keys copied incorrectly

## 📝 Quick Fix Checklist

- [ ] Logged into OpenRouter account
- [ ] Checked existing keys status
- [ ] Created new API key(s)
- [ ] Copied new key(s) correctly (no quotes/spaces)
- [ ] Updated `OPENROUTER_API_KEY` in Railway
- [ ] Updated `OPENROUTER_API_KEY_1` through `OPENROUTER_API_KEY_4` (if using)
- [ ] Railway restarted automatically
- [ ] Checked logs - see "Starting bot polling"
- [ ] Tested bot in Telegram - works!

## 🆘 Alternative: Use Single Key

If you only need one key:
1. Create **one** new API key in OpenRouter
2. Add only `OPENROUTER_API_KEY` in Railway
3. Remove or leave empty `OPENROUTER_API_KEY_1` through `OPENROUTER_API_KEY_4`
4. Bot will use the single key (and default keys from code if needed)

## ✅ After Fixing

Once you add valid keys:
- Railway will automatically restart
- Check logs - should see successful connection
- Bot will start responding in Telegram

## 📞 Need Help?

1. **OpenRouter Support:**
   - Check [OpenRouter Docs](https://openrouter.ai/docs)
   - OpenRouter Discord: [discord.gg/openrouter](https://discord.gg/openrouter)

2. **Verify Key Format:**
   - Valid key: `REDACTED`
   - Length: ~73 characters
   - Starts with: `sk-or-v1-`

3. **Test Key Manually:**
   ```bash
   curl https://openrouter.ai/api/v1/models \
     -H "Authorization: Bearer YOUR_KEY_HERE"
   ```
   Should return list of models, not 401 error.

