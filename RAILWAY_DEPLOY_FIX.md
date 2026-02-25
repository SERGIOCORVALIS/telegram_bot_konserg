# Railway Deployment Error Fix

## Problem
Deployment failed - deployment did not succeed

## Solution

### Step 1: Check Service Settings in Railway

1. Open project in Railway
2. Open your service
3. Go to **"Settings"**

### Step 2: Configure Service Type

Make sure:
- **Service Type**: `Worker` (not Web Service)
- **Start Command**: `python -m src.bot`
- **Build Command**: leave empty (Railway will automatically detect)

### Step 3: Check Environment Variables

Make sure all required variables are added (see RAILWAY_ENV_SETUP.md):
- `TELEGRAM_BOT_TOKEN`
- `OPENROUTER_API_KEY`
- `OPENROUTER_API_KEY_1` - `OPENROUTER_API_KEY_4` (optional)
- `APP_PUBLIC_URL` (optional)
- `APP_NAME` (optional)

### Step 4: Restart Deployment

1. In Railway, open the **"Deployments"** tab
2. Find the last deployment
3. Click the three dots (⋮) → **"Redeploy"**

Or just make a new commit and push to GitHub - Railway will automatically deploy:

```bash
git add .
git commit -m "Fix Railway deployment configuration"
git push origin main
```

### Step 5: Check Logs

1. In Railway, open the **"Logs"** tab
2. Find errors (in red)
3. Common errors:

#### Error: "Environment variables are required"
**Solution**: Add environment variables (see RAILWAY_ENV_SETUP.md)

#### Error: "ModuleNotFoundError: No module named 'src'"
**Solution**: Make sure `src/__init__.py` file exists (already added)

#### Error: "Command not found: python"
**Solution**: Make sure `runtime.txt` specifies Python 3.12

#### Error: "No such file or directory: requirements.txt"
**Solution**: Make sure `requirements.txt` file is in the project root

## Alternative Method: Using Docker

If problems persist, Railway can use Dockerfile:

1. In service settings, select **"Use Dockerfile"**
2. Railway will automatically use `Dockerfile` from the project root
3. Restart deployment

## Successful Deployment Verification

After fixing, logs should show:
```
Starting bot polling
Run polling for bot @AIpomoshnikalissabot id=...
Loaded X API keys and Y models
```

If you see these messages - the bot is running! ✅

## If Nothing Helps

1. Delete the service in Railway
2. Create a new service
3. Connect GitHub repository again
4. Add environment variables
5. Railway will automatically deploy

## Useful Debugging Commands

If you have Railway CLI installed:

```bash
# View logs
railway logs

# View environment variables
railway variables

# Restart service
railway restart
```
