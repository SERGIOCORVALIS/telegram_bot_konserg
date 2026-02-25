# Bot Deployment Guide for 24/7 Operation

This guide will help you deploy the bot on a server so it runs 24/7 independently of your computer.

## Option 1: Railway (Recommended - Simplest and Free)

Railway provides a free plan with $5 credits per month, which is sufficient for running the bot.

### Step 1: Project Preparation

1. Make sure you have Git installed:
   ```bash
   git --version
   ```

2. Create a `Procfile` in the project root (for Railway):
   ```
   worker: python -m src.bot
   ```

3. Create a `runtime.txt` file (specify Python version):
   ```
   python-3.12
   ```

### Step 2: Railway Registration

1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub (create an account if needed)
3. Click "New Project" → "Deploy from GitHub repo"

### Step 3: Connect Repository

1. If you don't have a GitHub repository yet:
   - Create a repository on [github.com](https://github.com)
   - Upload the code:
     ```bash
     git init
     git add .
     git commit -m "Initial commit"
     git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
     git push -u origin main
     ```

2. In Railway, select your repository

### Step 4: Configure Environment Variables

In Railway:
1. Open your project
2. Go to "Variables"
3. Add variables:
   ```
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   OPENROUTER_API_KEY=your_openrouter_api_key
   OPENROUTER_API_KEY_1=your_additional_key_1
   OPENROUTER_API_KEY_2=your_additional_key_2
   OPENROUTER_API_KEY_3=your_additional_key_3
   OPENROUTER_API_KEY_4=your_additional_key_4
   APP_PUBLIC_URL=https://your-project.up.railway.app
   APP_NAME=AI Assistant Bot
   ```

### Step 5: Configure Deployment

1. In Railway, open "Settings"
2. In the "Deploy" section, select:
   - **Root Directory**: leave empty
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python -m src.bot`

3. Railway will automatically detect Python and install dependencies

### Step 6: Launch

1. Click "Deploy" or Railway will automatically deploy on GitHub push
2. Open the "Logs" tab to see bot logs
3. The bot should start and begin responding to messages!

---

## Option 2: Render (Railway Alternative)

### Step 1: Preparation

Create a `render.yaml` file in the project root:
```yaml
services:
  - type: worker
    name: telegram-bot
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python -m src.bot
    envVars:
      - key: TELEGRAM_BOT_TOKEN
        sync: false
      - key: OPENROUTER_API_KEY
        sync: false
      - key: APP_PUBLIC_URL
        value: https://your-project.onrender.com
      - key: APP_NAME
        value: AI Assistant Bot
```

### Step 2: Registration

1. Go to [render.com](https://render.com)
2. Sign in with GitHub
3. Click "New +" → "Background Worker"

### Step 3: Configuration

1. Connect your GitHub repository
2. Specify:
   - **Name**: telegram-bot
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python -m src.bot`
3. Add environment variables (same as Railway)
4. Click "Create Background Worker"

---

## Option 3: VPS (DigitalOcean, Hetzner, AWS EC2)

If you have a VPS server, you can deploy the bot there.

### Step 1: Connect to Server

```bash
ssh root@your-server-ip
```

### Step 2: Install Dependencies

```bash
# Update system
apt update && apt upgrade -y

# Install Python and Git
apt install -y python3 python3-pip python3-venv git

# Install systemd (for auto-start)
apt install -y systemd
```

### Step 3: Clone Project

```bash
cd /opt
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git telegram-bot
cd telegram-bot
```

### Step 4: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 5: Create .env File

```bash
nano .env
```

Add:
```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_API_KEY_1=your_additional_key_1
OPENROUTER_API_KEY_2=your_additional_key_2
OPENROUTER_API_KEY_3=your_additional_key_3
OPENROUTER_API_KEY_4=your_additional_key_4
APP_PUBLIC_URL=https://your-domain.com
APP_NAME=AI Assistant Bot
```

Save: `Ctrl+O`, `Enter`, `Ctrl+X`

### Step 6: Create systemd Service

```bash
sudo nano /etc/systemd/system/telegram-bot.service
```

Add:
```ini
[Unit]
Description=Telegram Bot Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/telegram-bot
Environment="PATH=/opt/telegram-bot/venv/bin"
ExecStart=/opt/telegram-bot/venv/bin/python -m src.bot
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Step 7: Start Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable auto-start
sudo systemctl enable telegram-bot

# Start bot
sudo systemctl start telegram-bot

# Check status
sudo systemctl status telegram-bot

# View logs
sudo journalctl -u telegram-bot -f
```

---

## Option 4: Docker (for Local Server or VPS)

### Step 1: Create Dockerfile

The file should already be created (see `Dockerfile`)

### Step 2: Create docker-compose.yml

The file should already be created (see `docker-compose.yml`)

### Step 3: Run

```bash
docker-compose up -d
```

### Step 4: View Logs

```bash
docker-compose logs -f
```

---

## Bot Verification

After deployment using any method:

1. Open Telegram
2. Find your bot
3. Send `/start`
4. Send any question
5. The bot should respond!

## Monitoring and Logs

- **Railway**: "Logs" tab in the dashboard
- **Render**: "Logs" tab in the dashboard
- **VPS**: `sudo journalctl -u telegram-bot -f`
- **Docker**: `docker-compose logs -f`

## Bot Updates

### Railway/Render:
Just do `git push` to your repository - automatic deployment!

### VPS:
```bash
cd /opt/telegram-bot
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart telegram-bot
```

### Docker:
```bash
docker-compose pull
docker-compose up -d
```

## Recommendations

1. **Railway** - Best choice for beginners (free, simple, automatic deployment)
2. **Render** - Good alternative to Railway
3. **VPS** - If you need full control (from $5/month)
4. **Docker** - If you already use Docker

## Troubleshooting

### Bot doesn't respond:
- Check logs for errors
- Make sure environment variables are set correctly
- Check that the bot is running (`systemctl status` or cloud logs)

### Connection errors:
- Check server internet connection
- Make sure tokens are correct
- Check firewall (internet access should be open)

### Rate limit errors:
- The bot automatically tries different models and keys
- Wait a few seconds and try again
