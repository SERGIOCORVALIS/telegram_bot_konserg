#!/bin/bash
# Скрипт для быстрой настройки переменных окружения на Railway
# Использование: railway-setup.sh

echo "🚀 Настройка переменных окружения для Railway..."
echo ""

# Проверка наличия Railway CLI
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI не установлен!"
    echo "Установите Railway CLI: npm i -g @railway/cli"
    echo "Или следуйте инструкциям в RAILWAY_QUICK_FIX_RU.md"
    exit 1
fi

echo "✅ Railway CLI найден"
echo ""

# Обязательные переменные
echo "📝 Добавление обязательных переменных..."

railway variables set TELEGRAM_BOT_TOKEN="REDACTED"
railway variables set OPENROUTER_API_KEY="REDACTED"

echo ""
echo "📝 Добавление дополнительных ключей OpenRouter..."

railway variables set OPENROUTER_API_KEY_1="REDACTED"
railway variables set OPENROUTER_API_KEY_2="REDACTED"
railway variables set OPENROUTER_API_KEY_3="REDACTED"
railway variables set OPENROUTER_API_KEY_4="REDACTED"

echo ""
echo "📝 Добавление опциональных переменных..."

railway variables set APP_NAME="AI Assistant Bot"
# railway variables set APP_PUBLIC_URL="https://your-project-name.up.railway.app"  # Раскомментируйте и замените на ваш URL

echo ""
echo "✅ Все переменные добавлены!"
echo ""
echo "⏳ Подождите 10-30 секунд, Railway автоматически перезапустит сервис"
echo "📋 Проверьте логи в Railway Dashboard → Logs"
echo ""

