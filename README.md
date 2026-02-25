# DeepSeek V3.1 Telegram Bot

Telegram bot built with `aiogram` that answers user questions using the `DeepSeek V3.1 (free)` model via [OpenRouter](https://openrouter.ai/) API.

## Key Features

- Asynchronous message processing using `aiogram v3`.
- Single `aiohttp.ClientSession` with timeout for OpenRouter requests.
- Secure configuration loading and validation from environment variables.
- Error handling and INFO-level logging.
- `HTTP-Referer` and `X-Title` headers to comply with OpenRouter recommendations.
- Dialog history management for contextual responses.
- Rate limiting protection against spam.
- Multiple model and API key rotation for reliability.

## Quick Start

1. **Dependencies**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows PowerShell
   pip install -r requirements.txt
   ```

2. **Configuration**

   Create a `.env` file in the project root:
   ```
   TELEGRAM_BOT_TOKEN=1234567890:ABCDEF...
   OPENROUTER_API_KEY=or-...
   APP_PUBLIC_URL=https://example.com  # optional, but helps OpenRouter
   APP_NAME=DeepSeek QA Bot            # optional
   REQUEST_TIMEOUT=45                  # optional (seconds)
   ```

3. **Run**
   ```bash
   python -m src.bot
   ```

## Best Practices Used

- **aiogram**
  - Separation of settings and core logic.
  - Using `Router` inside `Dispatcher` for modularity.
  - Using `ChatActionSender` to notify users about bot activity.

- **OpenRouter**
  - HTTP session reuse and timeout configuration.
  - Passing `HTTP-Referer`/`X-Title` headers (OpenRouter recommendation).
  - Response validation and detailed error handling (`ClientResponseError`, `ClientError`).
  - Automatic model and API key rotation on rate limits.

- **General**
  - Clear logging format.
  - Configurable parameters via environment variables.
  - Minimal system prompt for consistent responses.
  - Dialog history management.
  - Rate limiting for spam protection.

## Deployment for 24/7 Operation

To run the bot 24/7 independently of your computer, see the detailed guide in [DEPLOYMENT.md](DEPLOYMENT.md).

**Quick start with Railway (recommended):**
1. Create a GitHub repository
2. Sign up at [railway.app](https://railway.app)
3. Connect the repository and add environment variables
4. The bot will automatically start and run continuously!

## Available Commands

- `/start` - Start a dialog (clears history)
- `/reset` - Clear dialog history
- `/about` - Bot information
- `/help` - Show available commands
- `/feedback` - Send feedback

## What's Next

- Add Redis storage for dialog history persistence.
- Implement request delays/limits for spam protection (already implemented in-memory).
- Support commands `/reset`, `/about`, `/feedback` (already implemented).

