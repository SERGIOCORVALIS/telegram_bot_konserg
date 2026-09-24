# PowerShell script to start Telegram bot locally.
# Secrets must come from environment variables or a local .env file (not committed).

Write-Host "Starting Telegram AI Bot..." -ForegroundColor Green

if (-not (Test-Path ".env")) {
    Write-Host "Missing .env file. Copy .env.example to .env and fill in your secrets." -ForegroundColor Red
    exit 1
}

# Load .env into the process environment (python-dotenv will also load it)
Get-Content ".env" | ForEach-Object {
    $line = $_.Trim()
    if (-not $line -or $line.StartsWith("#")) { return }
    $parts = $line -split "=", 2
    if ($parts.Count -eq 2) {
        $name = $parts[0].Trim()
        $value = $parts[1].Trim().Trim('"').Trim("'")
        Set-Item -Path "Env:$name" -Value $value
    }
}

if (-not $env:TELEGRAM_BOT_TOKEN -or -not $env:OPENROUTER_API_KEY) {
    Write-Host "TELEGRAM_BOT_TOKEN and OPENROUTER_API_KEY must be set in .env" -ForegroundColor Red
    exit 1
}

if (-not $env:APP_NAME) { $env:APP_NAME = "AI Assistant Bot" }

Write-Host "Environment variables loaded from .env" -ForegroundColor Yellow

if (Test-Path ".\.venv\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & .\.venv\Scripts\Activate.ps1
}

Write-Host "Starting bot..." -ForegroundColor Green
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

python -m src.bot
