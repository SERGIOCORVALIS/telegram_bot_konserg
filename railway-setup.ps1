# Скрипт PowerShell для быстрой настройки переменных окружения на Railway
# Использование: .\railway-setup.ps1

Write-Host "🚀 Настройка переменных окружения для Railway..." -ForegroundColor Cyan
Write-Host ""

# Проверка наличия Railway CLI
try {
    $null = Get-Command railway -ErrorAction Stop
    Write-Host "✅ Railway CLI найден" -ForegroundColor Green
} catch {
    Write-Host "❌ Railway CLI не установлен!" -ForegroundColor Red
    Write-Host "Установите Railway CLI: npm i -g @railway/cli" -ForegroundColor Yellow
    Write-Host "Или следуйте инструкциям в RAILWAY_QUICK_FIX_RU.md" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "📝 Добавление обязательных переменных..." -ForegroundColor Yellow

railway variables set TELEGRAM_BOT_TOKEN="REDACTED"
railway variables set OPENROUTER_API_KEY="REDACTED"

Write-Host ""
Write-Host "📝 Добавление дополнительных ключей OpenRouter..." -ForegroundColor Yellow

railway variables set OPENROUTER_API_KEY_1="REDACTED"
railway variables set OPENROUTER_API_KEY_2="REDACTED"
railway variables set OPENROUTER_API_KEY_3="REDACTED"
railway variables set OPENROUTER_API_KEY_4="REDACTED"

Write-Host ""
Write-Host "📝 Добавление опциональных переменных..." -ForegroundColor Yellow

railway variables set APP_NAME="AI Assistant Bot"
# railway variables set APP_PUBLIC_URL="https://your-project-name.up.railway.app"  # Раскомментируйте и замените на ваш URL

Write-Host ""
Write-Host "✅ Все переменные добавлены!" -ForegroundColor Green
Write-Host ""
Write-Host "⏳ Подождите 10-30 секунд, Railway автоматически перезапустит сервис" -ForegroundColor Cyan
Write-Host "📋 Проверьте логи в Railway Dashboard → Logs" -ForegroundColor Cyan
Write-Host ""

