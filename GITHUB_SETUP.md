# GitHub Repository Setup Guide

## Step 1: Create Repository on GitHub

1. Go to [github.com](https://github.com) and sign in to your account (or create a new one)

2. Click the **"+"** button in the top right corner → **"New repository"**

3. Fill in the form:
   - **Repository name**: `telegram-ai-bot` (or any other name)
   - **Description**: `Telegram bot with AI models via OpenRouter`
   - Select **Public** or **Private**
   - **DO NOT** check "Add a README file", "Add .gitignore", "Choose a license" (already included)

4. Click **"Create repository"**

## Step 2: Connect Local Repository to GitHub

After creating the repository, GitHub will show instructions. Execute the following commands:

```bash
cd C:\Users\dolma\Documents\main_alisa

# Rename branch to main (if needed)
git branch -M main

# Add remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/telegram-ai-bot.git

# Upload code to GitHub
git push -u origin main
```

**Important:** Replace `YOUR_USERNAME` with your actual GitHub username and `telegram-ai-bot` with your repository name.

## Step 3: Verification

1. Refresh the repository page on GitHub
2. You should see all project files
3. Done! 🎉

## Additional: Setup for Railway/Render

After uploading to GitHub, you can immediately deploy the bot on Railway or Render:

1. **Railway**: 
   - Go to [railway.app](https://railway.app)
   - "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Add environment variables (see [QUICK_START_DEPLOY.md](QUICK_START_DEPLOY.md))

2. **Render**:
   - Go to [render.com](https://render.com)
   - "New +" → "Background Worker"
   - Connect GitHub repository
   - Configure environment variables

## Security

⚠️ **Important:** Make sure files with secrets (`.env`, `.env.txt` with real tokens) are not in the repository!

If you accidentally uploaded secrets:
1. Remove file from repository: `git rm --cached .env.txt`
2. Add to `.gitignore`: `.env.txt`
3. Make commit: `git commit -m "Remove secrets"`
4. Update secrets in GitHub (they are already compromised!)
5. Upload: `git push`

## Useful Git Commands

```bash
# Check status
git status

# View changes
git diff

# Add all changes
git add .

# Make commit
git commit -m "Description of changes"

# Upload to GitHub
git push

# Update from GitHub
git pull
```
