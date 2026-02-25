# PowerShell script to start Telegram bot locally

Write-Host "Starting Telegram AI Bot..." -ForegroundColor Green

# Set environment variables
$env:TELEGRAM_BOT_TOKEN = "REDACTED"
$env:OPENROUTER_API_KEY = "REDACTED"
$env:OPENROUTER_API_KEY_1 = "REDACTED"
$env:OPENROUTER_API_KEY_2 = "REDACTED"
$env:OPENROUTER_API_KEY_3 = "REDACTED"
$env:OPENROUTER_API_KEY_4 = "REDACTED"
$env:OPENROUTER_API_KEY_5 = "REDACTED"
$env:OPENROUTER_API_KEY_6 = "REDACTED"
$env:APP_PUBLIC_URL = "https://example.com"
$env:APP_NAME = "AI Assistant Bot"

Write-Host "Environment variables set" -ForegroundColor Yellow

# Activate virtual environment and run bot
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

Write-Host "Starting bot..." -ForegroundColor Green
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

python -m src.bot

