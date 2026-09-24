# Quick Railway env setup for PowerShell.
# Secrets must come from environment variables or a local .env file (not committed).
# Usage: fill .env, then run: .\railway-setup.ps1

Write-Host "Setting Railway environment variables..." -ForegroundColor Cyan
Write-Host ""

try {
    $null = Get-Command railway -ErrorAction Stop
    Write-Host "Railway CLI found" -ForegroundColor Green
} catch {
    Write-Host "Railway CLI is not installed!" -ForegroundColor Red
    Write-Host "Install: npm i -g @railway/cli" -ForegroundColor Yellow
    Write-Host "See RAILWAY_QUICK_FIX_RU.md for details." -ForegroundColor Yellow
    exit 1
}

if (Test-Path ".env") {
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
}

if (-not $env:TELEGRAM_BOT_TOKEN -or -not $env:OPENROUTER_API_KEY) {
    Write-Host "Set TELEGRAM_BOT_TOKEN and OPENROUTER_API_KEY in .env or the environment." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Adding required variables..." -ForegroundColor Yellow

railway variables set TELEGRAM_BOT_TOKEN="$env:TELEGRAM_BOT_TOKEN"
railway variables set OPENROUTER_API_KEY="$env:OPENROUTER_API_KEY"

Write-Host ""
Write-Host "Adding optional additional OpenRouter keys (if present)..." -ForegroundColor Yellow

1..9 | ForEach-Object {
    $name = "OPENROUTER_API_KEY_$_"
    $value = [Environment]::GetEnvironmentVariable($name)
    if ($value) {
        railway variables set "$name=$value"
    }
}

Write-Host ""
Write-Host "Adding optional app settings..." -ForegroundColor Yellow

if (-not $env:APP_NAME) { $env:APP_NAME = "AI Assistant Bot" }
railway variables set APP_NAME="$env:APP_NAME"
if ($env:APP_PUBLIC_URL) {
    railway variables set APP_PUBLIC_URL="$env:APP_PUBLIC_URL"
}

Write-Host ""
Write-Host "Variables submitted. Railway should restart the service shortly." -ForegroundColor Green
Write-Host "Check Railway Dashboard → Logs." -ForegroundColor Cyan
Write-Host ""
